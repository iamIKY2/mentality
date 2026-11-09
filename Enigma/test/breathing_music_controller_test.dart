import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:enigma/core/services/breathing_music_controller.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

class _MusicBundle extends CachingAssetBundle {
  _MusicBundle(this.paths);
  final List<String> paths;

  @override
  Future<ByteData> load(String key) async {
    expect(key, 'AssetManifest.bin');
    return const StandardMessageCodec().encodeMessage({
      for (final path in paths)
        path: [
          {'asset': path},
        ],
    })!;
  }
}

class _FakePlayer implements AudioPlayer {
  final states = StreamController<PlayerState>.broadcast(sync: true);
  final completions = StreamController<void>.broadcast(sync: true);
  final played = <String>[];
  int pauses = 0;
  int resumes = 0;
  int stops = 0;
  bool disposed = false;
  bool failPlayback = false;
  Completer<void>? playGate;

  @override
  late AudioCache audioCache;

  @override
  Stream<PlayerState> get onPlayerStateChanged => states.stream;
  @override
  Stream<void> get onPlayerComplete => completions.stream;
  @override
  Future<void> setAudioContext(AudioContext context) async {}
  @override
  Future<void> setReleaseMode(ReleaseMode mode) async {}
  @override
  Future<void> play(Source source,
      {double? volume,
      double? balance,
      AudioContext? ctx,
      Duration? position,
      PlayerMode? mode}) async {
    if (playGate != null) await playGate!.future;
    if (failPlayback) throw StateError('Invalid audio');
    played.add((source as AssetSource).path);
    states.add(PlayerState.playing);
  }

  @override
  Future<void> pause() async {
    pauses++;
    states.add(PlayerState.paused);
  }

  @override
  Future<void> resume() async {
    resumes++;
    states.add(PlayerState.playing);
  }

  @override
  Future<void> stop() async {
    stops++;
    states.add(PlayerState.stopped);
  }

  @override
  Future<void> dispose() async {
    disposed = true;
    await states.close();
    await completions.close();
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => super.noSuchMethod(invocation);
}

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  test('discovers music assets, ignores other files, sorts and names tracks',
      () async {
    final music = BreathingMusicController();
    addTearDown(music.dispose);
    await music.load(
        bundle: _MusicBundle([
      'music/Zen.wav',
      'music/Am_thanh.MP3',
      'music/README.md',
      'assets/other.mp3',
      'music/nested/hidden.mp3',
    ]));
    expect(music.tracks.map((t) => t.title), ['Am thanh', 'Zen']);
    expect(music.loading, isFalse);
  });

  test('empty playlist does not create a player', () async {
    final music = BreathingMusicController(
        playerFactory: () => throw StateError('Unused'));
    addTearDown(music.dispose);
    await music.load(bundle: _MusicBundle(['music/README.md']));
    await music.toggle();
    await music.skip(1);
    await music.stop();
    expect(music.error, isNull);
    expect(music.selectedTrack, isNull);
  });

  late _FakePlayer player;
  late BreathingMusicController music;

  group('playback', () {
    setUp(() async {
      player = _FakePlayer();
      music = BreathingMusicController(playerFactory: () => player);
      await music.load(bundle: _MusicBundle(['music/a.mp3', 'music/b.wav']));
    });
    tearDown(() => music.dispose());

    test('pause resumes same source; stop starts it again from the beginning',
        () async {
      await music.toggle();
      expect(player.audioCache.prefix, '');
      expect(player.played, ['music/a.mp3']);
      expect(music.playing, isTrue);
      await music.toggle();
      expect(player.pauses, 1);
      expect(music.playing, isFalse);
      await music.toggle();
      expect(player.resumes, 1);
      await music.stop();
      expect(music.playing, isFalse);
      await music.toggle();
      expect(player.played, ['music/a.mp3', 'music/a.mp3']);
    });

    test('selects tracks, wraps both directions and advances on completion',
        () async {
      await music.select(1);
      expect(music.selectedTrack!.assetPath, 'music/b.wav');
      await music.skip(1);
      expect(music.selectedIndex, 0);
      await music.skip(-1);
      expect(music.selectedIndex, 1);
      player.completions.add(null);
      await Future<void>.delayed(Duration.zero);
      expect(music.selectedIndex, 0);
      expect(player.played.last, 'music/a.mp3');
    });

    test('bad files report error and allow playing another track', () async {
      player.failPlayback = true;
      await music.toggle();
      expect(music.error, isNotNull);
      expect(music.playing, isFalse);
      player.failPlayback = false;
      await music.select(1);
      expect(music.error, isNull);
      expect(music.playing, isTrue);
    });

    test('session ending while a track loads still stops playback', () async {
      player.playGate = Completer<void>();
      final pending = music.toggle();
      await Future<void>.delayed(Duration.zero);
      await music.stop();
      player.playGate!.complete();
      await pending;
      expect(music.playing, isFalse);
      expect(player.stops, 1);
    });

    test('disposing releases player and subscriptions', () async {
      await music.toggle();
      var notifications = 0;
      music.addListener(() => notifications++);
      music.dispose();
      expect(player.disposed, isTrue);
      expect(notifications, 0);
      // Prevent tearDown from disposing the same notifier twice.
      music = BreathingMusicController();
    });
  });
}
