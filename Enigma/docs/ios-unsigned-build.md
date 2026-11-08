# Tạo IPA không ký từ Windows bằng Codemagic

Workflow `ios-unsigned` trong `codemagic.yaml` chạy trên máy macOS của Codemagic.
Không cần Apple Developer, chứng chỉ ký hay provisioning profile cho workflow này.

## Cách chạy

1. Đưa dự án vào kho Git riêng trên GitHub, GitLab hoặc Bitbucket. Thêm
   `codemagic.yaml`, mã nguồn Flutter, `pubspec.lock`, assets và thư mục `ios/`.
   Không đưa `.env`, khóa API bí mật, thư mục `backend/venv/`, `build/` hoặc
   thông tin ký ứng dụng lên kho mã nguồn.
2. Đăng nhập https://codemagic.io và thêm ứng dụng từ kho mã nguồn đó.
3. Chọn cấu hình bằng `codemagic.yaml` và workflow **Enigma iOS - Unsigned IPA**.
4. Chọn nhánh chứa cấu hình rồi bắt đầu build.
5. Khi thành công, tải **Enigma-unsigned.ipa** trong phần **Artifacts** của build.

Workflow được chạy thủ công, không tự build khi push. Kiểm tra hạn mức và chi phí
của tài khoản Codemagic trước khi bắt đầu.

## File được tạo

Lệnh `flutter build ios --release --no-codesign` tạo `Runner.app` cho thiết bị iOS.
Workflow đặt ứng dụng vào `Payload/Runner.app` và nén thành
`build/ios/ipa/Enigma-unsigned.ipa`. Bước cuối kiểm tra cấu trúc ZIP của file.

Đây là IPA chưa ký: không cài trực tiếp lên iPhone thông thường và không tải
thẳng lên TestFlight/App Store. Có thể giữ file để ký bằng công cụ khác sau này.
Đây cũng không phải bản chạy trên iOS Simulator.

## Môi trường build

- Flutter `3.47.5`, khớp SDK local của dự án (Dart `3.13.4`).
- Máy `mac_mini_m2`, Xcode mới nhất do Codemagic cung cấp.
- Dự án dùng CocoaPods, có sẵn `ios/Podfile` và tắt Swift Package Manager riêng
  trong `pubspec.yaml`. Workflow tự chạy `pod install --repo-update`.
- Cấu hình Firebase, Google và ký ứng dụng: xem [ios-setup.md](ios-setup.md).

Chưa có build macOS thực tế được chạy từ workspace Windows này. Nếu dịch vụ
không cung cấp phiên bản SDK đã ghim hoặc build báo lỗi plugin/Xcode, cần xem log
build để điều chỉnh; không hạ yêu cầu Dart trong `pubspec.yaml` chỉ để bỏ qua lỗi.

Tài liệu:
- https://docs.codemagic.io/yaml-quick-start/building-a-flutter-app/
- https://docs.codemagic.io/yaml-basic-configuration/yaml-getting-started/
