import 'package:enigma/core/startup/runtime_diagnostics.dart';
import 'package:enigma/core/utils/storage.dart';
import 'package:enigma/screens/app_logs_screen.dart';
import 'package:enigma/screens/settings_screen.dart';
import 'package:enigma/state/auth_state.dart';
import 'package:enigma/state/theme_state.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUp(() => RuntimeDiagnostics.clear());

  testWidgets('live logs can be filtered, copied and cleared', (tester) async {
    RuntimeDiagnostics.lines.value = [
      '10:00 Storage: ready',
      '10:01 API request failed: status=500',
    ];
    String? copied;
    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(
      SystemChannels.platform,
      (call) async {
        if (call.method == 'Clipboard.setData') {
          copied = (call.arguments as Map)['text'] as String;
        }
        return null;
      },
    );
    addTearDown(() => tester.binding.defaultBinaryMessenger
        .setMockMethodCallHandler(SystemChannels.platform, null));

    await tester.pumpWidget(const MaterialApp(home: AppLogsScreen()));
    RuntimeDiagnostics.lines.value = [
      ...RuntimeDiagnostics.lines.value,
      '10:02 API connection restored',
    ];
    await tester.pump();
    expect(find.text('10:02 API connection restored'), findsOneWidget);
    expect(
      tester.getTopLeft(find.text('10:02 API connection restored')).dy,
      lessThan(tester
          .getTopLeft(find.text('10:01 API request failed: status=500'))
          .dy),
    );

    await tester.enterText(find.byType(TextField), 'API');
    await tester.pump();
    expect(find.text('10:00 Storage: ready'), findsNothing);
    await tester.tap(find.byTooltip('Sao chép log'));
    await tester.pump();
    expect(copied,
        '10:01 API request failed: status=500\n\n10:02 API connection restored');

    await tester.tap(find.byTooltip('Xóa nhật ký'));
    await tester.pump();
    expect(RuntimeDiagnostics.lines.value, isEmpty);
    expect(find.text('Chưa có nhật ký trong phiên này.'), findsOneWidget);
  });

  testWidgets('empty search does not copy unrelated entries', (tester) async {
    RuntimeDiagnostics.lines.value = ['Storage: ready'];
    await tester.pumpWidget(const MaterialApp(home: AppLogsScreen()));
    await tester.enterText(find.byType(TextField), 'not found');
    await tester.pump();
    expect(find.text('Không tìm thấy nhật ký phù hợp.'), findsOneWidget);
    expect(
        tester
            .widget<IconButton>(
                find.widgetWithIcon(IconButton, Icons.copy_rounded))
            .onPressed,
        isNull);
  });

  testWidgets('logs are accessible from settings', (tester) async {
    SharedPreferences.setMockInitialValues({});
    await StorageUtil.init();
    const authChannel = MethodChannel('plugins.flutter.io/local_auth');
    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(
      authChannel,
      (call) async =>
          call.method == 'getAvailableBiometrics' ? <String>[] : false,
    );
    addTearDown(() => tester.binding.defaultBinaryMessenger
        .setMockMethodCallHandler(authChannel, null));
    await tester.pumpWidget(MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthState()),
        ChangeNotifierProvider(create: (_) => ThemeState()),
      ],
      child: const MaterialApp(home: SettingsScreen()),
    ));
    await tester.pumpAndSettle();
    await tester.scrollUntilVisible(find.text('Nhật ký ứng dụng'), 300,
        scrollable: find.byType(Scrollable).first);
    await tester.tap(find.text('Nhật ký ứng dụng'));
    await tester.pumpAndSettle();
    expect(find.byType(AppLogsScreen), findsOneWidget);
    expect(find.text('Debug'), findsNothing);
  });
}
