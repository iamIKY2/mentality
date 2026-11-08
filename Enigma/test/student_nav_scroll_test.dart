import 'package:enigma/app.dart';
import 'package:enigma/core/onboarding/feature_tour_controller.dart';
import 'package:enigma/core/onboarding/services/feature_onboarding_service.dart';
import 'package:enigma/core/services/sync_service.dart';
import 'package:enigma/core/utils/storage.dart';
import 'package:enigma/navigation/student_nav.dart';
import 'package:enigma/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  setUp(() async {
    SharedPreferences.setMockInitialValues({
      'user_onboarded_features_guest': 'home,tasks,checkin,handbook,chat',
    });
    await StorageUtil.init();
    await FeatureOnboardingService.instance.initForUser('guest');
  });

  testWidgets('bottom menu follows user scroll and resets when switching tabs',
      (tester) async {
    addTearDown(SyncService.instance.cancelTimers);
    addTearDown(FeatureTour.dismiss);
    await tester.pumpWidget(const EnigmaApp(home: StudentNav()));
    await tester.pump(const Duration(seconds: 2));

    final homeScroll = find.descendant(
      of: find.byType(HomeScreen),
      matching: find.byType(CustomScrollView),
    );
    final nav = find.byType(NavigationBar);
    final navAnimation = find.ancestor(
      of: nav,
      matching: find.byType(TweenAnimationBuilder<double>),
    );
    final expandedHeight = tester.getSize(navAnimation).height;
    expect(expandedHeight, greaterThan(0));

    await tester.drag(homeScroll, const Offset(0, -300));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, 0);

    // A small reversal must not make the bar flicker back into view.
    final gesture = await tester.startGesture(tester.getCenter(homeScroll));
    await gesture.moveBy(const Offset(0, 3));
    await gesture.up();
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, 0);

    await tester.drag(homeScroll, const Offset(0, 150));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, expandedHeight);

    await tester.drag(homeScroll, const Offset(0, -150));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, 0);

    tester.state<StudentNavState>(find.byType(StudentNav)).switchToTab(3);
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    expect(tester.getSize(navAnimation).height, expandedHeight);
    expect(tester.widget<NavigationBar>(nav).selectedIndex, 3);

    // Explicit hiding (for other flows) takes precedence over scroll gestures.
    final state = tester.state<StudentNavState>(find.byType(StudentNav));
    state.switchToTab(0);
    state.setNavVisible(false);
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 400));
    await tester.drag(homeScroll, const Offset(0, 150));
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, 0);
    state.setNavVisible(true);
    await tester.pump();
    await tester.pump();
    await tester.pump(const Duration(milliseconds: 300));
    expect(tester.getSize(navAnimation).height, expandedHeight);

    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump(const Duration(seconds: 1));
  },
      variant:
          TargetPlatformVariant({TargetPlatform.android, TargetPlatform.iOS}));
}
