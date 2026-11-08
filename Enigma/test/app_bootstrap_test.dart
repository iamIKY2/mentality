import 'dart:async';

import 'package:enigma/core/startup/app_bootstrap.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  Widget readyApp(BuildContext context) =>
      const MaterialApp(home: Scaffold(body: Text('App ready')));

  testWidgets('renders startup while platform initialization is pending', (
    tester,
  ) async {
    final initialization = Completer<void>();
    final optionalService = Completer<void>();
    var optionalStarted = false;
    await tester.pumpWidget(
      AppBootstrap(
        initialize: () => initialization.future,
        builder: readyApp,
        onReady: () {
          optionalStarted = true;
          unawaited(optionalService.future);
        },
      ),
    );

    expect(find.text('Đang khởi động…'), findsOneWidget);
    expect(optionalStarted, isFalse);

    initialization.complete();
    await tester.pumpAndSettle();
    expect(find.text('App ready'), findsOneWidget);
    expect(optionalStarted, isTrue);
    // A service which never finishes must not block the app.
    expect(optionalService.isCompleted, isFalse);
    optionalService.complete();
  });

  testWidgets('startup failure shows retry and recovers', (tester) async {
    var attempts = 0;
    await tester.pumpWidget(
      AppBootstrap(
        initialize: () async {
          if (++attempts == 1) throw StateError('Storage unavailable');
        },
        builder: readyApp,
      ),
    );
    await tester.pumpAndSettle();
    expect(find.text('Thử lại'), findsOneWidget);
    expect(find.text('App ready'), findsNothing);

    await tester.tap(find.text('Thử lại'));
    await tester.pumpAndSettle();
    expect(attempts, 2);
    expect(find.text('App ready'), findsOneWidget);
  });

  testWidgets('hung platform initialization shows an error after timeout', (
    tester,
  ) async {
    final initialization = Completer<void>();
    await tester.pumpWidget(
      AppBootstrap(
        initialize: () => initialization.future,
        builder: readyApp,
        timeout: const Duration(seconds: 1),
      ),
    );
    await tester.pump(const Duration(seconds: 1));
    await tester.pumpAndSettle();
    expect(find.text('Thử lại'), findsOneWidget);

    // A late platform response must not replace the error screen.
    initialization.complete();
    await tester.pumpAndSettle();
    expect(find.text('Thử lại'), findsOneWidget);
    expect(find.text('App ready'), findsNothing);
  });
}
