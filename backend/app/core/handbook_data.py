"""
Kho dữ liệu Cẩm nang Thực tập Doanh nghiệp & KCN (Handbook Knowledge Base).
Chứa 20 chủ đề cẩm nang toàn diện về: ăn uống, đi lại, thuê trọ, ca kíp, sức khỏe, 
an toàn lao động, quyền lợi phụ cấp, tâm lý và kỹ năng thích nghi.
"""

HANDBOOK_ARTICLES = [
    {
        "id": "h1-food-trang-due",
        "title": "Mẹo ăn uống tiết kiệm và an toàn quanh KCN Tràng Duệ và An Dương",
        "category": "social",
        "summary": "Kinh nghiệm quán ăn bình dân, chợ chiều và dinh dưỡng cho sinh viên thực tập",
        "content": """Kinh nghiệm bỏ túi cho sinh viên thực tập tại KCN Tràng Duệ và khu vực An Dương, Hải Phòng:

1. Bữa trưa và bữa tối tại nhà máy:
- Tận dụng tối đa suất ăn ca miễn phí của nhà máy (thường có 3-4 món mặn, canh, rau xanh và hoa quả tráng miệng). Đồ ăn nhà máy luôn được kiểm nghiệm an toàn vệ sinh thực phẩm định kỳ.
- Nếu làm ca đêm, hãy nhớ nhận phiếu ăn đêm hoặc suất ăn nhẹ tại canteen lúc 00:00 - 01:00 để nạp năng lượng duy trì sự tỉnh táo.

2. Quán ăn bình dân chất lượng gần cổng khu công nghiệp:
- Quán Cơm Cô Hoa (gần Cổng 2 KCN): Cơm suất 25.000đ - 30.000đ, khẩu phần đầy đặn, cơm và canh xin thêm miễn phí.
- Chợ Chiều Tân Tiến: Họp từ 16:00 đến 19:00 hàng ngày, rau củ quả, thịt cá tươi rẻ hơn siêu thị khoảng 30%, rất thích hợp để mua về nấu chung cùng bạn trọ.
- Quán bún cá cay và phở đối diện cổng Ký túc xá: Ăn sáng nhanh từ 20.000đ - 25.000đ, phục vụ nhanh cho ca sáng 08:00.

3. Mẹo uống nước và bù khoáng trong phòng sạch:
- Trong phòng sạch (cleanroom) độ ẩm thường được duy trì ở mức thấp nên cơ thể rất dễ mất nước. Hãy uống 1 cốc nước ấm trước khi vào ca và tranh thủ bổ sung nước chanh muối hoặc dung dịch oresol vào giờ giải lao 10-15 phút giữa ca.
- Tránh uống nước đá lạnh liên tục sau khi tan ca vì dễ gây viêm họng và sốc nhiệt khi vừa ra khỏi môi trường điều hòa công nghiệp."""
    },
    {
        "id": "h2-ergonomics-back-neck",
        "title": "Xử lý đau mỏi vai gáy và thắt lưng do đứng chuyền liên tục",
        "category": "physical",
        "summary": "Tư thế đứng thao tác chuẩn và bài tập 3 phút giãn cơ chống mỏi lưng, vai gáy",
        "content": """Đứng thao tác lắp ráp tại line sản xuất 8-12 tiếng liên tục rất dễ dẫn đến căng cứng cơ cổ vai gáy, hội chứng ống cổ tay và thoái hóa thắt lưng:

1. Tư thế đứng chuẩn tại vị trí thao tác:
- Hai chân mở rộng bằng vai, trọng tâm cơ thể phân bổ đều, không khóa chặt khớp gối. Tránh dồn toàn bộ trọng lượng vào một chân quá lâu.
- Cứ mỗi 15-20 phút, hãy chủ động đổi chân trụ hoặc nhấc nhẹ gót chân lên xuống để kích hoạt van tĩnh mạch, giúp máu hồi lưu về tim tốt hơn.

2. Bài tập giãn cơ 3 phút trong giờ nghỉ giải lao:
- Động tác 1: Xoay tròn khớp cổ nhẹ nhàng theo chiều kim đồng hồ 5 vòng và ngược lại.
- Động tác 2: Nâng hai bả vai lên sát tai, giữ 3 giây rồi thở mạnh hạ vai xuống hoàn toàn.
- Động tác 3: Đan 10 ngón tay ra sau lưng, ưỡn ngực mở rộng khớp vai để giải tỏa áp lực đè nặng lên cột sống ngực.

3. Chăm sóc tại phòng trọ sau ca làm:
- Tắm nước ấm dưới vòi sen trực tiếp vào vùng gáy và thắt lưng trong 10 phút.
- Dùng cao dán giảm đau thảo dược hoặc xoa bóp dầu ngải cứu trước khi đi ngủ. Tuyệt đối không bẻ vặn cổ kêu răng rắc quá mạnh vì có thể làm tổn thương đĩa đệm cổ."""
    },
    {
        "id": "h3-esd-shoes-care",
        "title": "Bí quyết bảo vệ bàn chân khi mang giày bảo hộ ESD ca 12 tiếng",
        "category": "physical",
        "summary": "Kinh nghiệm chọn lót giày silicon, vớ cotton dày và mẹo ngâm chân giảm sưng phù",
        "content": """Giày bảo hộ chống tĩnh điện (ESD) có đế cứng và mũi bọc thép/composite, dễ gây phồng rộp da, đau nhức gan bàn chân và thâm móng chân:

1. Đầu tư miếng lót giày chuyên dụng:
- Thay miếng lót mỏng đi kèm giày bằng lót giày y tế Silicon hoặc Memory Foam có đệm vòm bàn chân (Arch Support). Điều này giúp phân bổ đều trọng lực và giảm tới 60% phản lực từ sàn bê tông/epoxy dội lên gót chân.

2. Chọn tất (vớ) bảo hộ phù hợp:
- Dùng tất cotton dày có đệm ở phần mũi và gót chân. Tuyệt đối tránh tất sợi nilon tổng hợp vì gây bí bách, giữ mồ hôi và dễ nhiễm nấm kẽ chân.
- Mang thêm một đôi tất sạch dự phòng trong balo để thay vào giữa ca nếu chân ra nhiều mồ hôi.

3. Phục hồi đôi chân sau ca làm:
- Ngâm chân nước ấm pha muối hột và gừng đập dập trong 15 phút trước khi đi ngủ để kích thích lưu thông máu và thư giãn các dây thần kinh bàn chân.
- Kê một chiếc gối cao dưới bắp chân khi nằm ngủ (chân cao hơn tim khoảng 15cm), giúp giảm phù nề và xua tan cảm giác nặng trĩu đôi chân vào sáng hôm sau."""
    },
    {
        "id": "h4-rights-ot-allowance",
        "title": "Quy định làm thêm giờ OT, phụ cấp ca đêm và quyền lợi hợp đồng thực tập",
        "category": "career",
        "summary": "Cách tính tiền lương làm thêm giờ 150%, 200%, 300% và quy chế bảo vệ thực tập sinh",
        "content": """Nắm chắc quyền lợi tài chính và quy chế làm thêm giờ theo Bộ luật Lao động và thỏa thuận thực tập:

1. Cách tính tiền lương làm thêm giờ (OT - Overtime):
- Ngày làm việc bình thường: Tiền làm thêm giờ được trả tối thiểu bằng 150% đơn giá tiền lương của ngày làm việc bình thường.
- Ngày nghỉ hằng tuần (Chủ nhật): Tiền làm thêm giờ tối thiểu bằng 200%.
- Ngày lễ, Tết hoặc ngày nghỉ có hưởng lương: Tiền làm thêm giờ tối thiểu bằng 300% chưa kể tiền lương ngày lễ.

2. Phụ cấp làm việc ca đêm (Khung giờ từ 22:00 đến 06:00 hôm sau):
- Người lao động làm việc ca đêm được trả thêm ít nhất 30% tiền lương tính theo đơn giá ngày bình thường.
- Nếu vừa làm ca đêm vừa làm thêm giờ OT đêm, sinh viên được cộng thêm 20% lương tính theo ca ngày tương ứng.

3. Giới hạn số giờ làm việc bảo vệ sức khỏe:
- Tổng số giờ làm thêm không được vượt quá 40 giờ trong 1 tháng và 200 giờ trong 1 năm.
- Công ty không được phép ép buộc thực tập sinh làm thêm giờ khi sinh viên có lý do sức khỏe hoặc kỳ thi tại trường. Mọi trường hợp ép ca sai quy định, sinh viên hãy báo ngay cho Giảng viên phụ trách đoàn thực tập."""
    },
    {
        "id": "h5-sleep-night-shift",
        "title": "Bí quyết cân bằng nhịp sinh học và giấc ngủ sâu khi chuyển đổi ca đêm",
        "category": "sleep",
        "summary": "Cách chống buồn ngủ lúc 3-4h sáng, chuẩn bị phòng ngủ ban ngày và điều hòa Melatonin",
        "content": """Chuyển đổi ca từ ca ngày (08:00 - 20:00) sang ca đêm (20:00 - 08:00) là thử thách lớn đối với đồng hồ sinh học của sinh viên:

1. Chống chọi cơn buồn ngủ lúc 03:00 - 04:00 sáng:
- Đây là khung giờ thân nhiệt cơ thể giảm xuống mức thấp nhất trong chu kỳ 24 giờ. Hãy đứng dậy đi rửa mặt bằng nước mát, nhai kẹo cao su bạc hà hoặc thực hiện vài động tác vươn vai khởi động nhẹ.
- Hạn chế uống cà phê đặc hoặc nước tăng lực sau 03:00 sáng vì chất caffeine tồn dư trong máu sẽ khiến bạn trằn trọc mất ngủ khi về phòng trọ lúc 09:00 sáng.

2. Chuẩn bị phòng ngủ ban ngày đạt chuẩn tối ưu:
- Lắp rèm cản sáng 100% hoặc đeo bịt mắt chất lượng tốt. Tuyệt đối không để ánh nắng mặt trời chiếu vào mắt vì ánh sáng tự nhiên sẽ ức chế não bộ tiết hormone ngủ Melatonin.
- Dùng nút bịt tai chống ồn (Earplugs) nếu phòng trọ gần đường lớn hoặc bạn cùng phòng sinh hoạt ca ngày.
- Bật quạt hoặc điều hòa giữ nhiệt độ phòng mát mẻ lý tưởng từ 24 - 26 độ C.

3. Đeo kính râm trên đường về phòng:
- Khi tan ca ca đêm buổi sáng, hãy đeo kính râm tối màu trên đường từ nhà máy về phòng trọ để đánh lừa não bộ rằng trời vẫn chưa sáng hẳn, giúp bạn dễ dàng đi vào giấc ngủ sâu hơn."""
    },
    {
        "id": "h6-rent-room-security",
        "title": "Kinh nghiệm thuê phòng trọ an ninh và chi phí hợp lý gần khu công nghiệp",
        "category": "social",
        "summary": "Tiêu chí chọn phòng trọ làm ca kíp, kiểm tra cách âm, giá điện nước và hợp đồng ngắn hạn",
        "content": """Hướng dẫn tìm phòng trọ an toàn, thuận tiện cho sinh viên thực tập tại các khu vực lân cận KCN:

1. Tiêu chí chọn phòng trọ cho người làm việc ca kíp:
- Ưu tiên khu trọ có giờ giấc mở cổng tự do hoặc có khóa vân tay riêng (để tiện đi làm ca đêm về lúc 08:30 sáng hoặc đi ca tối lúc 19:30).
- Kiểm tra độ cách âm của phòng: Gõ thử tường, kiểm tra cửa sổ có khít không, tránh các dãy trọ nằm sát mặt đường lớn có xe container và xe tải chạy liên tục ngày đêm.
- Hỏi kỹ đơn giá điện nước: Giá điện nên từ 2.500đ - 3.500đ/kWh, nước sạch từ 15.000đ - 20.000đ/m3 hoặc 60.000đ - 80.000đ/người/tháng.

2. Lưu ý về hợp đồng thuê phòng:
- Chỉ ký hợp đồng đúng thời hạn thực tập (thường từ 2 đến 4 tháng). Không nên ký hợp đồng dài hạn 1 năm nếu chưa chắc chắn ở lại làm chính thức sau tốt nghiệp để tránh bị phạt mất tiền cọc.
- Chụp ảnh lại hiện trạng phòng (tường, quạt, công tơ điện, khóa cửa, vòi nước) trước khi ký biên bản bàn giao phòng với chủ trọ."""
    },
    {
        "id": "h7-roommate-shift-rules",
        "title": "Quy tắc ứng xử và giải quyết mâu thuẫn phòng trọ khi lệch ca làm việc",
        "category": "social",
        "summary": "Quy ước giờ yên tĩnh, phân công việc nhà và cách ứng xử văn minh trong phòng trọ ghép",
        "content": """Khi ở ghép phòng trọ hoặc ký túc xá mà người làm ca ngày, người làm ca đêm:

1. Thống nhất quy ước phòng ngay từ ngày đầu tiên:
- Khung giờ yên tĩnh tuyệt đối: Ban ngày từ 09:00 đến 16:00 (giờ người làm ca đêm ngủ bù) và ban đêm từ 22:00 đến 06:00 (giờ người làm ca ngày ngủ).
- Trong khung giờ này: Bắt buộc đeo tai nghe khi xem điện thoại hoặc nghe nhạc; đóng mở cửa thật nhẹ nhàng; tắt đèn trần chính và chỉ dùng đèn ngủ cá nhân nhỏ.

2. Chia sẻ việc nhà và chi phí sinh hoạt công bằng:
- Phân công rõ lịch đổ rác, cọ rửa nhà vệ sinh theo tuần thay vì để dồn lại cuối tháng gây khó chịu cho nhau.
- Lập quỹ chung cho các vật dụng thiết yếu: Nước rửa chén, gia vị nấu nướng, xà phòng, giấy vệ sinh.
- Sử dụng các ứng dụng ghi chép chi tiêu chung để minh bạch từng khoản tiền phát sinh.

3. Giải quyết mâu thuẫn văn minh:
- Nếu có bất đồng về giờ giấc sinh hoạt, hãy trao đổi trực tiếp, nhẹ nhàng vào cuối tuần. Nếu không thể dung hòa, hãy chủ động liên hệ Ban quản lý ký túc xá hoặc Thầy Cô phụ trách đoàn thực tập để xin chuyển phòng sớm."""
    },
    {
        "id": "h8-5s-cleanroom-safety",
        "title": "Quy tắc 5S và an toàn tĩnh điện ESD trong phòng sạch công nghiệp",
        "category": "career",
        "summary": "Kỷ luật 5S tại line sản xuất, tiêu chuẩn chống tĩnh điện và thao tác phòng sạch",
        "content": """Môi trường sản xuất linh kiện điện tử, vi mạch và màn hình đòi hỏi kỷ luật phòng sạch (Cleanroom) khắt khe:

1. Quy tắc 5S căn bản tại trạm làm việc:
- Sàng lọc (Seiri): Loại bỏ ngay các bao bì, khay linh kiện lỗi hoặc phế phẩm ra khỏi bàn thao tác.
- Sắp xếp (Seiton): Dụng cụ (nhíp gắp, súng bắn vít, máy quét barcode) phải để đúng ô quy định và dán nhãn nhận diện.
- Sạch sẽ (Seiso): Lau sạch bụi bàn thao tác bằng khăn chống xước chuyên dụng trước và sau mỗi ca làm.
- Săn sóc (Seiketsu): Duy trì 3 tiêu chí trên thành thói quen kỷ luật mỗi ngày.
- Sẵn sàng (Shitsuke): Luôn tự giác tuân thủ nội quy an toàn lao động và bảo hộ cá nhân.

2. Tiêu chuẩn chống tĩnh điện (ESD):
- Luôn đeo vòng tay chống tĩnh điện (ESD wrist strap) và kẹp đúng vào đầu dây nối đất (grounding) khi chạm vào bo mạch điện tử.
- Tuyệt đối không mang vật dụng cá nhân sinh tĩnh điện cao (áo len, túi nilon bên ngoài, điện thoại) vào khu vực Cleanroom chưa được phép.
- Giày ESD phải được đo kiểm tra tại máy đo tĩnh điện cổng vào trước mỗi ca làm việc."""
    },
    {
        "id": "h9-box-breathing-stress",
        "title": "Kỹ thuật Hít thở Box Breathing 4-4-4-4 giảm căng thẳng và hoảng loạn tức thì",
        "category": "mental",
        "summary": "Phương pháp thở 4 thì giúp kích hoạt hệ phó giao cảm, hạ nhịp tim và ổn định tâm trí",
        "content": """Khi cảm thấy hoảng sợ, dồn dập hoặc kiệt sức trong ca thực tập do áp lực sản lượng hoặc máy báo lỗi:

1. Cơ chế sinh học của Box Breathing:
- Kỹ thuật hít thở 4 thì (Box Breathing) được áp dụng trong lực lượng đặc nhiệm Navy SEALs và y học tâm lý để kích hoạt hệ thần kinh phó giao cảm, hạ nhịp tim, giảm nồng độ cortisol trong máu chỉ sau 3-5 phút.

2. Các bước thực hiện chi tiết:
- Bước 1: Thở hết toàn bộ không khí ứ đọng ra khỏi đáy phổi qua miệng.
- Bước 2: Hít vào thật chậm rãi bằng mũi trong đúng 4 giây, cảm nhận bụng căng dần lên.
- Bước 3: Giữ nín thở trong lồng ngực trong 4 giây.
- Bước 4: Thở ra nhẹ nhàng, êm dịu qua miệng trong 4 giây, bụng xẹp xuống.
- Bước 5: Nín thở nghỉ trong 4 giây trước khi bắt đầu chu kỳ hít vào tiếp theo.

3. Khuyến nghị thực hành:
- Lặp lại từ 4 đến 6 chu kỳ mỗi khi bạn cảm thấy tim đập nhanh, bồn chồn lo âu hoặc trước các buổi họp giao ban ca quan trọng."""
    },
    {
        "id": "h10-leave-shift-swap",
        "title": "Quy trình xin nghỉ phép, đổi ca làm việc và xử lý khi bị ốm sốt đột xuất",
        "category": "career",
        "summary": "Các bước báo cáo xin nghỉ phép hợp lệ, đổi ca làm việc và thủ tục xác nhận y tế",
        "content": """Quy trình xin nghỉ và đổi ca nhằm đảm bảo tính kỷ luật và không làm gián đoạn dây chuyền sản xuất:

1. Quy trình xin nghỉ phép có kế hoạch trước:
- Báo cáo với Trưởng ca (Line Leader) và Quản lý bộ phận ít nhất trước 24 đến 48 giờ để kịp thời sắp xếp người thay thế line.
- Điền đầy đủ vào Đơn xin nghỉ phép theo mẫu của bộ phận nhân sự và xin chữ ký xác nhận của Leader.

2. Xử lý khi bị ốm đau, sốt hoặc sự cố gia đình đột xuất:
- Nhắn tin hoặc gọi điện trực tiếp cho Line Leader và Giáo viên phụ trách đoàn trước giờ vào ca ít nhất 2 tiếng.
- Đến khám tại Trạm Y tế công ty hoặc Trung tâm Y tế huyện để xin Giấy xác nhận khám chữa bệnh / Giấy nghỉ ốm hưởng BHXH để nộp bổ sung ngay khi đi làm trở lại.

3. Quy định về việc đổi ca làm việc giữa các thực tập sinh:
- Việc đổi ca (ví dụ đổi từ ca ngày sang ca đêm) chỉ được chấp thuận khi cả 2 bạn cùng thực tập ở cùng một vị trí công việc (cùng skill) và có sự phê duyệt trước bằng văn bản của Quản lý ca.
- Tuyệt đối không tự ý hoán đổi ca khi chưa có sự đồng ý của Leader vì hệ thống quẹt thẻ an ninh sẽ ghi nhận vi phạm phân công ca kíp."""
    },
    {
        "id": "h11-bus-transportation",
        "title": "Kinh nghiệm sử dụng xe buýt đưa đón nhân viên và văn hóa đi xe an toàn",
        "category": "social",
        "summary": "Lịch trình đón trả, quy tắc quẹt thẻ xe bus và văn hóa giao thông an toàn cho sinh viên",
        "content": """Xe buýt đưa đón là phương tiện di chuyển an toàn và tiết kiệm nhất cho sinh viên thực tập xa nhà:

1. Nắm chắc lộ trình và thời gian xe chạy:
- Mỗi tuyến xe buýt đều có bảng giờ xuất bến cố định cho ca ngày (thường đón lúc 06:30 - 07:00) và ca đêm (đón lúc 18:30 - 19:00).
- Hãy có mặt tại điểm đón trước giờ xe chạy ít nhất 10 phút. Xe buýt công nghiệp chạy theo lịch trình nghiêm ngặt và sẽ không chờ đợi cá nhân trễ giờ.

2. Quy tắc quẹt thẻ và nhận diện:
- Luôn đeo thẻ thực tập sinh hoặc thẻ xe buýt hợp lệ trên cổ khi bước lên xe để nhân viên kiểm soát thẻ đối chiếu.
- Nếu lỡ chuyến xe buýt của công ty, hãy báo ngay cho Leader và di chuyển bằng phương tiện cá nhân an toàn, tuyệt đối không phóng nhanh vượt ẩu trên quốc lộ.

3. Văn hóa đi xe buýt văn minh:
- Giữ trật tự, nói chuyện nhỏ nhẹ và đeo tai nghe khi nghe nhạc/xem video để không ảnh hưởng đến các anh chị công nhân đang tranh thủ ngủ bù trên xe.
- Giữ gìn vệ sinh chung, không mang đồ ăn có mùi nồng nặc lên xe và luôn thắt dây an toàn ở các ghế có trang bị."""
    },
    {
        "id": "h12-emergency-stop-safety",
        "title": "Hướng dẫn xử lý sự cố an toàn, nút dừng khẩn cấp E-Stop và cảnh báo máy",
        "category": "career",
        "summary": "Quy tắc an toàn máy móc, nhận biết cảnh báo lỗi và cách sử dụng nút Emergency Stop",
        "content": """An toàn lao động là ưu tiên số một trong mọi dây chuyền sản xuất công nghiệp:

1. Nguyên tắc vàng khi máy móc gặp sự cố hoặc kẹt linh kiện:
- Tuyệt đối KHÔNG tự ý đưa tay, que kim loại hoặc vật dụng vào buồng thao tác khi máy vẫn đang cấp điện hoặc đang hoạt động. Rất nhiều tai nạn lao động nghiêm trọng xảy ra do thói quen thò tay gỡ kẹt phôi.
- Khi máy phát ra tiếng kêu lạ, có mùi khét hoặc đèn tháp cảnh báo chuyển sang màu ĐỎ (Alarm): Hãy lùi lại khoảng cách an toàn và bấm nút Dừng Khẩn Cấp (Emergency Stop).

2. Cách sử dụng nút dừng khẩn cấp (E-Stop):
- Nút E-Stop thường có hình dạng cây nấm màu đỏ nổi bật trên nền vàng. Khi nhấn dứt khoát vào nút, toàn bộ nguồn động lực của cơ cấu máy sẽ bị ngắt tức thì.
- Sau khi nhấn E-Stop, hãy giơ tay báo hiệu và gọi ngay Kỹ sư bảo trì (Maintenance) hoặc Line Leader đến xử lý, không tự ý xoay nút để reset máy khi chưa rõ nguyên nhân.

3. Lối thoát hiểm và quy định phòng cháy chữa cháy:
- Ghi nhớ vị trí của 2 lối thoát hiểm gần nhất tại xưởng làm việc của bạn.
- Khi có còi báo động cháy sơ tán: Giữ bình tĩnh, đi theo hàng lối có biển EXIT chỉ dẫn, không chen lấn, xô đẩy hoặc quay lại lấy tư trang cá nhân."""
    },
    {
        "id": "h13-first-aid-exhaustion",
        "title": "Kinh nghiệm sơ cứu nhanh kiệt sức do nhiệt, tụt đường huyết và say nắng",
        "category": "physical",
        "summary": "Dấu hiệu nhận biết tụt huyết áp, hoa mắt chóng mặt và các bước sơ cứu bước đầu",
        "content": """Làm việc đứng ca dài trong điều kiện tập trung cao độ dễ dẫn đến hạ đường huyết hoặc kiệt sức:

1. Dấu hiệu nhận biết sớm cơ thể đang phát tín hiệu cầu cứu:
- Cảm giác hoa mắt, vã mồ hôi lạnh ở trán và lòng bàn tay, run tay chân, tim đập nhanh hồi hộp, cảm giác choáng váng muốn ngã gục.

2. Các bước xử lý sơ cứu tức thì:
- Bước 1: Ngay lập tức ngồi thụp xuống hoặc ngồi bệt xuống sàn, tựa lưng vào tường để tránh bị ngã đập đầu gây chấn thương sọ não nếu ngất xỉu.
- Bước 2: Báo hiệu cho bạn làm cùng line hoặc Leader gần nhất hỗ trợ: "Em bị tụt huyết áp/chóng mặt quá".
- Bước 3: Nới lỏng cổ áo, tháo khẩu trang và cởi áo khoác bảo hộ ngoài để cơ thể dễ hô hấp.
- Bước 4: Uống một cốc nước đường ấm, nước gừng hoặc ăn ngay 1-2 chiếc kẹo ngọt có sẵn trong túi.

3. Chăm sóc tại phòng y tế:
- Sau khi qua cơn choáng ban đầu, hãy để đồng nghiệp dìu vào Trạm Y tế công ty để bác sĩ đo huyết áp, kiểm tra nhịp tim và nằm nghỉ ngơi theo dõi ít nhất 30-45 phút."""
    },
    {
        "id": "h14-workplace-communication",
        "title": "Cách giao tiếp hiệu quả và báo cáo sự cố với Line Leader, Mentor và quản lý ca",
        "category": "social",
        "summary": "Nguyên tắc báo cáo 5W1H, văn hóa ứng xử nơi công xưởng và cách đặt câu hỏi thông minh",
        "content": """Kỹ năng giao tiếp quyết định 50% sự thành công và đánh giá xếp loại trong kỳ thực tập doanh nghiệp:

1. Văn hóa chào hỏi và tác phong công nghiệp:
- Luôn chủ động chào hỏi Line Leader, các anh chị công nhân kỹ thuật lâu năm đầu ca và cảm ơn khi tan ca. Thái độ lễ phép, cầu thị sẽ giúp bạn nhận được sự chỉ bảo tận tình từ những người đi trước.
- Luôn mang theo một cuốn sổ tay nhỏ và bút trong túi áo để ghi chép lại các hướng dẫn, mã lỗi hoặc quy trình thao tác chuẩn (SOP).

2. Nguyên tắc báo cáo sự cố theo công thức 5W1H ngắn gọn:
- What: Sự cố gì đang xảy ra? (Ví dụ: Máy dán barcode bị kẹt linh kiện).
- Where: Tại vị trí nào? (Tại line Module số 3).
- When: Từ thời điểm nào? (Khoảng 10 phút trước).
- Who: Ai đang phụ trách? (Em và bạn Nam đang thao tác).
- How / Action: Đã thực hiện thao tác gì ban đầu? (Em đã bấm nút tạm dừng và xin ý kiến anh Leader hướng dẫn xử lý).

3. Cách đặt câu hỏi khi chưa hiểu rõ thao tác:
- Thà hỏi lại 2-3 lần để làm đúng còn hơn làm ẩu gây lỗi hàng loạt (NG hàng loạt). Hãy nói: "Anh/Chị ơi, thao tác này em chưa chắc chắn lắm, nhờ Anh/Chị làm mẫu lại giúp em một lần được không ạ?"."""
    },
    {
        "id": "h15-mindset-non-major",
        "title": "Tâm thế thích ứng khi làm việc trái ngành tại nhà máy sản xuất",
        "category": "career",
        "summary": "Cách tìm kiếm giá trị, rèn luyện tư duy quản lý chất lượng và làm giàu hồ sơ xin việc",
        "content": """Rất nhiều sinh viên cảm thấy hụt hẫng và sốc khi công việc thực tế tại nhà máy mang tính vận hành dây chuyền, khác xa với lý thuyết chuyên ngành đại học:

1. Chuyển dịch góc nhìn từ 'thợ bấm máy' sang 'người quan sát hệ thống':
- Dù bạn đang đứng ở vị trí thao tác lắp ráp cơ bản, hãy chú ý quan sát cách nhà máy vận hành chuỗi cung ứng, cách họ kiểm soát chất lượng lỗi (QA/QC), cách bố trí mặt bằng sản xuất tinh gọn (Lean Manufacturing) và quy trình giao ca giữa các tổ đội.
- Đây là những kiến thức thực tế vô giá mà không một cuốn giáo trình đại học nào có thể mô tả chi tiết được.

2. Rèn luyện sức bền và tác phong công nghiệp:
- Khả năng làm việc đúng giờ giấc tuyệt đối, sự tập trung cao độ trong môi trường áp lực và tinh thần làm việc nhóm là những kỹ năng mềm hàng đầu mà mọi tập đoàn đa quốc gia đều tìm kiếm ở ứng viên mới ra trường.

3. Biến kỳ thực tập thành điểm tựa vững chắc trong CV:
- Khi viết CV xin việc sau này, đừng chỉ ghi "công nhân lắp ráp". Hãy viết: "Thực tập sinh vận hành dây chuyền công nghệ cao, nắm vững tiêu chuẩn 5S, kỷ luật phòng sạch ESD và đóng góp vào mục tiêu đạt 99.5% tỷ lệ sản phẩm đạt chuẩn của chuyền"."""
    },
    {
        "id": "h16-internship-report-guide",
        "title": "Hướng dẫn viết nhật ký thực tập và hoàn thành báo cáo tốt nghiệp đạt điểm cao",
        "category": "career",
        "summary": "Cách thu thập số liệu thực tế, cấu trúc báo cáo chuẩn và xin xác nhận của đơn vị thực tập",
        "content": """Báo cáo thực tập là căn cứ quan trọng nhất để Nhà trường đánh giá và cho điểm kỳ thực tập tốt nghiệp:

1. Thói quen ghi chép nhật ký thực tập mỗi ngày:
- Dành ra 5 phút cuối mỗi ca làm việc để ghi lại: Ngày làm việc, công việc cụ thể được giao, bài học kinh nghiệm rút ra, khó khăn gặp phải và cách giải quyết.
- Việc ghi chép đều đặn sẽ giúp bạn không bị "trống rỗng" dữ liệu khi đến tuần cuối cùng phải viết báo cáo tổng kết 40-50 trang.

2. Cấu trúc chuẩn của một báo cáo thực tập đạt điểm giỏi:
- Phần 1: Giới thiệu tổng quan về Doanh nghiệp (Lịch sử hình thành, cơ cấu tổ chức, sơ đồ các phòng ban, sản phẩm chủ lực).
- Phần 2: Nội dung công việc thực tế được phân công tại xưởng/bộ phận.
- Phần 3: Phân tích quy trình công nghệ, các vấn đề tồn tại và đề xuất giải pháp cải tiến (Kaizen).
- Phần 4: Bài học kinh nghiệm cá nhân và định hướng nghề nghiệp sau khi tốt nghiệp.

3. Thủ tục xin nhận xét và dấu mộc của doanh nghiệp:
- Hoàn thành bản nháp báo cáo trước ngày kết thúc kỳ thực tập ít nhất 1 tuần để gửi Anh/Chị Mentor duyệt.
- Nộp Phiếu đánh giá thực tập sinh có điểm số và nhận xét chi tiết kèm chữ ký của Quản lý bộ phận và dấu mộc tròn của công ty."""
    },
    {
        "id": "h17-insurance-benefits",
        "title": "Chính sách bảo hiểm y tế, bảo hiểm tai nạn lao động cho thực tập sinh",
        "category": "career",
        "summary": "Quyền lợi khám chữa bệnh BHYT, quy trình giám định tai nạn lao động tại nhà máy",
        "content": """Tìm hiểu chế độ bảo hiểm giúp sinh viên được bảo vệ quyền lợi tối đa khi gặp sự cố sức khỏe:

1. Thẻ Bảo hiểm Y tế (BHYT) sinh viên:
- Thẻ BHYT sinh viên do Nhà trường cấp có giá trị sử dụng trên toàn quốc. Khi đi thực tập xa trường, bạn hoàn toàn có thể sử dụng thẻ BHYT (hoặc ứng dụng VssID / VNeID) để khám chữa bệnh tại các bệnh viện tuyến huyện/tỉnh nơi nhà máy đóng quân.
- Trường hợp cấp cứu: Được hưởng 100% quyền lợi BHYT tại bất kỳ cơ sở y tế nào trên toàn quốc.

2. Bảo hiểm tai nạn lao động tại doanh nghiệp:
- Các doanh nghiệp uy tín đều mua bảo hiểm tai nạn lao động (bảo hiểm 24/7) cho sinh viên thực tập trong suốt thời gian diễn ra kỳ thực tập.
- Nếu không may xảy ra sự cố va quệt, chấn thương trong giờ làm việc hoặc trên tuyến đường đi làm: Hãy thông báo ngay cho Leader để lập Biên bản sự cố tai nạn lao động, làm căn cứ chi trả viện phí và bồi thường theo đúng thỏa thuận hợp đồng."""
    },
    {
        "id": "h18-financial-management",
        "title": "Kỹ năng quản lý tài chính và chi tiêu thông minh với tiền phụ cấp thực tập",
        "category": "social",
        "summary": "Quy tắc phân bổ 50/30/20, xây dựng quỹ dự phòng và cảnh báo bẫy tín dụng đen",
        "content": """Khoản tiền phụ cấp hàng tháng là thành quả lao động đầu đời, cần được quản lý một cách khoa học:

1. Công thức phân bổ ngân sách 50/30/20:
- 50% cho nhu cầu thiết yếu: Tiền thuê phòng trọ, điện nước, ăn uống sinh hoạt cá nhân ngoài giờ làm việc.
- 30% cho tiết kiệm và quỹ dự phòng khẩn cấp: Để dành phòng khi ốm đau, sửa xe hoặc chi phí mua sắm đồ dùng học tập khi quay lại trường.
- 20% cho chi tiêu linh hoạt: Mua sắm quần áo ấm, liên hoan cùng bạn bè trọ hoặc gửi quà về biếu bố mẹ.

2. Cảnh giác với các bẫy tài chính xung quanh khu công nghiệp:
- Quanh các KCN thường có rất nhiều tờ rơi, biển quảng cáo cho vay tiền nhanh qua app, vay tiền chỉ cần căn cước công dân hoặc cắm thẻ sinh viên với lãi suất "cắt cổ".
- Tuyệt đối KHÔNG sa vào vay nóng, không tham gia cá độ đỏ đen hoặc các sàn đầu tư tài chính ảo trên mạng để tránh để lại hậu quả khôn lường cho bản thân và gia đình."""
    },
    {
        "id": "h19-noise-pressure-adaptation",
        "title": "Mẹo thích nghi với tiếng ồn còi báo và môi trường áp lực cao trong xưởng",
        "category": "physical",
        "summary": "Cách sử dụng nút tai chống ồn công nghiệp và bài tập thư giãn mắt khi kiểm tra ngoại quan",
        "content": """Môi trường nhà máy với tiếng động cơ, tiếng còi báo động và đèn huỳnh quang liên tục dễ gây căng thẳng giác quan:

1. Bảo vệ thính giác trước tiếng ồn công nghiệp:
- Trang bị nút bịt tai giảm ồn chất lượng cao (loại bọt xốp hoặc silicon đạt chuẩn NRR 25-30dB). Khi nhét đúng cách, nút tai sẽ giảm thiểu các tần số âm thanh gây hại nhưng vẫn cho phép bạn nghe được tiếng nhắc nhở của đồng nghiệp và còi báo động khẩn cấp.
- Vệ sinh hoặc thay mới nút bịt tai định kỳ để tránh nguy cơ viêm tai giữa do mồ hôi và bụi bẩn.

2. Thư giãn thị giác khi làm vị trí kiểm tra ngoại quan (Visual Inspection):
- Việc nhìn chăm chú vào các chi tiết vi mạch nhỏ hoặc soi kính hiển vi liên tục dễ gây khô mắt, nhức mỏi và mờ mắt tạm thời.
- Áp dụng quy tắc 20-20-20: Cứ mỗi 20 phút tập trung, hãy chớp mắt nhìn ra một điểm xa 20 feet (khoảng 6 mét) trong 20 giây để cơ thể điều tiết mắt trở lại trạng thái thư giãn.
- Luôn mang theo một lọ nước mắt nhân tạo (nước muối sinh lý 0.9%) để nhỏ mắt khi cảm thấy cộm xót."""
    },
    {
        "id": "h20-phq4-mental-screening",
        "title": "Thang đo Y khoa PHQ-4: Sàng lọc nhanh trầm cảm và lo âu cho sinh viên ca kíp",
        "category": "mental",
        "summary": "Bộ công cụ 4 câu hỏi chuẩn hóa y khoa giúp nhận biết sớm quá tải tâm lý và cách phục hồi",
        "content": """Nghiên cứu Y học Lao động quốc tế PMC8038412 xác nhận hiệu quả của thang đo PHQ-4 trong việc phát hiện sớm quá tải cảm xúc:

1. Ý nghĩa của bộ lọc PHQ-4 trong ứng dụng Enigma:
- Gồm 4 câu hỏi ngắn đánh giá cảm xúc trong 14 ngày qua: 2 câu về Lo âu (GAD-2) và 2 câu về Trầm cảm (PHQ-2).
- Mất chưa đầy 60 giây để thực hiện nhưng cung cấp bức tranh trung thực về sức khỏe tinh thần của bạn sau những ca làm việc căng thẳng.

2. Hướng dẫn đọc kết quả phân tầng:
- Điểm 0 - 2 (Bình thường): Áp lực thích nghi thông thường, cơ thể và tâm trí bạn đang làm quen tốt với nhịp sống nhà máy.
- Điểm 3 - 5 (Căng thẳng nhẹ): Bạn đang bắt đầu mệt mỏi, hãy ngủ đủ 7-8 tiếng, ngâm chân nước ấm và tập thở 4-4-4-4 mỗi ngày.
- Điểm 6 - 8 (Căng thẳng vừa): Hãy chia sẻ với Anh/Chị Mentor hoặc Giảng viên phụ trách, đề xuất giảm bớt ca tăng ca (OT).
- Điểm 9 - 12 (Nguy cơ cao): Cần liên hệ ngay với Phòng Y tế hoặc chuyên gia tâm lý học đường để được tham vấn chuyên sâu và hỗ trợ kịp thời."""
    }
]

