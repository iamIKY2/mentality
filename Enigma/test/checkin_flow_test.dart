import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:enigma/models/daily_checkin.dart';
import 'package:enigma/state/app_state.dart';
import 'package:enigma/widgets/mood_checkin_card.dart';

void main() {
  test('restoring a check-in keeps one record and the server streak', () {
    final state = AppState();
    final factors = ['Thiếu ngủ'];
    state.recordCheckin(MoodLevel.stressed, factors, 'Ghi chú', streakDays: 7);
    factors.clear();
    expect(state.todayCheckin!.stressFactors, ['Thiếu ngủ']);
    state.recordCheckin(MoodLevel.stressed, [], '', streakDays: 7);
    expect(state.checkins.length, 1);
    expect(state.streakDays, 7);
  });

  test('every API mood round trips', () {
    for (final mood in MoodLevel.values) {
      expect(CheckinMood.fromApi(mood.apiKey), mood);
    }
  });

  testWidgets('home selects a draft and completed card cannot submit again', (
    tester,
  ) async {
    MoodLevel? selected;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MoodCheckinCard(onMoodSelected: (mood) => selected = mood),
        ),
      ),
    );
    await tester.tap(find.text('Tuyệt vời'));
    expect(selected, MoodLevel.great);
    expect(find.byType(TextField), findsNothing);
    selected = null;
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: MoodCheckinCard(
            todayCheckin: DailyCheckin(
              id: '1',
              timestamp: DateTime.now(),
              mood: MoodLevel.great,
              stressFactors: [],
            ),
            onMoodSelected: (mood) => selected = mood,
          ),
        ),
      ),
    );
    await tester.tap(find.text('Tốt'));
    expect(selected, isNull);
    expect(find.text('Đã điểm danh'), findsOneWidget);
  });
}
