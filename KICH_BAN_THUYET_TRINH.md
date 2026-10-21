# Kịch bản thuyết trình (12 slide, khoảng 10–12 phút)

**Cách dùng file này:**
- Mỗi slide có 3 phần: **Lời nói** (đọc to vài lần, rồi nói bằng lời của mình), **Nhớ 1 câu** (nếu quên hết thì nói câu này), **Chuyển** (câu nối sang slide sau).
- Đừng đọc chữ trên slide. Slide là để thầy cô nhìn, còn bạn kể chuyện.
- Công thức: chỉ nói **nó dùng để làm gì**, không giải thích ký hiệu.
- Gợi ý chia người: người 1 nói slide 1–4, người 2 nói slide 5–8, người 3 nói slide 9–12.
- Bị hỏi khó: xem [VAN_DAP.md](VAN_DAP.md).

---

## Slide 1 — Bìa (30 giây)

**Lời nói:**
> Em chào thầy cô và các bạn. Nhóm em làm đề tài tái hiện một bài báo về học tăng cường: dùng Deep Q-Network để giảm tiền điện cho một ngôi nhà thông minh. Bài báo đăng ở hội nghị BuildSys năm 2023, có công khai code. Việc của nhóm là lấy code đó về, chạy lại, hiểu nó, và so từng con số với bài báo.

**Nhớ 1 câu:** Nhóm chạy lại một bài báo RL có sẵn code và kiểm tra xem kết quả có đúng như bài nói không.

**Chuyển:** "Trước hết, bài toán là gì?"

---

## Slide 2 — Bài toán (1 phút)

**Lời nói:**
> Hãy tưởng tượng một ngôi nhà có ba thứ: pin mặt trời trên mái, một cục pin lưu điện trong nhà, và dây nối lưới điện để mua hoặc bán điện.
>
> Cứ mỗi 15 phút, hệ thống phải quyết định: nên sạc pin hay xả pin, nên mua điện hay bán điện. Mục tiêu là cuối năm trả ít tiền điện nhất.
>
> Điểm quan trọng là giá mua đắt gấp 4 lần giá bán. Nên bán điện đi thì không lời mấy, lợi nhất là tích điện lúc rẻ để tự dùng lúc đắt. Nhưng lúc nào là "rẻ", lúc nào là "đắt" thì giá thay đổi liên tục, nên rất khó viết luật bằng tay. Đó là lý do dùng học tăng cường.
>
> Dữ liệu là số đo thật của một nhà ở Hy Lạp trong 2 năm. Năm đầu để máy học, năm sau để kiểm tra.

**Nhớ 1 câu:** Mỗi 15 phút chọn sạc/xả, mua/bán sao cho tiền điện cả năm thấp nhất.

**Chuyển:** "Để máy học được, phải mô tả bài toán theo dạng của học tăng cường."

---

## Slide 3 — Mô hình MDP (1 phút 30)

**Lời nói:**
> Học tăng cường cần ba thứ: agent nhìn thấy gì, được làm gì, và được thưởng phạt ra sao.
>
> **Nhìn thấy (state):** agent xem lại 2 ngày gần nhất: mức pin, điện mặt trời, điện nhà dùng, giá điện, và vài thông tin khác. Tổng cộng là một dãy 1344 con số.
>
> **Được làm (action):** chỉ có 4 lựa chọn, ví dụ sạc pin hết cỡ, hoặc xả pin rồi bán phần dư.
>
> **Thưởng phạt (reward):** có 3 phần cộng lại.
> - Phần chính là **tiền điện**: trả càng nhiều thì điểm càng thấp. Đây là cái mình thật sự muốn tối ưu.
> - Hai phần còn lại là **gợi ý** cho agent học nhanh hơn. Một phần phạt nếu để pin quá cạn hoặc quá đầy. Phần kia thưởng nếu sạc lúc giá rẻ và xả lúc giá đắt.
>
> Phần gợi ý thứ hai rất cần thiết. Agent chỉ "nhìn xa" được khoảng 2 tiếng rưỡi. Nếu chỉ nhìn tiền điện, nó thấy sạc pin là tốn tiền ngay, còn cái lợi lúc tối thì quá xa nên không thấy. Phần thưởng gợi ý cho nó biết ngay là "sạc lúc này là đúng".

**Về công thức `R1 + 3·R2 + 3·R3`:** chỉ cần nói "điểm thưởng là tổng của ba phần: giữ pin an toàn, mua rẻ bán đắt, và tiền điện; hai phần sau được nhân 3 cho quan trọng hơn".

**Nhớ 1 câu:** Agent nhìn 2 ngày lịch sử, chọn 1 trong 4 việc, và được chấm điểm chủ yếu bằng tiền điện.

**Chuyển:** "Còn agent học bằng cách nào? Đó là thuật toán DQN."

---

## Slide 4 — DQN (1 phút 30)

**Lời nói:**
> DQN là một mạng nơ-ron học cách **chấm điểm từng lựa chọn**: "ở tình huống này, chọn sạc pin thì về lâu dài được bao nhiêu điểm". Rồi agent chọn việc có điểm cao nhất.
>
> Hàng trên là lúc agent làm việc. Nó nhìn tình hình, mạng chấm điểm 4 lựa chọn, rồi nó chọn. Ban đầu agent chưa biết gì nên phần lớn chọn bừa để khám phá. Càng về sau càng ít chọn bừa, cuối cùng chỉ còn khoảng 2%.
>
> Hàng dưới là lúc agent học. Mỗi bước, nó ghi kinh nghiệm vào một "cuốn sổ" chứa 2000 dòng. Khi học, nó lấy ngẫu nhiên 32 dòng trong sổ ra ôn. Ôn ngẫu nhiên giúp không bị học lệch theo mấy bước gần nhất, vì các bước liền nhau gần như giống hệt nhau.
>
> Còn một mẹo nữa: một bản sao của mạng, chỉ cập nhật sau mỗi 100 lần học, dùng làm "đáp án mẫu". Nhờ đáp án đứng yên một lúc, việc học không bị chao đảo.
>
> Mạng ở đây rất nhỏ: lớp ẩn chỉ có 8 nơ-ron. Chi tiết này sẽ quan trọng ở phần sau.

**Về công thức `y = r + 0.9 · max Q_target`:** chỉ cần nói "điểm mục tiêu = điểm nhận ngay bây giờ, cộng điểm tốt nhất có thể có ở bước sau. Số 0.9 nghĩa là tương lai được tính nhẹ hơn hiện tại một chút".

**Nhớ 1 câu:** Mạng nơ-ron chấm điểm từng lựa chọn, học từ "sổ kinh nghiệm" ôn ngẫu nhiên.

**Chuyển:** "Đó là phần lý thuyết. Sau đây nhóm em trình bày cách chạy lại."

---

## Slide 5 — Cách chạy lại (1 phút)

**Lời nói:**
> Code gốc viết năm 2023. Nhóm chạy trên máy hiện tại và chỉ phải sửa **đúng 2 dòng**, vì thư viện PyTorch bản mới đổi cách nạp model đã lưu. Toàn bộ thuật toán, tham số và dữ liệu giữ nguyên.
>
> Nhóm train tổng cộng 48 lần trên 9 cấu hình khác nhau: pin to hoặc nhỏ, hiệu suất pin cao hoặc thấp, giá điện kiểu thị trường hoặc kiểu theo khung giờ. Mỗi lần train mất khoảng 15 phút.
>
> Để so cho chính xác, nhóm không ước lượng số của bài báo bằng mắt. Biểu đồ trong file PDF được lưu dạng vector, nên nhóm đọc toạ độ từng cột và đổi ra số euro chính xác.

**Nhớ 1 câu:** Chỉ sửa 2 dòng code, train 48 lần, số của bài báo đọc chính xác từ PDF.

**Chuyển:** "Câu hỏi đầu tiên: môi trường mô phỏng có chạy đúng không?"

---

## Slide 6 — Baseline khớp bài báo (45 giây)

**Lời nói:**
> Để kiểm tra, nhóm dùng hai chiến lược đơn giản làm mốc: một là **không dùng pin**, hai là **xoay vòng 4 lựa chọn** theo thứ tự. Hai chiến lược này không có gì ngẫu nhiên, nên nếu môi trường đúng thì phải ra đúng số của bài báo.
>
> Kết quả: ở cả 7 cấu hình, số của nhóm lệch bài báo **dưới 1 euro**. Vậy dữ liệu, cách mô phỏng pin và cách tính tiền đều đúng. Nếu có khác biệt thì chỉ nằm ở phần DQN.

**Nhớ 1 câu:** Baseline lệch dưới 1 €, nên môi trường mô phỏng đúng.

**Chuyển:** "Vậy còn DQN thì sao?"

---

## Slide 7 — Kết quả DQN (1 phút)

**Lời nói:**
> Bảng này so chi phí cả năm của bài báo với lần train tốt nhất của nhóm.
>
> Ba dòng tô màu là ba cấu hình nhóm đạt **gần như bằng bài báo, chỉ lệch 2 đến 4%**. Vậy con số trong bài là làm được thật.
>
> Nhưng cấu hình chính của bài báo, 730 euro, thì sau 12 lần train nhóm chỉ xuống được 980 euro.
>
> Nhìn cột cuối, "học được", sẽ thấy vấn đề: phần lớn các lần train **không học được gì**.

**Nhớ 1 câu:** Ba cấu hình đạt gần số bài báo, nhưng đa số lần train thất bại.

**Chuyển:** "Vì sao lại thất bại nhiều như vậy?"

---

## Slide 8 — Train bấp bênh (1 phút 30) ⭐ phát hiện chính

**Lời nói:**
> Trong 48 lần train, chỉ **12 lần** agent thật sự biết dùng pin. Ba phần tư còn lại thì agent chỉ làm đúng một việc lặp đi lặp lại: luôn xả pin. Pin lúc nào cũng gần rỗng, tiền điện gần bằng nhà không có pin.
>
> Nhóm tìm ra nguyên nhân bằng cách mở mạng nơ-ron ra xem. Hiện tượng này gọi là **dying ReLU**, tức "nơ-ron chết". Có thể hình dung mỗi nơ-ron như một bóng đèn. Nếu trong lúc học nó bị đẩy quá đà về phía âm, nó tắt hẳn và không bao giờ sáng lại.
>
> Mạng này chỉ có 8 nơ-ron ở lớp đầu. Khi cả 8 đều tắt, mạng cho cùng một kết quả với mọi tình huống, nên agent cứ chọn mãi một việc.
>
> Lý do dễ xảy ra: mạng quá nhỏ so với 1344 đầu vào, tốc độ học khá lớn, và điểm thưởng có giá trị lớn. Ngay cả model mà tác giả đưa kèm cũng chỉ còn 1 trên 8 nơ-ron sống.
>
> Một điểm hay nữa: khi cố định "hạt giống ngẫu nhiên", kết quả lặp lại y hệt. Một bạn trong nhóm chạy trên máy khác cũng ra **trùng từng chữ số**.

**Nhớ 1 câu:** Ba phần tư số lần train thất bại vì nơ-ron chết, mạng chỉ biết làm một việc.

**Chuyển:** "Có một dấu hiệu rất dễ nhận ra run bị chết."

---

## Slide 9 — Run chết ra cùng một con số (45 giây)

**Lời nói:**
> Các lần train bị chết cho ra **đúng cùng một con số**, dù khác hạt giống ngẫu nhiên, thậm chí khác cả dung lượng pin. Lý do: agent luôn xả nên pin luôn rỗng, pin to hay nhỏ cũng như nhau.
>
> Có một cái bẫy khi đọc kết quả. Với pin hiệu suất thấp (80%), chiến lược xoay vòng còn tệ hơn cả không dùng pin. Nên một run chết vẫn "thắng xoay vòng 11%", nhìn tưởng học tốt. Phải so với **cả hai** mốc mới thấy nó thật ra không làm gì.

**Nhớ 1 câu:** Run chết luôn ra cùng một số; phải so với cả hai mốc mới thấy.

**Chuyển:** "Trong lúc đọc code, nhóm còn thấy code không hoàn toàn giống bài báo."

---

## Slide 10 — Code khác bài báo (1 phút)

**Lời nói:**
> Nhóm tìm được 11 chỗ code khác bài báo. Bốn chỗ đáng kể nhất:
> - Phần thưởng "mua rẻ bán đắt" trong code **lớn gấp 10 lần** công thức trong bài.
> - Phần phạt khi pin quá đầy trong code nặng hơn nhiều so với bài ghi.
> - Code không cố định hạt giống ngẫu nhiên, nên mỗi lần train ra một kết quả khác. Chính README của tác giả cũng thừa nhận có thể phải train lại hơn 10 lần.
> - Một vài chi tiết khác: agent nhìn 7 loại thông tin chứ không phải 5, giá bán mặc định khác bài, và tên hai baseline bị đặt ngược.
>
> Hai chỗ đầu làm điểm thưởng to bất thường. Đây có thể chính là thứ làm nơ-ron chết ở slide trước.

**Nhớ 1 câu:** Code khác bài 11 chỗ, nhất là phần thưởng to hơn nhiều, góp phần gây nơ-ron chết.

**Chuyển:** "Tóm lại, nhóm rút ra được gì?"

---

## Slide 11 — Kết luận (45 giây)

**Lời nói:**
> Nhóm rút ra bốn điều:
> 1. Môi trường mô phỏng tái hiện đúng, và chỉ cần sửa 2 dòng code.
> 2. Kết quả của bài báo là làm được, nhưng đó là lần train tốt nhất sau nhiều lần thử.
> 3. Việc train rất bấp bênh, chỉ khoảng một phần tư thành công, do nơ-ron chết.
> 4. Nếu làm tiếp, nhóm sẽ thử loại nơ-ron không bị chết (LeakyReLU), mạng to hơn, học chậm hơn, và báo cáo kết quả trung bình nhiều lần thay vì chỉ lần tốt nhất.

**Nhớ 1 câu:** Phương pháp của bài đúng, nhưng con số tốt nhất phụ thuộc nhiều vào may mắn khi train.

---

## Slide 12 — Cảm ơn (10 giây)

**Lời nói:**
> Phần trình bày của nhóm em đến đây là hết. Toàn bộ code, kết quả và biểu đồ của mọi lần chạy đều có trên GitHub. Nhóm em cảm ơn thầy cô và các bạn đã lắng nghe, và rất mong nhận được câu hỏi.

---

## Từ điển nhanh (khi lỡ phải giải thích thêm)

| Thuật ngữ | Nói đơn giản |
|---|---|
| Học tăng cường (RL) | Máy tự thử, được thưởng/phạt, dần dần học cách làm tốt |
| Agent | "Người ra quyết định", ở đây là bộ điều khiển pin |
| State | Những gì agent nhìn thấy trước khi quyết định |
| Action | Việc agent được chọn làm |
| Reward | Điểm thưởng/phạt sau mỗi việc |
| Q-value | Điểm dự đoán "làm việc này thì về lâu dài được bao nhiêu" |
| ε-greedy | Thỉnh thoảng chọn bừa để khám phá, còn lại chọn việc điểm cao nhất |
| Replay buffer | Sổ ghi kinh nghiệm, lấy ngẫu nhiên ra ôn |
| Target net | Bản sao cập nhật chậm, làm "đáp án mẫu" cho ổn định |
| γ = 0.9 | Mức quan tâm tới tương lai; 0.9 ≈ nhìn xa khoảng 10 bước = 2.5 giờ |
| Dying ReLU | Nơ-ron tắt hẳn, không bao giờ sáng lại |
| Baseline | Chiến lược đơn giản dùng làm mốc so sánh |
| Seed | "Hạt giống ngẫu nhiên"; cố định nó thì chạy lại ra y hệt |
| RTP / TOU | Giá theo thị trường (đổi liên tục) / giá theo khung giờ (3 mức cố định) |
