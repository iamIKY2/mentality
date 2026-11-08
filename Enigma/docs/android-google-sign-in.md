# Sửa Google Sign-In: ApiException 10 trên Android

Mã 10 là `DEVELOPER_ERROR`: Google phát hiện cấu hình ứng dụng không hợp lệ.
Kiểm tra bộ ba package name, SHA-1 của chứng chỉ ký bản đang cài và OAuth project.

## Kết quả kiểm tra tại workspace

- Android application ID: `com.enigma.enigmateam.enigma`.
- Firebase project: `enigma-mentality` (project number `36729513984`).
- Android Firebase app ID đúng package trong `google-services.json`:
  `1:36729513984:android:826c356fca005577b8d0e5`.
- `lib/firebase_options.dart` đã được sửa để dùng app ID này; trước đó dùng app
  của package `com.enigmadevteam.enigma`.
- Web/server client ID trong Flutter khớp client loại 3 trong JSON và giá trị
  mặc định của backend. Giữ `serverClientId` là client loại Web.
- SHA-1 OAuth Android trong JSON hiện tại:
  `72:32:51:FF:B5:1C:EF:6E:04:43:1C:DE:92:E5:DB:96:DF:C0:42:08`.
- SHA-1 của debug keystore trên máy này **và APK hiện có** tại
  `build/app/outputs/flutter-apk/app-debug.apk`:
  `AE:9C:DD:31:39:09:9E:38:E3:B3:FC:CD:3C:95:31:FA:DF:39:39:B1`.
- SHA-256 của cùng chứng chỉ:
  `3B:7A:30:B5:B7:5F:65:48:50:EC:96:62:57:FD:9D:AF:71:AD:B8:CB:E2:04:C0:15:06:DC:7C:2B:41:1D:F3:CA`.

Hai SHA-1 đang khác nhau. JSON có thể cũ; cần kiểm tra cấu hình thực tế trên
Console. Chứng chỉ của APK đang cài trên điện thoại có thể khác APK local này.
Gradle hiện ký cả debug và release bằng debug key của máy build.

## Thao tác cần làm trên Console

1. Mở Firebase Console → dự án **enigma-mentality** → Project settings → Your
   apps → chọn Android app có package **com.enigma.enigmateam.enigma**.
2. Trong SHA certificate fingerprints, thêm SHA-1 và SHA-256 của APK nêu trên.
   Giữ các fingerprint đang dùng cho những máy hoặc bản phát hành khác.
3. Nếu dùng Firebase Authentication, kiểm tra Sign-in method → Google đã bật.
4. Trong Google Cloud Console của cùng dự án → Google Auth Platform → Clients
   (hoặc APIs & Services → Credentials), kiểm tra có OAuth client loại Android
   cho đúng package và SHA-1 mới. Nếu chưa có, tạo client Android tương ứng.
5. Tải lại `google-services.json`, thay file `android/app/google-services.json`.
   File mới cần có Android OAuth client cho SHA-1 mới và Web client loại 3.
6. Build lại rồi thử đăng nhập trên điện thoại:

   ```bash
   flutter pub get
   flutter run
   ```

Nếu cài từ Google Play, dùng SHA-1 **App signing key certificate** trong Play
Console → App integrity/App signing, không chỉ SHA của upload key. Nếu APK được
build trên máy/CI khác, lấy fingerprint của đúng APK đó. Không chỉnh certificate
hash trong JSON bằng tay: thao tác đó không đăng ký chứng chỉ với Google.

Không cần thêm Google Services Gradle plugin chỉ để xử lý mã 10 trong luồng
hiện tại: Flutter đã truyền Web client ID trực tiếp và khởi tạo Firebase bằng
`FirebaseOptions`. Đăng ký OAuth trên Console mới là bước cần thiết khi SHA sai.

Tài liệu chính thức:

- [Google: DEVELOPER_ERROR = 10](https://developers.google.com/android/reference/com/google/android/gms/common/api/CommonStatusCodes#DEVELOPER_ERROR)
- [Firebase: Google Sign-In trên Android](https://firebase.google.com/docs/auth/android/google-signin)
