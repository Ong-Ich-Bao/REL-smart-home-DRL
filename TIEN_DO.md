# Tiến độ nhóm

**Ký hiệu:** ✅ xong · 🔄 đang làm · ⬜ chưa ai nhận

Muốn nhận việc: điền tên vào cột **Người làm**, đổi ⬜ → 🔄, push lên. Xong thì đổi → ✅ và ghi link kết quả.

## Bảng việc

| # | Việc | Người làm | Trạng thái | Kết quả / ghi chú |
|---|---|---|---|---|
| 1 | Clone, cài môi trường | Bảo | ✅ | Code gốc + model của tác giả trong repo |
| 2 | Sửa lỗi tương thích torch ≥ 2.6 (`torch.load`) | Bảo | ✅ | 2 dòng, xem commit "Fix torch.load…" |
| 3 | Test model gốc của tác giả trên cả năm test | Bảo | ✅ | DQN 1000.26 vs bài báo 976 — [ket_qua.md](ket_qua/ket_qua.md) mục 1–2 |
| 4 | Lấy số liệu chính xác Fig. 3/4 trong bài báo | Bảo | ✅ | [ket_qua.md](ket_qua/ket_qua.md) mục 2 |
| 5 | Train lại 12 lần (4 kW, 6 kW) + chẩn đoán | Bảo | ✅ | Chỉ 2/12 run thắng baseline, nguyên nhân dying ReLU — [ket_qua.md](ket_qua/ket_qua.md) mục 3 |
| 6 | Đọc hiểu bài báo + code, ghi chỗ lệch | Bảo | ✅ | [HUONG_DAN.md](HUONG_DAN.md) Phần 3–4 |
| 7 | Train thêm seed 5–12 cho cấu hình 6 kW, tìm run gần 730 € | Bảo | ✅ | Tốt nhất seed 8 = 980.60 €, chưa tới 730 — [ket_qua.md](ket_qua/ket_qua.md) mục 4–5 |
| 8 | Chạy giá TOU (`data/tou2.csv`), so với Fig. 4 | Bảo | ✅ | 6 kW seed 1 = 917 € (bài báo 894) — [ket_qua.md](ket_qua/ket_qua.md) mục 4–5 |
| 9 | Chạy cấu hình pin khác (10 kWh; hiệu suất 80%, 90%) | Bảo | ✅ | Đủ 5 cột còn lại của Fig. 3; 10 kWh/95% = 781 € (bài 766), 20 kWh/80% = 1078 € (bài 1037) — [ket_qua.md](ket_qua/ket_qua.md) mục 4–7 |
| 10 | Báo cáo — phần giới thiệu bài toán + mô hình MDP (state/action/reward) | Bảo | ✅ | Bản nháp đủ 9 mục trên Claude Docs (xuất được Word/PDF) — Bảo gửi link trong nhóm; cần điền tên thành viên |
| 11 | Báo cáo — phần kết quả: bảng bài báo vs chạy lại, biểu đồ | Bảo | ✅ | Trong báo cáo, mục 5 |
| 12 | Báo cáo — phần phân tích: chỗ lệch code/bài báo, dying ReLU | Bảo | ✅ | Trong báo cáo, mục 6–7 |
| 13 | Slide thuyết trình | Bảo | ✅ | 12 slide trên Claude (xuất được PPTX/PDF) — Bảo gửi link; cần điền tên thành viên ở slide bìa |
| 14 | Chuẩn bị câu hỏi vấn đáp | Bảo | ✅ | 18 câu kèm đáp án — Bảo gửi trong nhóm |
| 15 | Đọc lại báo cáo + slide, tập thuyết trình | | ⬜ | Bảo gửi kịch bản thuyết trình + đáp án vấn đáp trong nhóm |

Thêm việc mới: thêm dòng vào cuối bảng.

## Cập nhật gần nhất

Ghi mới nhất lên trên, mỗi lần 1 dòng.

- **21/10/2026 (tối) — Bảo:** Hoàn thành việc 10–14: báo cáo, slide, file vấn đáp. Sửa tài liệu: test là tất định (không "lệch nhẹ" như ghi trước đây).
- **21/10/2026 — Bảo:** Hoàn thành việc 7–9 (36 run mới). Mọi baseline khớp bài báo < 1 €; 3 cấu hình đạt gần số bài báo (lệch 2–4%); train thành công 12/48 run. Kết quả trùng từng chữ số với bản chạy độc lập của một bạn trong nhóm.
- **05/10/2026 — Bảo:** Hoàn thành việc 1–6, đưa repo lên GitHub.

## Cách cập nhật file này (git cơ bản)

Chạy trong terminal, ở thư mục repo. **Luôn `git pull` trước khi sửa** để lấy bản mới nhất của người khác.

```powershell
git pull                                   # 1. lấy bản mới nhất
# 2. sửa TIEN_DO.md (hoặc file khác) rồi lưu
git add TIEN_DO.md                         # 3. chọn file muốn đưa lên
git commit -m "Cap nhat tien do: <viec gi>" # 4. ghi lại thay đổi
git push                                   # 5. đẩy lên GitHub
```

- `git push` báo **rejected** ⇒ có người vừa đẩy trước bạn: chạy `git pull` rồi `git push` lại.
- `git pull` báo **CONFLICT** ⇒ hai người sửa cùng một dòng: mở file, tìm đoạn giữa `<<<<<<<` và `>>>>>>>`, giữ nội dung đúng, xoá 3 dòng đánh dấu, rồi `git add` → `git commit` → `git push`.
- Không đưa lên: file `CLAUDE.md`, thư mục `.claude/`, model tự train, file PDF — đã chặn sẵn trong `.gitignore`.
