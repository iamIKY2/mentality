import 'package:enigma/core/startup/runtime_diagnostics.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  setUp(() => RuntimeDiagnostics.lines.value = []);

  test('log collection follows the build flag and bounds retained entries', () {
    for (var i = 0; i < 205; i++) {
      RuntimeDiagnostics.log('step $i');
    }
    if (RuntimeDiagnostics.enabled) {
      expect(RuntimeDiagnostics.lines.value.length, 200);
      expect(RuntimeDiagnostics.lines.value.first, endsWith('step 5'));
    } else {
      expect(RuntimeDiagnostics.lines.value, isEmpty);
    }
  });

  test('records platform error code without credentials in its message', () {
    RuntimeDiagnostics.error('Storage',
        PlatformException(code: '-34018', message: 'secret-token'), null);
    final log = RuntimeDiagnostics.lines.value.join('\n');
    expect(log, isNot(contains('secret-token')));
    if (RuntimeDiagnostics.enabled) expect(log, contains('code=-34018'));
  });
}
