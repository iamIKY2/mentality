# Nhạc cho màn hình hít thở thư giãn

Chép các file nhạc trực tiếp vào thư mục `music/` này (không tạo thư mục con).
Hỗ trợ nhận diện: `.mp3`, `.m4a`, `.aac`, `.wav`, `.ogg`, `.flac`.
Khả năng phát từng định dạng phụ thuộc thiết bị; nên dùng MP3 hoặc WAV.

Tên file được dùng làm tên bài hát trong danh sách. Không cần khai báo từng bài
trong mã nguồn hoặc pubspec.yaml. Ví dụ: `music/Tieng mua.mp3`.

Sau khi thêm, xóa hoặc đổi tên file, dừng ứng dụng và chạy/build lại bằng Flutter
để cập nhật tài nguyên. Nhạc được đóng gói cùng ứng dụng và phát offline;
thư mục này không phải thư mục Music trên điện thoại.

Trong màn hình hít thở, dùng nút phát/tạm dừng, dừng hẳn, bài trước/bài sau,
hoặc mở danh sách để chọn bài. Hết bài sẽ chuyển sang bài tiếp theo và lặp
danh sách. Nhạc dừng khi kết thúc phiên hoặc rời màn hình.
