import 'package:enigma/state/auth_state.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('iOS without OAuth configuration stops before calling Google SDK', () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.iOS;
    const channel = MethodChannel('enigma/ios_configuration');
    const googleChannel = MethodChannel('plugins.flutter.io/google_sign_in');
    final messenger = TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger;
    var configurationChecks = 0;
    final googleCalls = <String>[];
    messenger.setMockMethodCallHandler(channel, (call) async {
      expect(call.method, 'isGoogleSignInConfigured');
      configurationChecks++;
      return false;
    });
    messenger.setMockMethodCallHandler(googleChannel, (call) async {
      googleCalls.add(call.method);
      return null;
    });
    final auth = AuthState();
    addTearDown(() {
      debugDefaultTargetPlatformOverride = null;
      messenger.setMockMethodCallHandler(channel, null);
      messenger.setMockMethodCallHandler(googleChannel, null);
      auth.dispose();
    });

    expect(await auth.loginWithGoogle(), isFalse);
    expect(auth.isLoading, isFalse);
    expect(auth.isAuthenticated, isFalse);
    expect(auth.error, contains('chưa được cấu hình trên iOS'));
    expect(configurationChecks, 1);
    expect(googleCalls, isEmpty);
  });
}
