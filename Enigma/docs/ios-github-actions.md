# Tạo IPA không ký bằng GitHub Actions từ Windows

Workflow: `.github/workflows/build.yml`.

## Chạy build

1. Đưa mã nguồn dự án và workflow lên kho GitHub, gồm `pubspec.lock`, assets
   và thư mục `ios/`. Workflow cần có trên nhánh mặc định để xuất hiện nút chạy.
2. Mở kho trên GitHub → **Actions** → **Build iOS Unsigned IPA**.
3. Chọn **Run workflow**, chọn nhánh cần build, rồi xác nhận chạy.
4. Mở lần chạy vừa tạo, chờ job **Build Enigma unsigned IPA** thành công.
5. Tại **Artifacts**, tải **Enigma-unsigned-ipa**. Giải nén file tải về để lấy
   **Enigma-unsigned.ipa**.

Không cần cấu hình GitHub Secrets, chứng chỉ ký hoặc Apple Developer cho
workflow này. Workflow chỉ chạy thủ công, không tự chạy khi push hay mở PR.
Artifact được giữ trong 7 ngày. Kiểm tra hạn mức Actions của tài khoản trước
khi chạy trên máy macOS.

## Cách hoạt động

Máy `macos-latest` cài Flutter `3.47.5` (khớp SDK local của dự án), lấy dependency,
chạy analyzer, tests, kiểm tra cấu hình và cài CocoaPods, sau đó chạy
`flutter build ios --release --no-codesign`, rồi đóng gói `Runner.app`
thành `Payload/Runner.app` trong IPA. Bước đóng gói giữ symlink và kiểm tra ZIP.

IPA chưa ký không cài trực tiếp được lên iPhone thông thường hoặc đưa thẳng lên
TestFlight/App Store. Có thể tải về để ký sau. Đây là bản cho thiết bị iOS,
không phải iOS Simulator.

Không cần dùng `codemagic.yaml` khi chạy workflow này.

## Kiểm tra màn hình trắng

Giữ bật **Enable application logs** khi chạy workflow để ghi log
khởi động vào device console và **Cài đặt → Thông tin ứng dụng → Nhật ký ứng dụng**.
Trang nhật ký cập nhật trực tiếp, có tìm kiếm, sao chép các mục đang lọc và xóa
nhật ký. Giữ tối đa 200 mục trong phiên hiện tại, mất khi tiến trình khởi động lại.
Không ghi nội dung request/response, URL, token hay mật khẩu vào trang này.
IPA vẫn là bản release; không có nút Debug nổi.

`ENIGMA_DIAGNOSTICS=true` chỉ bật ghi log; `main.dart` gọi `AppBootstrap` để
hiển thị giao diện trước khi chờ các dịch vụ. Workflow chạy kiểm thử
entry point thật ở cả cấu hình thông thường và cấu hình bật chẩn đoán.

Artifact **Enigma-ios-build-logs** chứa `ios-build.log` và `build-info.txt` (commit,
số lần build, trạng thái diagnostics). Số lần build cũng được dùng làm build
number và ghi trong log khởi động, để xác định bản IPA đang thử.

Log build thành công không cho biết lỗi lúc mở trên iPhone. Nếu bản đã nối
bootstrap vẫn trắng hoàn toàn, không có chữ Enigma, cần device console
hoặc crash log lúc mở app để kiểm tra native launch/engine/chữ ký. Không thể kết
luận nguyên nhân đó chỉ từ `ios-build.log`.

Chưa chạy build macOS thực tế trong workspace Windows; nếu build thất bại,
mở bước màu đỏ trong Actions để lấy log. Nếu báo không tìm thấy Flutter `3.47.5`,
cần kiểm tra SDK dịch vụ cung cấp và khả năng tương thích với yêu cầu Dart
`>=3.5.0 <4.0.0` cùng yêu cầu của các dependency trước khi đổi phiên bản.

Cấu hình bundle ID, Firebase, OAuth Google và quyền iOS được mô tả trong
[ios-setup.md](ios-setup.md).

Tài liệu:
- https://docs.github.com/en/actions/managing-workflow-runs-and-deployments/managing-workflow-runs/manually-running-a-workflow
- https://docs.github.com/en/actions/tutorials/store-and-share-data
- https://github.com/subosito/flutter-action
