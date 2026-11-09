# Tạo IPA không ký bằng GitHub Actions từ Windows

Workflow: `.github/workflows/ios-unsigned.yml`.

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
