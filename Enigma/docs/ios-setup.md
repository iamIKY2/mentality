# Cấu hình và kiểm tra build iOS

Dự án dùng Flutter 3.47.5, iOS 15.0 trở lên và CocoaPods. Swift Package Manager
được tắt riêng cho dự án trong `pubspec.yaml` để các plugin native đang ghim
được liên kết thống nhất bằng Podfile. Không cần thay cấu hình Flutter toàn máy.

## Build trên macOS

```bash
flutter pub get
flutter analyze --no-pub
flutter test --no-pub
cd ios
pod install --repo-update
cd ..
flutter build ios --release --no-codesign
```

Mở `ios/Runner.xcworkspace` khi dùng Xcode. Giữ `ios/Podfile.lock` trong kho mã
nguồn sau lần cài pods thành công đầu tiên. Không sao chép `Generated.xcconfig`,
`Flutter/ephemeral` hoặc Pods từ Windows sang máy build; Flutter tạo lại chúng.

GitHub Actions và Codemagic đã có bước analyze, test, kiểm tra plist/Podfile,
cài pods và build release. Xem [GitHub Actions](ios-github-actions.md) hoặc
[Codemagic](ios-unsigned-build.md) để tải IPA chưa ký.

## Bundle ID và Firebase

Runner và RunnerTests đã dùng tiền tố `com.enigmadevteam.enigma`, khớp
`iosBundleId` đang có trong `lib/firebase_options.dart`. Bundle ID iOS trước đây
là `com.enigma.enigmateam.enigma`; cần dùng App ID và provisioning profile
tương ứng với ID mới khi ký. Android giữ bundle ID hiện có.

Cần đối chiếu Firebase Console để bảo đảm các giá trị iOS đã có trong
`firebase_options.dart` thuộc đúng ứng dụng này. Nếu Firebase đang đăng ký ID
khác, đăng ký ứng dụng iOS phù hợp và chạy lại `flutterfire configure` với dự án
`enigma-mentality` thay vì tự sửa app ID/API key.

Ứng dụng đã khai báo mô tả quyền Face ID, vị trí khi sử dụng và background mode
`remote-notification`. Geolocator được biên dịch với
`BYPASS_PERMISSION_LOCATION_ALWAYS=1`: ứng dụng chỉ cần vị trí khi đang mở.

Để nhận push trên iPhone thật, chọn Team trong Xcode, bật Push Notifications
cho App ID/provisioning profile và tải APNs key lên Firebase Cloud Messaging.
Runner dùng `Runner.entitlements` với môi trường APNs development cho Debug,
production cho Release/Profile. IPA chưa ký không dùng để kiểm tra APNs.

## Đăng nhập Google trên iOS

Kho hiện chưa có OAuth client iOS và callback URL scheme. Build vẫn thực hiện
được; khi thiếu cấu hình, ứng dụng hiển thị thông báo và cho phép đăng nhập
bằng email hoặc dùng chế độ khách, tránh gọi Google SDK với cấu hình thiếu.

Để bật Google Sign-In:

1. Tạo OAuth client loại **iOS** cho bundle ID `com.enigmadevteam.enigma` và bật
   Google Sign-In trong dự án Firebase tương ứng.
2. Lấy `CLIENT_ID` và `REVERSED_CLIENT_ID` từ cấu hình Firebase/OAuth thực tế.
3. Trong `ios/Runner/Info.plist`, thêm `GIDClientID` có giá trị `CLIENT_ID`.
   Thêm `CFBundleURLTypes` là array chứa một dict có `CFBundleTypeRole` là
   `Editor`, và `CFBundleURLSchemes` là array chứa `REVERSED_CLIENT_ID`.
4. Giữ Web/server client ID trong `AppConstants.googleServerClientId` khớp với
   client ID mà backend xác thực. Không dùng Web client ID thay cho iOS client.
5. Build lại và thử đăng nhập, hủy đăng nhập, quay lại từ Google trên iPhone.

Hướng dẫn plugin: [google_sign_in_ios](https://pub.dev/packages/google_sign_in_ios).

## Phạm vi xác minh

Workspace Windows chạy được analyzer và Flutter tests (kể cả UI variant iOS),
nhưng không có Xcode/CocoaPods để biên dịch Swift, cài pods hoặc tạo IPA iOS.
Chỉ khi workflow macOS hoặc Xcode build thành công mới xác nhận được bản build
native. Cần thử Face ID, quyền vị trí, thông báo và Google trên thiết bị thật
sau khi cấu hình tài khoản dịch vụ và ký ứng dụng.
