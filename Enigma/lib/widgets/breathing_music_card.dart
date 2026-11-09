import 'package:flutter/material.dart';

import '../core/services/breathing_music_controller.dart';
import '../theme/app_theme.dart';

class BreathingMusicCard extends StatefulWidget {
  const BreathingMusicCard({super.key, required this.sessionFinished});

  final bool sessionFinished;

  @override
  State<BreathingMusicCard> createState() => _BreathingMusicCardState();
}

class _BreathingMusicCardState extends State<BreathingMusicCard> {
  final _music = BreathingMusicController();

  @override
  void initState() {
    super.initState();
    _music.load();
  }

  @override
  void didUpdateWidget(covariant BreathingMusicCard oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.sessionFinished && !oldWidget.sessionFinished) _music.stop();
  }

  @override
  void dispose() {
    _music.dispose();
    super.dispose();
  }

  Future<void> _showPlaylist() async {
    await showModalBottomSheet<void>(
      context: context,
      showDragHandle: true,
      isScrollControlled: true,
      builder: (sheetContext) => SafeArea(
        child: SizedBox(
          height: MediaQuery.sizeOf(sheetContext).height * 0.6,
          child: Column(
            children: [
              const Padding(
                padding: EdgeInsets.all(16),
                child: Text('Danh sách nhạc thư giãn',
                    style:
                        TextStyle(fontSize: 18, fontWeight: FontWeight.w700)),
              ),
              Expanded(
                child: ListenableBuilder(
                  listenable: _music,
                  builder: (context, _) => ListView.builder(
                    itemCount: _music.tracks.length,
                    itemBuilder: (context, index) => ListTile(
                      leading: Icon(index == _music.selectedIndex
                          ? Icons.music_note_rounded
                          : Icons.audiotrack_outlined),
                      title: Text(_music.tracks[index].title),
                      selected: index == _music.selectedIndex,
                      enabled: !_music.busy && !widget.sessionFinished,
                      trailing: index == _music.selectedIndex
                          ? const Icon(Icons.check_rounded)
                          : null,
                      onTap: () {
                        Navigator.pop(sheetContext);
                        _music.select(index);
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => ListenableBuilder(
        listenable: _music,
        builder: (context, _) {
          final canPlay = !_music.loading &&
              !_music.busy &&
              _music.tracks.isNotEmpty &&
              !widget.sessionFinished;
          return Container(
            padding: const EdgeInsets.all(16),
            decoration: AppTheme.cardDecorationFor(context),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.library_music_rounded,
                        color: AppTheme.accentMint),
                    const SizedBox(width: 10),
                    const Expanded(
                      child: Text('Nhạc thư giãn',
                          style: TextStyle(fontWeight: FontWeight.w700)),
                    ),
                    IconButton(
                      tooltip: 'Chọn bài trong danh sách nhạc',
                      onPressed: canPlay ? _showPlaylist : null,
                      icon: const Icon(Icons.queue_music_rounded),
                    ),
                  ],
                ),
                if (_music.loading)
                  const LinearProgressIndicator()
                else if (_music.tracks.isEmpty)
                  const Text(
                      'Chưa có nhạc. Thêm file vào thư mục music của dự án, '
                      'sau đó build lại ứng dụng.')
                else ...[
                  Text(_music.selectedTrack!.title,
                      maxLines: 2, overflow: TextOverflow.ellipsis),
                  const SizedBox(height: 4),
                  Text(
                    widget.sessionFinished
                        ? 'Phiên thở đã kết thúc'
                        : 'Bài ${_music.selectedIndex + 1}/${_music.tracks.length}',
                    style: TextStyle(
                        fontSize: 12,
                        color: AppTheme.onSurfaceSecondary(context)),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        tooltip: 'Bài trước',
                        onPressed: canPlay ? () => _music.skip(-1) : null,
                        icon: const Icon(Icons.skip_previous_rounded),
                      ),
                      IconButton.filledTonal(
                        tooltip: _music.playing ? 'Tạm dừng nhạc' : 'Phát nhạc',
                        onPressed: canPlay ? _music.toggle : null,
                        icon: Icon(_music.playing
                            ? Icons.pause_rounded
                            : Icons.play_arrow_rounded),
                      ),
                      IconButton(
                        tooltip: 'Dừng nhạc',
                        onPressed: canPlay ? _music.stop : null,
                        icon: const Icon(Icons.stop_rounded),
                      ),
                      IconButton(
                        tooltip: 'Bài tiếp theo',
                        onPressed: canPlay ? () => _music.skip(1) : null,
                        icon: const Icon(Icons.skip_next_rounded),
                      ),
                    ],
                  ),
                ],
                if (_music.error != null)
                  Text(_music.error!,
                      style: TextStyle(
                          color: Theme.of(context).colorScheme.error)),
              ],
            ),
          );
        },
      );
}
