import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:enigma/app.dart';
import 'package:enigma/navigation/student_nav.dart';
import 'package:enigma/core/utils/storage.dart';
import 'package:enigma/core/services/sync_service.dart';
import 'package:enigma/widgets/dashboard_summary_card.dart';
import 'package:enigma/core/onboarding/feature_tour_controller.dart';

void main() {
  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    await StorageUtil.init();
  });

  testWidgets('Enigma App smoke test and UI verification', (WidgetTester tester) async {
    tester.view.physicalSize = const Size(1080, 2400);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(() => tester.view.resetPhysicalSize());
    addTearDown(() => tester.view.resetDevicePixelRatio());
    addTearDown(SyncService.instance.cancelTimers);
    addTearDown(FeatureTour.dismiss);

    // Build our app and trigger a frame.
    await tester.pumpWidget(const EnigmaApp(home: StudentNav()));
    await tester.pump();
    await tester.pump(const Duration(seconds: 2));

    // Verify header and core sections exist
    expect(find.byType(DashboardSummaryCard), findsOneWidget);
    expect(find.text('Cảm xúc hôm nay'), findsOneWidget);
    expect(find.text('Nhiệm vụ hôm nay'), findsOneWidget);

    // Cancel timers
    SyncService.instance.cancelTimers();
    await tester.pump(const Duration(seconds: 1));
  }, variant: TargetPlatformVariant({TargetPlatform.android, TargetPlatform.iOS}));
}
