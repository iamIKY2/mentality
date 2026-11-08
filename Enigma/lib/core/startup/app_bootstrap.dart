import 'package:flutter/material.dart';
import 'runtime_diagnostics.dart';

/// Draw a frame before waiting for platform storage; recover from startup errors.
class AppBootstrap extends StatefulWidget {
  const AppBootstrap({
    super.key,
    required this.initialize,
    required this.builder,
    this.onReady,
    this.timeout = const Duration(seconds: 15),
  });

  final Future<void> Function() initialize;
  final WidgetBuilder builder;
  final VoidCallback? onReady;
  final Duration timeout;

  @override
  State<AppBootstrap> createState() => _AppBootstrapState();
}

class _AppBootstrapState extends State<AppBootstrap> {
  bool _ready = false;
  bool _failed = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _initialize());
  }

  Future<void> _initialize() async {
    if (!mounted) return;
    setState(() => _failed = false);
    try {
      RuntimeDiagnostics.log('Required initialization: starting');
      await widget.initialize().timeout(widget.timeout);
    } catch (error, stack) {
      RuntimeDiagnostics.error('Required initialization failed', error, stack);
      debugPrint('[Startup] Required initialization failed: $error\n$stack');
      if (mounted) setState(() => _failed = true);
      return;
    }
    if (!mounted) return;
    setState(() => _ready = true);
    RuntimeDiagnostics.log('Required initialization: ready');
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (mounted) {
        RuntimeDiagnostics.log(
            'App frame rendered; starting optional services');
        widget.onReady?.call();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_ready) return widget.builder(context);
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.all(24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Text('Enigma', style: TextStyle(fontSize: 32)),
                  const SizedBox(height: 24),
                  if (_failed) ...[
                    const Text(
                      'Không thể khởi tạo dữ liệu trên thiết bị. Vui lòng thử lại.',
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 16),
                    FilledButton(
                      onPressed: _initialize,
                      child: const Text('Thử lại'),
                    ),
                  ] else ...[
                    const CircularProgressIndicator(),
                    const SizedBox(height: 16),
                    const Text('Đang khởi động…'),
                  ],
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
