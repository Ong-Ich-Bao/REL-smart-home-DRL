# Kết quả chạy lại

Máy chạy: Windows 11, Python 3.13, torch 2.9 (CPU), numpy 2.2, pandas 2.2.
Sửa code gốc: chỉ 1 chỗ, `dqn.py:127-128` thêm `weights_only=False` (xem nhật ký trong `../HUONG_DAN.md`).

Lệnh đã chạy: xem `../HUONG_DAN.md` Phần 5. Biểu đồ được lưu bằng cách chạy với `MPLBACKEND=Agg` rồi gọi `plt.savefig(...)` sau `m.test()`, không sửa `fig.show()` trong code.

## 1. Model có sẵn của tác giả (`saved_nets/rtp_20_10_90_2_2`)

Cấu hình thật (theo `properties.json`): pin 20 kWh, `max_en=1` (≈ 4 kW), hiệu suất 95%, giá RTP, mua = 2×SMP, bán = 0.5×SMP (= ¼ giá mua, khớp bài báo), ε lúc test = 0.0176.

### Test full năm thứ 2 (dòng 30000 → hết, 29 844 bước) — 84 giây

| Chiến lược | Tên trong bài báo | Chi phí cả năm | DQN rẻ hơn |
|---|---|---|---|
| **DQN** | proposed | **1000.26** | — |
| Xoay vòng 4 action (`step % 4`) — "compare" | Baseline 2 – alternating | 1176.15 | **14.95%** |
| Có PV, không pin (action 7) | Baseline 1 – greedy | 1250.84 | **20.03%** |
| Không PV, không pin | (không có trong bài) | 1973.54 | 49.32% |

Số in ra gốc: `DQN cost:-1000.26 | compare cost:-1176.15 | Gain over compare: 175.89( 14.95% )` — dấu âm vì code cộng dồn `-tiền_trả`.

Biểu đồ: `pretrained_test_full.png`. Log: `pretrained_test_full.log`.

### Test nhanh 2000 bước — 59 giây (phần lớn là nạp `params.json` 95 MB)

DQN 89.89 · xoay vòng 104.00 (DQN rẻ hơn 13.57%) · không pin 108.45 · không PV không pin 172.22. Biểu đồ: `pretrained_test_2000.png`.

## 2. Số liệu chính xác của bài báo (Fig. 3 và Fig. 4)

**Cách lấy:** Fig. 3/4 được nhúng trong PDF dưới dạng vector (pgfplots, file gốc `results_rtp.pdf`, `results_tou2.pdf`). Mình đọc toạ độ từng cột (lệnh `re`) và vị trí các vạch lưới trục y, rồi quy đổi tuyến tính sang €. Kết quả ra số tròn và khớp mọi con số ghi trong bài (730 €, 894 €, −41.60%, −40.68%, −47.66%; −35.27% tính lại ra 35.23% do làm tròn) ⇒ tin cậy được. Trang PDF được render bằng API `Windows.Data.Pdf` có sẵn của Windows để xem bằng mắt; ảnh cắt: `paper_fig2_prices.png`, `paper_fig3_rtp.png`, `paper_fig4_tou.png`, `paper_fig5_selfbalancing.png`.

**Fig. 3 — RTP, chi phí năm test (€):**

| Pin, hiệu suất | DQN 6 kW | DQN 4 kW | Baseline 2 xoay vòng (6 kW) | Baseline 1 không pin |
|---|---|---|---|---|
| 20 kWh, 80% | 1037 | 1094 | 1411 | 1250 |
| 10 kWh, 80% | 1050 | 1106 | 1407 | 1250 |
| 20 kWh, 90% | 876 | 1052 | 1212 | 1250 |
| 10 kWh, 90% | 910 | 1069 | 1212 | 1250 |
| **20 kWh, 95%** | **730** | **976** | **1127** | **1250** |
| 10 kWh, 95% | 766 | 998 | 1129 | 1250 |

**Fig. 4 — TOU (`tou2.csv`), chi phí năm test (€):**

| Pin, hiệu suất | DQN 6 kW | DQN 4 kW | Baseline 2 xoay vòng (6 kW) | Baseline 1 không pin |
|---|---|---|---|---|
| 20 kWh, 80% | 1384 | 1484 | 1928 | 1708 |
| 10 kWh, 80% | 1386 | 1484 | 1920 | 1708 |
| 20 kWh, 90% | 1113 | 1443 | 1634 | 1708 |
| 10 kWh, 90% | 1124 | 1450 | 1632 | 1708 |
| 20 kWh, 95% | 894 | 1279 | 1507 | 1708 |
| 10 kWh, 95% | 915 | 1291 | 1509 | 1708 |

Lưu ý: bài chỉ vẽ Baseline 2 với 6 kW, không có cột xoay vòng 4 kW.

### So với bài báo (model có sẵn = cấu hình 20 kWh / 95% / 4 kW)

| | Bài báo (Fig. 3) | Chạy lại model có sẵn | Lệch |
|---|---|---|---|
| DQN 4 kW | 976 | 1000.26 | +2.5% |
| Baseline 1 không pin | 1250 | 1250.84 | ≈ 0 (khớp) |
| Xoay vòng | 1127 (6 kW) | 1176.15 (4 kW) | khác cấu hình, không so trực tiếp |

- Baseline 1 khớp gần tuyệt đối ⇒ môi trường mô phỏng, dữ liệu và cách tính tiền **tái hiện đúng**.
- DQN lệch +2.5%: hợp lý vì lúc test vẫn còn ε ≈ 0.018 ngẫu nhiên (chạy lại sẽ ra số lệch nhẹ), và không chắc đây đúng là model tác giả dùng để vẽ hình.

## 3. Train lại từ đầu

Script: `run_train.py` (train 200 episode → lưu → test full năm → lưu biểu đồ), không sửa code gốc. Cấu hình chung: pin 20 kWh, hiệu suất 95%, giá RTP, `price_coefs=[2, 0.5]`, mọi siêu tham số giữ nguyên như code gốc. ε cuối = 0.0176 ở mọi run (khớp model có sẵn).

- `try5`: 5 episode, 16.5 s — chỉ để đo tốc độ.
- 4 run đầu (`run_4kw_1/2`, `run_6kw_1/2`): seed torch ngẫu nhiên, 4 run chạy song song mỗi run 12 luồng → ~26 phút/run.
- 8 run sau (`*_s1..s4`): seed torch cố định 1–4 (chỉ quyết định trọng số khởi tạo; numpy đã được code gốc seed bên trong `env.reset`), `torch.set_num_threads(1)`, 8 run song song → ~15 phút/run. **Tái lập được**: chạy lại cùng seed ra cùng kết quả.
- Test mỗi model: ~85–95 s.

### Kết quả (chi phí năm test, €; % âm = DQN rẻ hơn)

**4 kW** — baseline: xoay vòng 1176.15 · không pin 1250.84 · bài báo DQN = **976**

| Run | Seed | DQN | vs xoay vòng | vs không pin | Nơ-ron fc1 sống | Action greedy (3000 bước đầu) |
|---|---|---|---|---|---|---|
| *model có sẵn* | — | **1000.26** | −14.95% | −20.03% | 1/8 | 0: 722, 1: 2278 |
| run_4kw_1 | ngẫu nhiên | 1249.30 | +6.22% | −0.12% | 0/8 | chỉ 3 |
| run_4kw_2 | ngẫu nhiên | 1249.30 | +6.22% | −0.12% | 0/8 | chỉ 3 |
| run_4kw_s1 | 1 | 1231.67 | +4.72% | −1.53% | 0/8 | chỉ 1 |
| run_4kw_s2 | 2 | **1166.51** | **−0.82%** | −6.74% | 1/8 | 1: 800, 2: 780, 3: 1420 |
| run_4kw_s3 | 3 | 1245.12 | +5.86% | −0.46% | 2/8 | 1: 86, 3: 2914 |
| run_4kw_s4 | 4 | 1231.67 | +4.72% | −1.53% | 0/8 | chỉ 1 |

**6 kW** — baseline: xoay vòng 1127.32 (bài báo: 1127 ✓) · không pin 1250.84 (bài báo: 1250 ✓) · bài báo DQN = **730**

| Run | Seed | DQN | vs xoay vòng | vs không pin | Nơ-ron fc1 sống | Action greedy |
|---|---|---|---|---|---|---|
| run_6kw_1 | ngẫu nhiên | 1221.64 | +8.37% | −2.33% | 0/8 | chỉ 1 |
| run_6kw_2 | ngẫu nhiên | 1249.12 | +10.80% | −0.14% | 0/8 | chỉ 3 |
| run_6kw_s1 | 1 | 1221.64 | +8.37% | −2.33% | 0/8 | chỉ 1 |
| run_6kw_s2 | 2 | **994.32** | **−11.80%** | **−20.51%** | 1/8 | 1: 617, 2: 2383 |
| run_6kw_s3 | 3 | 1249.12 | +10.80% | −0.14% | 1/8 | chỉ 3 |
| run_6kw_s4 | 4 | 1249.12 | +10.80% | −0.14% | 0/8 | chỉ 3 |

(Cột nơ-ron/action đo bằng `diagnose.py`: chạy greedy 3000 bước test đầu, đếm nơ-ron ReLU lớp 1 có lúc nào > 0.)

### Nhận xét

1. **Môi trường tái hiện chính xác**: 2 baseline khớp số bài báo gần tuyệt đối (1250.84 vs 1250; 1127.32 vs 1127).
2. **Train lại rất bấp bênh**: 12 run → chỉ **1/6 run 6 kW** và **1/6 run 4 kW** thắng chiến lược xoay vòng; đa số chỉ ngang "không dùng pin". Khớp với cảnh báo trong README gốc ("có thể phải train lại hơn 10 lần").
3. **Nguyên nhân: "dying ReLU"** — lớp 1 chỉ có 8 nơ-ron nhận 1344 đầu vào, lr = 0.01, reward lớn (R1 tới −15, R2 ×10 so với bài) ⇒ trong lúc train cả 8 nơ-ron bị đẩy về vùng âm, mạng trả **hằng số** cho mọi state ⇒ luôn chọn 1 action (1 hoặc 3 = luôn xả pin) ⇒ pin luôn ~0 ⇒ chi phí ≈ không pin. Run nào thắng đều còn ≥ 1 nơ-ron sống; ngay cả model có sẵn của tác giả cũng chỉ còn 1/8.
4. Các run "chết" cho kết quả **trùng nhau từng chữ số** dù seed khác (vd. 1249.12 ×3) vì chính sách hằng số + numpy được code gốc seed cố định khi test.
5. Run tốt nhất 6 kW (994.32) vẫn **còn xa 730 € của bài báo** (−11.8% vs −35.2% so với xoay vòng). Model có sẵn 4 kW (1000.26) thì gần cột 976 € của bài. ⇒ Tái hiện được **xu hướng** (DQN thắng baseline khi train thành công) nhưng **không tái hiện được con số tốt nhất** chỉ với 6 lần thử mỗi cấu hình.

Biểu đồ: `run_*.png` (vd. `run_6kw_s2.png` — run tốt nhất, pin dao động 10–19 kWh; `run_4kw_1.png` — run chết, pin luôn ~0). Log: `run_*.log`.

## 4. Bảng tổng hợp: bài báo vs chạy lại (việc 7–9, chạy 21/10/2026)

36 run mới, mọi siêu tham số giữ như code gốc, giá `[2, 0.5]`, seed torch cố định. Lệnh: `python ../ket_qua/run_train.py <tên> <max_en> <seed> <pin> <hiệu suất> <file giá>` (script đã thêm 3 tham số cuối, code gốc không đổi). 12 run song song, ~10–13 phút train mỗi run.

**"Học được"** = rẻ hơn cả 2 baseline **và** rẻ hơn "không pin" ít nhất 5% (tức là agent thật sự dùng pin). Cột "Tốt nhất" là run rẻ nhất trong các seed đã chạy.

| Giá | Pin, hiệu suất, công suất | DQN bài báo | **Tốt nhất chạy lại** (seed) | Lệch | Run học được | Xoay vòng: bài / chạy lại | Không pin: bài / chạy lại |
|---|---|---|---|---|---|---|---|
| RTP | 20 kWh, 95%, 6 kW | 730 | 980.60 (s8) | +34% | 2/12 | 1127 / 1127.32 | 1250 / 1250.84 |
| RTP | 20 kWh, 95%, 4 kW | 976 | 1000.26 (model tác giả); 1166.51 (s2) | +2.5% | 1/6 | — / 1176.15 | 1250 / 1250.84 |
| RTP | 10 kWh, 95%, 6 kW | 766 | **780.83** (s3) | **+1.9%** | 2/4 | 1129 / 1129.20 | 1250 / 1250.84 |
| RTP | 20 kWh, 90%, 6 kW | 876 | 1137.32 (s3) | +30% | 1/4 | 1212 / 1212.47 | 1250 / 1250.84 |
| RTP | 10 kWh, 90%, 6 kW | 910 | 1225.66 (cả 4 seed) | +35% | 0/4 | 1212 / 1212.51 | 1250 / 1250.84 |
| RTP | 20 kWh, 80%, 6 kW | 1037 | **1077.77** (s3) | **+3.9%** | 2/4 | 1411 / 1411.59 | 1250 / 1250.84 |
| RTP | 10 kWh, 80%, 6 kW | 1050 | 1255.08 (s1–s3) | +20% | 0/4 | 1407 / 1407.31 | 1250 / 1250.84 |
| TOU | 20 kWh, 95%, 6 kW | 894 | **917.33** (s1) | **+2.6%** | 2/4 | 1507 / 1507.93 | 1708 / 1709.00 |
| TOU | 20 kWh, 95%, 4 kW | 1279 | 1455.83 (s2) | +14% | 2/4 | — / 1587.00 | 1708 / 1709.00 |

(Dòng 4 kW lấy từ mục 1 và 3. Bài báo chỉ vẽ baseline xoay vòng với 6 kW.)

**Kết luận chính:**
1. **Môi trường tái hiện chính xác ở cả 9 cấu hình**: mọi baseline lệch bài báo < 1 €.
2. **Ba cấu hình chạm gần số bài báo** (lệch 2–4%): 10 kWh/95% RTP, 20 kWh/80% RTP, TOU 6 kW. ⇒ Con số trong bài **đạt được**, nhưng là của run tốt nhất trong nhiều lần train. Khớp với README gốc ("có thể phải train lại hơn 10 lần").
3. Cấu hình chính của bài (20 kWh/95%/6 kW, 730 €) **vẫn chưa đạt** sau 12 seed (tốt nhất 980.60).
4. **Tỉ lệ train thành công chung: 12/48 run (25%)**, tính cả 12 run ở mục 3. Hai cấu hình pin 10 kWh hiệu suất 80–90% thì 0/8 run học được (mới thử 4 seed mỗi cấu hình, chưa đủ để kết luận là do cấu hình).

Log: `<tên>.log`, biểu đồ: `<tên>.png`, tên dạng `tou_6kw_s1`, `b10e95_6kw_s3` (= pin 10 kWh, hiệu suất 95%, 6 kW, seed 3). Nơ-ron/action: `diagnose_viec789.txt`.

## 5. Chi tiết từng run (chi phí năm test, €; % âm = DQN rẻ hơn)

Cột "Nơ-ron" = số nơ-ron fc1 còn sống / 8; "Action" = action greedy trên 3000 bước test đầu (đo bằng `diagnose.py`).

**RTP, 20 kWh, 95%, 6 kW, seed 5–12 (việc 7)** — xoay vòng 1127.32 · không pin 1250.84

| Seed | DQN | vs xoay vòng | vs không pin | Nơ-ron | Action |
|---|---|---|---|---|---|
| 5 | 1260.58 | +11.82% | +0.78% | 1/8 | 0: 387, 3: 2613 |
| 6 | 1241.61 | +10.14% | −0.74% | 2/8 | 1: 1869, 3: 1131 |
| 7 | 1221.64 | +8.37% | −2.33% | 0/8 | chỉ 1 |
| **8** | **980.60** | **−13.01%** | **−21.60%** | 2/8 | 0: 171, 1: 985, 2: 1844 |
| 9 | 1221.64 | +8.37% | −2.33% | 0/8 | chỉ 1 |
| 10 | 1249.12 | +10.80% | −0.14% | 0/8 | chỉ 3 |
| 11 | 1204.14 | +6.81% | −3.73% | 1/8 | 1: 40, 2: 2440, 3: 520 |
| 12 | 1227.81 | +8.91% | −1.84% | 1/8 | 1: 2159, 3: 841 |

Gộp với mục 3 (seed 1–4 + 2 run ngẫu nhiên): 2/12 run thắng (seed 2: 994.32, seed 8: 980.60).

**TOU (`tou2.csv`), 20 kWh, 95% (việc 8)** — không pin 1709.00

| Run | DQN | vs xoay vòng | vs không pin | Nơ-ron | Action |
|---|---|---|---|---|---|
| **6 kW s1** | **917.33** | **−39.17%** | **−46.32%** | 1/8 | 0: 548, 1: 2452 |
| 6 kW s2 | 1438.28 | −4.62% | −15.84% | 2/8 | 1: 690, 2: 229, 3: 2081 |
| 6 kW s3 | 1706.72 | +13.18% | −0.13% | 0/8 | chỉ 3 |
| 6 kW s4 | 1706.72 | +13.18% | −0.13% | 0/8 | chỉ 3 |
| 4 kW s1 | 1706.76 | +7.55% | −0.13% | 0/8 | chỉ 3 |
| **4 kW s2** | **1455.83** | **−8.27%** | **−14.81%** | 2/8 | 0: 347, 1: 1223, 2: 1430 |
| 4 kW s3 | 1675.94 | +5.60% | −1.93% | 0/8 | chỉ 1 |
| 4 kW s4 | 1520.87 | −4.17% | −11.01% | 2/8 | 0: 14, 1: 74, 2: 1611, 3: 1301 |

Xoay vòng: 6 kW 1507.93 (bài báo 1507 ✓), 4 kW 1587.00. Bài báo: DQN 6 kW = 894 (−40.68% vs xoay vòng); run s1 đạt −39.17%.

**RTP, các cấu hình pin khác, 6 kW (việc 9)**

| Cấu hình | Seed | DQN | vs xoay vòng | vs không pin | Nơ-ron | Action |
|---|---|---|---|---|---|---|
| 10 kWh, 95% (xoay vòng 1129.20) | 1 | 1020.12 | −9.66% | −18.45% | 2/8 | 1: 537, 2: 2034, 3: 429 |
| | 2 | 1238.57 | +9.69% | −0.98% | 1/8 | 1: 978, 3: 2022 |
| | **3** | **780.83** | **−30.85%** | **−37.58%** | 2/8 | 0: 504, 1: 2324, 2: 172 |
| | 4 | 1163.02 | +3.00% | −7.02% | 1/8 | 1: 2264, 2: 730, 3: 6 |
| 20 kWh, 90% (xoay vòng 1212.47) | 1 | 1250.99 | +3.18% | +0.01% | 0/8 | chỉ 3 |
| | 2 | 1250.69 | +3.15% | −0.01% | 1/8 | 1: 276, 3: 2724 |
| | **3** | **1137.32** | **−6.20%** | **−9.08%** | 1/8 | 1: 1272, 2: 777, 3: 951 |
| | 4 | 1225.66 | +1.09% | −2.01% | 0/8 | chỉ 1 |
| 20 kWh, 80% (xoay vòng 1411.59) | 1 | 1255.08 | −11.09% | +0.34% | 0/8 | chỉ 3 |
| | 2 | 1082.83 | −23.29% | −13.43% | 1/8 | 0: 56, 1: 742, 2: 2202 |
| | **3** | **1077.77** | **−23.65%** | **−13.84%** | 2/8 | 0: 3, 1: 562, 2: 2435 |
| | 4 | 1233.96 | −12.58% | −1.35% | 1/8 | chỉ 1 |
| 10 kWh, 90% (xoay vòng 1212.51) | 1–4 | 1225.66 (cả 4) | +1.08% | −2.01% | 0–1/8 | chỉ 1 |
| 10 kWh, 80% (xoay vòng 1407.31) | 1–3 | 1255.08 | −10.82% | +0.34% | 0/8 | chỉ 3 |
| | 4 | 1281.36 | −8.95% | +2.44% | 2/8 | 0: 400, 1: 60, 2: 1773, 3: 767 |

**Bẫy khi đọc:** ở hiệu suất 80%, chiến lược xoay vòng còn **đắt hơn không pin** (1411 > 1250) vì sạc/xả lỗ 20%. Vì vậy run chết (luôn action 3) vẫn "rẻ hơn xoay vòng 11%", nhưng thực chất **không dùng pin**: chỉ ngang không pin (+0.34%). Phải so với cả 2 baseline.

## 6. Run "chết" cho cùng một con số, dù khác seed và khác dung lượng pin

RTP, 6 kW:

| Chính sách hằng số | Hiệu suất 95% | 90% | 80% |
|---|---|---|---|
| Luôn action 1 | 1221.64 | 1225.66 | 1233.96 |
| Luôn action 3 | 1249.12 | 1250.99 | 1255.08 |

Ví dụ 1225.66 xuất hiện ở cả `b20e90_s4` (20 kWh) lẫn `b10e90_s1–s4` (10 kWh). Lý do: agent luôn xả pin, nên pin gần như luôn ~0 và dung lượng pin không còn ảnh hưởng tới kết quả; chỉ còn hiệu suất tác động tới phần năng lượng ít ỏi đi qua pin. Đây là dấu hiệu nhận biết nhanh run bị dying ReLU (xem mục 3, nhận xét 3–4).

## 7. Tái lập kết quả

- **Cùng máy:** 12 run (seed 1–4, 4 kW và 6 kW) bị chạy lại ngoài ý muốn ngày 21/10, 12 run song song, ra **trùng từng chữ số** với các run cùng seed ngày 05/10. Log: `tai_lap/`.
- **Khác máy:** một bạn trong nhóm chạy độc lập seed 5–12 (6 kW), TOU 6 kW và pin 10 kWh trên máy riêng. Kết quả trùng từng chữ số với bảng mục 5 (vd. seed 8 = 980.60, TOU = 1706.72, 10 kWh/90% = 1225.66, 10 kWh/80% = 1255.08). Bạn ấy còn chạy thêm pin 10 kWh với 4 kW (seed 1): 80% → 1239.35, 90% → 1234.20 (≈ không pin, run chết); 2 số này chưa có log gốc nên không đưa vào bảng.
- ⇒ Với `torch.manual_seed(k)`, kết quả **tất định**: không phụ thuộc số run chạy song song và máy chạy (cùng phiên bản thư viện).
- Ghi chú: log của 12 run việc 7–8 (seed 5–12, TOU 6 kW) bị mất khi đang chạy. Số trong bảng lấy từ việc **test lại model đã lưu** bằng `run_test.py` (test tất định nên ra đúng số cũ; trùng với số bạn trong nhóm chạy được). 12 log này chỉ có phần test (dòng `PROPERTIES`), không có `TRAIN_SECONDS`.
