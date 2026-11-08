import 'dart:async';
import 'dart:ui' show PlatformDispatcher;

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'core/utils/storage.dart';
import 'core/api/api_client.dart';
import 'core/services/push_notification_service.dart';
import 'core/services/reminder_service.dart';
import 'core/services/sync_service.dart';
import 'core/startup/app_bootstrap.dart';
import 'core/startup/runtime_diagnostics.dart';
import 'theme/app_theme.dart';
import 'app.dart';

/// Global navigator key để ApiClient có thể điều hướng về LoginScreen
/// khi refresh token hết hạn (không cần BuildContext).
final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  if (RuntimeDiagnostics.enabled) {
    FlutterError.onError = (details) {
      RuntimeDiagnostics.error(
          'Flutter error', details.exception, details.stack);
      FlutterError.presentError(details);
    };
    PlatformDispatcher.instance.onError = (error, stack) {
      RuntimeDiagnostics.error('Unhandled async error', error, stack);
      return false;
    };
  }
  RuntimeDiagnostics.log('Dart main entered');
  RuntimeDiagnostics.log(
    'Build ${const String.fromEnvironment('ENIGMA_BUILD_RUN', defaultValue: 'local')} '
    'commit ${const String.fromEnvironment('ENIGMA_BUILD_SHA', defaultValue: 'local')}',
  );

  // Khi sao lưu dữ liệu hoàn tất, tự động gửi thông báo đến thanh thông báo của điện thoại
  SyncService.instance.onSyncCompleted = (message) {
    PushNotificationService.showNotification(
      title: '☁️ Sao lưu dữ liệu thành công',
      body: message,
    );
  };

  // Kết nối callback: khi cả refresh token hết hạn → tự động về LoginScreen
  ApiClient.onUnauthorized = () {
    navigatorKey.currentState?.pushNamedAndRemoveUntil('/login', (_) => false);
  };

  SystemChrome.setSystemUIOverlayStyle(
    const SystemUiOverlayStyle(
      statusBarColor: Colors.transparent,
      statusBarIconBrightness: Brightness.light,
      systemNavigationBarColor: AppTheme.bgSurface,
      systemNavigationBarIconBrightness: Brightness.light,
    ),
  );

  // Render the startup screen before awaiting any platform plugin.
  runApp(AppBootstrap(
    initialize: () async {
      RuntimeDiagnostics.log('Storage: starting');
      await StorageUtil.init();
      RuntimeDiagnostics.log('Storage: ready; API: starting');
      ApiClient.init();
      RuntimeDiagnostics.log('API: ready');
    },
    builder: (_) => EnigmaApp(navigatorKey: navigatorKey),
    onReady: () {
      unawaited(_initializeOptionalService('Sync', SyncService.instance.init));
      unawaited(_initializeNotifications());
    },
  ));
}

Future<void> _initializeNotifications() async {
  await _initializeOptionalService('Push', PushNotificationService.init);
  await _initializeOptionalService('Reminders', ReminderService.init);
}

Future<void> _initializeOptionalService(
  String name,
  Future<void> Function() initialize,
) async {
  try {
    RuntimeDiagnostics.log('$name: starting');
    await initialize().timeout(const Duration(seconds: 15));
    RuntimeDiagnostics.log('$name: initialization returned');
  } catch (error, stack) {
    RuntimeDiagnostics.error('$name unavailable', error, stack);
    debugPrint('[Startup] $name unavailable: $error\n$stack');
  }
}
