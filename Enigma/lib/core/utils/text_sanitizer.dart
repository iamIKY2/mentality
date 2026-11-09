/// Utility to sanitize LLM-generated markdown into clean plain prose
/// for consistent UI rendering without broken markdown symbols.
String stripMarkdown(String? text) {
  if (text == null || text.isEmpty) {
    return '';
  }

  var s = text;

  // 1. Convert leading '* ' and '• ' bullets to '- ' while preserving indentation
  s = s.replaceAllMapped(
    RegExp(r'^([ \t]*)[\*•][ \t]+', multiLine: true),
    (m) => '${m[1]}- ',
  );

  // 2. Remove table separator rows (e.g. |---|---| or |:---|---:|)
  s = s.replaceAllMapped(
    RegExp(r'^[ \t]*\|[\s:\-\|]+\|[ \t]*$\n?', multiLine: true),
    (_) => '',
  );

  // 3. Convert table data rows '| a | b |' -> 'a - b'
  s = s.replaceAllMapped(
    RegExp(r'^[ \t]*\|(.*)\|[ \t]*$', multiLine: true),
    (m) {
      final inner = m[1] ?? '';
      final cells = inner
          .split('|')
          .map((c) => c.trim())
          .where((c) => c.isNotEmpty)
          .toList();
      return cells.join(' - ');
    },
  );

  // 4. Drop headings (#, ##, etc. at start of line)
  s = s.replaceAllMapped(
    RegExp(r'^[ \t]*#{1,6}[ \t]*', multiLine: true),
    (_) => '',
  );

  // 4. Turn [text](url) links into plain text
  s = s.replaceAllMapped(
    RegExp(r'\[([^\]]+)\]\([^\)]+\)'),
    (m) => m[1] ?? '',
  );

  // 5. Remove code blocks and inline-code backticks
  s = s.replaceAll(RegExp(r'```[a-zA-Z0-9]*\n?'), '');
  s = s.replaceAllMapped(RegExp(r'`([^`\n]+)`'), (m) => m[1] ?? '');
  s = s.replaceAll('`', '');

  // 6. Remove bold **text** and __text__
  s = s.replaceAllMapped(
    RegExp(r'\*\*([^*\n]+?)\*\*'),
    (m) => m[1] ?? '',
  );
  s = s.replaceAllMapped(
    RegExp(r'(?<![a-zA-Z0-9_])__([^_\n\s](?:.*?[^_\n\s])?)__(?![a-zA-Z0-9_])'),
    (m) => m[1] ?? '',
  );

  // 7. Remove italics *text* and _text_ without touching math (2*3) or identifiers/URLs with underscores (shift_day, user_id)
  s = s.replaceAllMapped(
    RegExp(r'(?<![a-zA-Z0-9])\*([^*\n\s](?:.*?[^*\n\s])?)\*(?![a-zA-Z0-9])'),
    (m) => m[1] ?? '',
  );
  s = s.replaceAllMapped(
    RegExp(r'(?<![a-zA-Z0-9_])_([^_\n\s](?:.*?[^_\n\s])?)_(?![a-zA-Z0-9_])'),
    (m) => m[1] ?? '',
  );

  // 8. Clean up extra blank lines
  s = s.replaceAll(RegExp(r'\n{3,}'), '\n\n');

  // Strip leading/trailing newlines
  return s.replaceAll(RegExp(r'^[\r\n]+|[\r\n]+$'), '');
}

