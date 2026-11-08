import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

/// Bounded session logs: do not collect HTTP bodies or credentials.
class RuntimeDiagnostics {
  static const enabled =
      bool.fromEnvironment('ENIGMA_DIAGNOSTICS', defaultValue: true);
  static final lines = ValueNotifier<List<String>>([]);

  static void clear() => lines.value = [];

  static void log(String message) {
    if (!enabled) return;
    final entry = '${DateTime.now().toIso8601String()} $message';
    final updated = [...lines.value, entry];
    lines.value =
        updated.length > 200 ? updated.sublist(updated.length - 200) : updated;
    debugPrint(entry);
  }

  static void error(String stage, Object error, StackTrace? stack) {
    // The error message may contain user data. Keep its type and stack only.
    final code = error is PlatformException ? ' code=${error.code}' : '';
    log('$stage: ${error.runtimeType}$code\n${stack ?? ''}');
  }
}
