import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../core/startup/runtime_diagnostics.dart';

class AppLogsScreen extends StatefulWidget {
  const AppLogsScreen({super.key});

  @override
  State<AppLogsScreen> createState() => _AppLogsScreenState();
}

class _AppLogsScreenState extends State<AppLogsScreen> {
  String _query = '';

  Future<void> _copyLogs(List<String> entries) async {
    try {
      await Clipboard.setData(ClipboardData(text: entries.join('\n\n')));
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Đã sao chép nhật ký')),
      );
    } catch (_) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Không thể sao chép. Vui lòng thử lại.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<List<String>>(
      valueListenable: RuntimeDiagnostics.lines,
      builder: (context, entries, child) {
        final visible = entries
            .where((entry) => entry.toLowerCase().contains(_query))
            .toList();
        return Scaffold(
          appBar: AppBar(
            title: const Text('Nhật ký ứng dụng'),
            actions: [
              IconButton(
                tooltip: 'Sao chép log',
                icon: const Icon(Icons.copy_rounded),
                onPressed: visible.isEmpty ? null : () => _copyLogs(visible),
              ),
              IconButton(
                tooltip: 'Xóa nhật ký',
                icon: const Icon(Icons.delete_outline_rounded),
                onPressed: entries.isEmpty ? null : RuntimeDiagnostics.clear,
              ),
            ],
          ),
          body: SafeArea(
            top: false,
            child: Column(
              children: [
                Padding(
                  padding: const EdgeInsets.fromLTRB(20, 12, 20, 16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        RuntimeDiagnostics.enabled
                            ? 'Ghi lại khởi động, lỗi ứng dụng và lỗi kết nối. '
                                'Giữ 200 mục gần nhất trong phiên hiện tại; '
                                'nhật ký mất khi ứng dụng khởi động lại.'
                            : 'Bản cài này đã tắt ghi nhật ký.',
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                      const SizedBox(height: 16),
                      TextField(
                        decoration: const InputDecoration(
                          labelText: 'Tìm trong nhật ký',
                          prefixIcon: Icon(Icons.search_rounded),
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (value) =>
                            setState(() => _query = value.trim().toLowerCase()),
                      ),
                      const SizedBox(height: 12),
                      Text(
                          '${visible.length}/${entries.length} mục • Mới nhất trước'),
                    ],
                  ),
                ),
                Expanded(
                  child: visible.isEmpty
                      ? Center(
                          child: Text(entries.isEmpty
                              ? 'Chưa có nhật ký trong phiên này.'
                              : 'Không tìm thấy nhật ký phù hợp.'),
                        )
                      : ListView.separated(
                          padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
                          itemCount: visible.length,
                          separatorBuilder: (context, index) =>
                              const SizedBox(height: 10),
                          itemBuilder: (context, index) => Card(
                            margin: EdgeInsets.zero,
                            child: Padding(
                              padding: const EdgeInsets.all(12),
                              child: SelectableText(
                                visible[visible.length - 1 - index],
                                style: const TextStyle(
                                  fontFamily: 'monospace',
                                  fontSize: 12,
                                  height: 1.5,
                                ),
                              ),
                            ),
                          ),
                        ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
