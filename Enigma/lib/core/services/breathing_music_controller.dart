import 'dart:async';

import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

class BreathingMusicTrack {
  const BreathingMusicTrack(this.assetPath);

  final String assetPath;

  String get title {
    final name = assetPath.split('/').last;
    return name.substring(0, name.lastIndexOf('.')).replaceAll('_', ' ');
  }
}

/// Owns only background music; breathing cues have their own audio players.
class BreathingMusicController extends ChangeNotifier {
  BreathingMusicController({AudioPlayer Function()? playerFactory})
      : _playerFactory = playerFactory ?? AudioPlayer.new;

  final AudioPlayer Function() _playerFactory;
  AudioPlayer? _player;
  StreamSubscription<void>? _completion;
  StreamSubscription<PlayerState>? _stateChanges;
  List<BreathingMusicTrack> tracks = const [];
  int selectedIndex = 0;
  bool loading = true;
  bool busy = false;
  bool playing = false;
  String? error;
  bool _disposed = false;
  bool _hasSource = false;
  bool _stopRequested = false;

  BreathingMusicTrack? get selectedTrack =>
      tracks.isEmpty ? null : tracks[selectedIndex];

  Future<void> load({AssetBundle? bundle}) async {
    try {
      final manifest =
          await AssetManifest.loadFromAssetBundle(bundle ?? rootBundle);
      if (_disposed) return;
      final paths = manifest
          .listAssets()
          .where((path) => RegExp(r'^music/[^/]+\.(mp3|m4a|aac|wav|ogg|flac)$',
                  caseSensitive: false)
              .hasMatch(path))
          .toList()
        ..sort((a, b) => a.toLowerCase().compareTo(b.toLowerCase()));
      tracks = List.unmodifiable(paths.map(BreathingMusicTrack.new));
    } catch (e) {
      if (_disposed) return;
      error = 'Không thể tải danh sách nhạc. Hãy mở lại màn hình.';
      debugPrint('[BreathingMusic] load: $e');
    }
    if (_disposed) return;
    loading = false;
    notifyListeners();
  }

  Future<AudioPlayer> _ensurePlayer() async {
    if (_player != null) return _player!;
    final player = _playerFactory();
    _player = player;
    player.audioCache = AudioCache(prefix: '');
    _stateChanges = player.onPlayerStateChanged.listen((state) {
      if (_disposed) return;
      playing = state == PlayerState.playing;
      notifyListeners();
    });
    _completion = player.onPlayerComplete.listen((_) {
      if (!_disposed && !busy) unawaited(skip(1));
    }, onError: (Object e) {
      if (_disposed) return;
      playing = false;
      _hasSource = false;
      error =
          'Không phát được bài này. Hãy chọn bài khác hoặc kiểm tra file nhạc.';
      debugPrint('[BreathingMusic] stream: $e');
      notifyListeners();
    });
    // Mix with breathing cues instead of interrupting them on iOS.
    await player.setAudioContext(AudioContext(
      android: const AudioContextAndroid(audioFocus: AndroidAudioFocus.none),
      iOS: AudioContextIOS(
        category: AVAudioSessionCategory.playback,
        options: {AVAudioSessionOptions.mixWithOthers},
      ),
    ));
    if (!_disposed) await player.setReleaseMode(ReleaseMode.stop);
    return player;
  }

  Future<void> _run(Future<void> Function() action) async {
    if (_disposed || busy || tracks.isEmpty) return;
    busy = true;
    error = null;
    notifyListeners();
    try {
      await action();
    } catch (e) {
      if (!_disposed) {
        _hasSource = false;
        playing = false;
        error =
            'Không phát được bài này. Hãy chọn bài khác hoặc kiểm tra file nhạc.';
        try {
          await _player?.stop();
        } catch (_) {}
      }
      debugPrint('[BreathingMusic] playback: $e');
    } finally {
      if (!_disposed) {
        if (_stopRequested) {
          _stopRequested = false;
          try {
            await _player?.stop();
          } catch (e) {
            debugPrint('[BreathingMusic] stop: $e');
          }
          _hasSource = false;
          playing = false;
        }
      }
      if (!_disposed) {
        busy = false;
        notifyListeners();
      }
    }
  }

  Future<void> toggle() => _run(() async {
        final player = await _ensurePlayer();
        if (_disposed) return;
        if (playing) {
          await player.pause();
        } else if (_hasSource) {
          await player.resume();
        } else {
          await player.play(AssetSource(selectedTrack!.assetPath));
          _hasSource = true;
        }
      });

  Future<void> select(int index) => _run(() async {
        if (index < 0 || index >= tracks.length) return;
        final player = await _ensurePlayer();
        if (_disposed) return;
        await player.stop();
        if (_disposed) return;
        selectedIndex = index;
        _hasSource = false;
        await player.play(AssetSource(selectedTrack!.assetPath));
        _hasSource = true;
      });

  Future<void> skip(int direction) =>
      select(tracks.isEmpty ? 0 : (selectedIndex + direction) % tracks.length);

  Future<void> stop() {
    if (busy) {
      _stopRequested = true;
      return Future.value();
    }
    return _run(() async {
      await _player?.stop();
      _hasSource = false;
      playing = false;
    });
  }

  @override
  void dispose() {
    _disposed = true;
    _completion?.cancel();
    _stateChanges?.cancel();
    _player?.dispose();
    super.dispose();
  }
}
