# Chuẩn bị vấn đáp

Mỗi câu: **trả lời ngắn** (nói trong 1–2 câu) → giải thích → chỗ trong code để chỉ khi thầy hỏi tiếp. Số liệu lấy từ [ket_qua/ket_qua.md](ket_qua/ket_qua.md).

---

## A. Thuật toán DQN

### 1. Tại sao cần replay buffer?

**Ngắn:** để phá tương quan giữa các mẫu liên tiếp và dùng lại kinh nghiệm cũ nhiều lần.

- Các bước liên tiếp gần như giống nhau (giá, nắng, mức pin chỉ đổi chút ít sau 15 phút). Học ngay từng bước thì gradient luôn kéo về một hướng, mạng "quên" những gì học trước và dễ dao động.
- Buffer lưu 2000 mẫu `(s, a, r, s')`, mỗi lần học lấy ngẫu nhiên 32 mẫu ⇒ các mẫu gần như độc lập, giống học có giám sát.
- Code: `store_transition()` và `learn()` trong [dqn.py](smart-home-energy-trading-with-DRL/dqn.py) (dòng 68–97), `np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)`.

### 2. Target net cập nhật khi nào, giải quyết gì?

**Ngắn:** copy từ mạng chính sau mỗi 100 lần `learn()`; giữ cho "mục tiêu" đứng yên một lúc.

- Mục tiêu `y = r + γ·max Q(s', a')`. Nếu tính `y` bằng chính mạng đang học thì mỗi lần cập nhật, mục tiêu cũng dịch theo, kiểu "đuổi theo cái bóng của mình" ⇒ dễ phân kỳ.
- Target net là bản sao cập nhật chậm ⇒ mục tiêu ổn định trong 100 lần học.

### 3. Agent bắt đầu học từ khi nào?

**Ngắn:** khi buffer có hơn 2000 mẫu, tức từ bước 2001, giữa episode thứ 3.

- Điều kiện `if dqn.memory_counter > self.memory_capacity: dqn.learn()` ở [HEMS.py:124](smart-home-energy-trading-with-DRL/HEMS.py#L124).
- Mỗi episode 672 bước ⇒ 2 episode đầu = 1344 bước, chưa đủ; đến bước 2001 (episode 3) mới học.
- Từ đó học **sau mỗi bước**, không phải cuối episode.

### 4. γ = 0.9 nghĩa là agent "nhìn xa" bao nhiêu? Có đủ để "sạc trưa, bán tối" không?

**Ngắn:** khoảng 1/(1−γ) = 10 bước = 2.5 giờ — **không đủ**; vì thế mới cần reward phụ R2.

- Sạc lúc trưa rồi bán lúc tối cách nhau 6–8 giờ = 24–32 bước. Phần thưởng sau 30 bước bị nhân 0.9³⁰ ≈ 0.04, gần như mất.
- Chỉ với R3 (tiền điện), agent thấy sạc = tốn tiền ngay, còn lợi ích thì quá xa ⇒ học được "đừng sạc".
- R2 thưởng **ngay lập tức** khi sạc lúc giá thấp hơn trung vị và xả lúc giá cao ⇒ bù cho tầm nhìn ngắn. Đây là lý do reward shaping cần thiết trong bài này.

### 5. Bỏ R1 hoặc R2 thì sao?

- **Bỏ R1** (phạt pin quá cạn/quá đầy): không còn gì giữ pin trong vùng 10–80%. R2 thưởng sạc khi giá thấp ⇒ agent dễ sạc đầy 100% rồi giữ đó; pin đầy thì không sạc thêm được khi giá thấp tiếp theo.
- **Bỏ R2**: như câu 4, γ = 0.9 không thấy được lợi ích bán tối ⇒ agent học "không dùng pin", chi phí ≈ baseline không pin.
- Lưu ý: R1 và R2 là **gợi ý**, mục tiêu thật vẫn là R3. Shaping sai có thể khiến agent tối ưu điểm phụ thay vì tiền điện.

### 6. Vì sao input mạng là 1344 chiều? `n_days=1` thì sao?

**Ngắn:** 7 biến × 2 ngày × 96 bước/ngày = 1344. Với 1 ngày: 7 × 96 = 672.

- 7 biến: mức pin, PV, tiêu thụ, EV, giá, chi phí, giờ trong ngày ([env.py:76](smart-home-energy-trading-with-DRL/env.py#L76)). Bài báo chỉ có 5 biến (960 chiều).
- Bẫy: `HEMS.__init__` gán cứng `self.n_days = 2`, chỉ `train(n_days=…)` nhận tham số ⇒ đổi phải sửa cả hai chỗ, nếu không train và test lệch kích thước.

### 7. Vì sao DQN mà không dùng thuật toán khác?

**Ngắn:** chỉ có 4 action rời rạc ⇒ DQN là lựa chọn đơn giản và đủ.

- Action liên tục (ví dụ sạc bao nhiêu kW) mới cần policy gradient / DDPG / SAC.
- Hướng cải tiến dễ nhất trong họ DQN: Double DQN (giảm ước lượng Q quá cao), Dueling DQN.

### 8. Vì sao test có ε ngẫu nhiên mà kết quả vẫn lặp lại y hệt?

**Ngắn:** `Env.__init__` luôn gọi `reset(0)` ⇒ numpy được seed = 0 ngay trước khi test, nên chuỗi "ngẫu nhiên" lần nào cũng giống nhau.

- `test()` dùng `self.epsilon` đã lưu (≈ 0.018) ⇒ khoảng 2% bước là ngẫu nhiên, nhưng là cùng một chuỗi ngẫu nhiên.
- Muốn test **hoàn toàn greedy**: đặt `m.epsilon = 0` trước `m.test()`.

---

## B. Kết quả chạy lại

### 9. Làm sao biết nhóm chạy lại đúng?

**Ngắn:** hai baseline không có gì ngẫu nhiên, và chúng khớp bài báo trong phạm vi 1 € ở cả 9 cấu hình.

- Ví dụ: không pin 1250.84 vs bài 1250; xoay vòng 6 kW 1127.32 vs 1127; TOU 1507.93 vs 1507.
- ⇒ Dữ liệu, mô phỏng pin, cách tính tiền đều đúng. Chỗ khác biệt chỉ còn nằm ở DQN.
- Số của bài báo đọc **chính xác** từ vector trong PDF, không ước lượng bằng mắt.

### 10. Tại sao không đạt 730 € như bài báo?

**Ngắn:** train rất bấp bênh; bài báo nhiều khả năng báo run tốt nhất sau nhiều lần train.

- 12 seed cho cấu hình chính → tốt nhất 980.60 €. Nhưng 3 cấu hình khác đạt gần số bài (lệch 2–4%) ⇒ số trong bài **đạt được**, chỉ cần đủ may.
- README gốc tự nhận "có thể phải train lại hơn 10 lần".
- Thêm: bài không ghi seed, không ghi siêu tham số, R1/R2 trong code khác công thức in trong bài (xem câu 13).

### 11. "Dying ReLU" là gì, sao biết nó xảy ra?

**Ngắn:** nơ-ron ReLU có đầu vào luôn âm ⇒ luôn ra 0, gradient bằng 0, không bao giờ sống lại. Lớp 1 chỉ có 8 nơ-ron, chết hết thì mạng trả hằng số.

- Đo bằng `ket_qua/diagnose.py`: chạy 3000 bước test, đếm nơ-ron lớp 1 nào có lúc > 0.
- Run "chết": 0/8 nơ-ron sống, luôn chọn đúng 1 action (1 hoặc 3 = luôn xả pin) ⇒ pin ~0 ⇒ chi phí ≈ không pin.
- Nguyên nhân hợp lý: lớp 1 nhận 1344 đầu vào nhưng chỉ có 8 nơ-ron, lr = 0.01 khá lớn, reward lớn và lệch âm (R1 tới −15, R2 gấp 10 lần công thức bài).
- Cách sửa có thể thử: LeakyReLU, lr nhỏ hơn, chuẩn hoá/cắt reward, nhiều nơ-ron hơn, gradient clipping.

### 12. Tại sao các run chết ra **cùng một con số** dù khác seed, thậm chí khác dung lượng pin?

**Ngắn:** chính sách hằng số + môi trường tất định ⇒ kết quả chỉ phụ thuộc action cố định đó và hiệu suất pin.

- Luôn xả pin ⇒ pin luôn ~0 ⇒ dung lượng 10 hay 20 kWh không còn ý nghĩa.
- Ví dụ 1225.66 € xuất hiện ở cả pin 20 kWh lẫn 10 kWh (cùng hiệu suất 90%, luôn action 1).

### 13. Code khác bài báo những gì quan trọng nhất?

1. **R2** không chia dung lượng pin và dùng SMP gốc ⇒ lớn gấp 10 lần công thức trong bài (với pin 20 kWh).
2. **R1** phạt tối đa −16 khi pin đầy (bài ghi −4 / −2), luôn cộng +1, và công thức in trong bài có vẻ bị đảo ngưỡng.
3. Không seed torch ⇒ kết quả train không lặp lại được.
4. State 7 biến thay vì 5; giá bán mặc định `[2, 1]` thay vì `[2, 0.5]`; tên baseline 1/2 đảo ngược.

Đủ 11 điểm: [HUONG_DAN.md](HUONG_DAN.md) Phần 4.

### 14. Nhóm sửa gì trong code gốc?

**Ngắn:** chỉ 1 chỗ, 2 dòng: thêm `weights_only=False` vào `torch.load` ([dqn.py:127-128](smart-home-energy-trading-with-DRL/dqn.py#L127-L128)), vì PyTorch ≥ 2.6 mặc định không nạp được nguyên đối tượng mạng. Mọi script khác (`run_train.py`, `run_test.py`, `diagnose.py`) viết thêm bên ngoài, không đụng code gốc.

### 15. Ở hiệu suất 80%, DQN "rẻ hơn xoay vòng 11%" — vậy là học tốt?

**Không.** Hiệu suất 80% ⇒ mỗi lần sạc/xả lỗ 20%, nên chiến lược xoay vòng còn **đắt hơn không dùng pin** (1411 > 1250). Run chết (không dùng pin) tự nhiên rẻ hơn xoay vòng. Phải so với **cả hai** baseline: run đó chỉ ngang không pin (+0.34%).

### 16. Giá RTP và TOU khác nhau thế nào, cái nào dễ hơn cho agent?

- **RTP:** giá thị trường thay đổi liên tục (8284 mức giá khác nhau).
- **TOU:** chỉ 3 mức giá theo khung giờ cố định (0.06 / 0.075 / 0.09 SMP) ⇒ quy luật lặp lại mỗi ngày, chênh giá lớn.
- Kết quả: run TOU tốt nhất rẻ hơn xoay vòng **39%**, so với 13% ở RTP 20 kWh/95%. Quy luật đơn giản và chênh lệch lớn giúp agent dễ học "sạc giờ rẻ, xả giờ đắt".

### 17. Có rò rỉ dữ liệu train sang test không?

**Không.** Train lấy các tuần trong dòng 0–29 999 (năm 1); test chạy từ dòng 30 000 đến hết (năm 2), không học thêm. Cửa sổ 2 ngày đầu tiên của test có nhìn lại 192 bước cuối năm 1, nhưng đó chỉ là lịch sử quan sát, không phải nhãn.

### 18. Kết quả có tái lập được không?

**Có, tuyệt đối** khi cố định `torch.manual_seed(k)`. Numpy đã được code gốc seed sẵn (`Env.__init__` → `reset(0)`), chỉ còn trọng số khởi tạo của torch là ngẫu nhiên. Đã kiểm: 12 run chạy lại trùng từng chữ số; một bạn trong nhóm chạy trên máy khác cũng ra trùng từng chữ số.
