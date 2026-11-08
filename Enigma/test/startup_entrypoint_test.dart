import 'dart:async';
import 'dart:ui' show PlatformDispatcher;

import 'package:enigma/app.dart';
import 'package:enigma/core/startup/app_bootstrap.dart';
import 'package:enigma/core/startup/runtime_diagnostics.dart';
import 'package:enigma/core/utils/storage.dart';
import 'package:enigma/main.dart' as app;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('real entry point draws startup before initializing services',
      (tester) async {
    final storageResponse = Completer<Map<String, Object>>();
    const storageChannel =
        MethodChannel('plugins.flutter.io/shared_preferences');
    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(
      storageChannel,
      (_) => storageResponse.future,
    );
    addTearDown(() => tester.binding.defaultBinaryMessenger
        .setMockMethodCallHandler(storageChannel, null));
    final flutterErrorHandler = FlutterError.onError;
    final asyncErrorHandler = PlatformDispatcher.instance.onError;
    addTearDown(() {
      FlutterError.onError = flutterErrorHandler;
      PlatformDispatcher.instance.onError = asyncErrorHandler;
    });

    app.main();
    // Preserve Flutter Test's error reporting while checking the real root.
    FlutterError.onError = flutterErrorHandler;
    await tester.pump();

    expect(find.byType(AppBootstrap), findsOneWidget);
    expect(find.text('Đang khởi động…'), findsOneWidget);
    expect(find.text('Debug'), findsNothing);
    if (RuntimeDiagnostics.enabled) {
      expect(RuntimeDiagnostics.lines.value.join('\n'),
          contains('Dart main entered'));
    }

    // Dispose before optional services start; this test checks the first frame.
    await tester.pumpWidget(const SizedBox.shrink());
    storageResponse.complete({});
    await tester.pump();
  });

  testWidgets('main app renders without a floating debug button',
      (tester) async {
    SharedPreferences.setMockInitialValues({});
    await StorageUtil.init();
    await tester.pumpWidget(const EnigmaApp(
      home: Scaffold(body: Text('App ready')),
    ));
    expect(find.text('App ready'), findsOneWidget);
    expect(find.text('Debug'), findsNothing);
    await tester.pumpWidget(const SizedBox.shrink());
  });
}
