import 'package:flutter_test/flutter_test.dart';
import 'package:enigma/core/utils/text_sanitizer.dart';

void main() {
  group('stripMarkdown tests', () {
    test('1. Converts star bullets to hyphen bullets', () {
      const raw = '* Mục thứ nhất\n* Mục thứ hai';
      const expected = '- Mục thứ nhất\n- Mục thứ hai';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('2. Converts dot bullets to hyphen bullets', () {
      const raw = '• Điều 1\n• Điều 2';
      const expected = '- Điều 1\n- Điều 2';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('3. Preserves indented bullets with hyphen', () {
      const raw = '  * Cấp 1\n    • Cấp 2';
      const expected = '  - Cấp 1\n    - Cấp 2';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('4. Preserves words with underscores like shift_day', () {
      const raw = 'Bạn đang làm ca shift_day hôm nay.';
      const expected = 'Bạn đang làm ca shift_day hôm nay.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('5. Preserves math multiplication like 2*3 = 6', () {
      const raw = 'Phép tính 2*3 = 6 và 4*5';
      const expected = 'Phép tính 2*3 = 6 và 4*5';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('6. Preserves isolated math expression 2*3', () {
      const raw = '2*3';
      const expected = '2*3';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('7. Preserves identifiers and URLs with underscores', () {
      const raw = 'Kiểm tra user_id tại https://api.enigma.vn/v1/user_id?sort=created_at';
      const expected = 'Kiểm tra user_id tại https://api.enigma.vn/v1/user_id?sort=created_at';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('8. Removes markdown headings', () {
      const raw = '# Tiêu đề 1\n## Tiêu đề 2\n### Tiêu đề 3';
      const expected = 'Tiêu đề 1\nTiêu đề 2\nTiêu đề 3';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('9. Converts table rows to plain prose and removes separators', () {
      const raw = 'Dưới đây là bảng thông tin:\n'
          '| Tiêu chí | Điểm |\n'
          '|---|---|\n'
          '| Thể chất | 8 |\n'
          '| Tinh thần | 9 |\n'
          'Chúc bạn khỏe mạnh.';
      const expected = 'Dưới đây là bảng thông tin:\n'
          'Tiêu chí - Điểm\n'
          'Thể chất - 8\n'
          'Tinh thần - 9\n'
          'Chúc bạn khỏe mạnh.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('9b. Converts single table row and separator', () {
      expect(stripMarkdown('| a | b |'), equals('a - b'));
      expect(stripMarkdown('|---|---|'), equals(''));
      expect(stripMarkdown('|:---|---:|'), equals(''));
    });

    test('10. Turns markdown links into plain text', () {
      const raw = 'Vui lòng xem [Cẩm nang 5S](https://handbook.enigma.vn/5s) để biết thêm.';
      const expected = 'Vui lòng xem Cẩm nang 5S để biết thêm.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('11. Removes inline code backticks', () {
      const raw = 'Dùng lệnh `flutter test` hoặc biến `work_shift`.';
      const expected = 'Dùng lệnh flutter test hoặc biến work_shift.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('12. Removes bold formatting', () {
      const raw = 'Hãy luôn **chú ý an toàn** và __uống đủ nước__.';
      const expected = 'Hãy luôn chú ý an toàn và uống đủ nước.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('13. Removes italics formatting without touching identifiers or math', () {
      const raw = 'Đây là *lời khuyên* rất _quan trọng_ cho bạn.';
      const expected = 'Đây là lời khuyên rất quan trọng cho bạn.';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('14. Handles complex mixed markdown correctly', () {
      const raw = '### Hướng dẫn ca làm việc\n\n'
          'Chào bạn, trong ca **shift_day**, bạn cần nhớ:\n'
          '* Đọc [quy chuẩn an toàn](https://example.com/safety)\n'
          '* Thực hiện `5S` mỗi ngày\n'
          '* Phép tính 2*3 = 6 và kiểm tra `user_id`\n\n'
          '| Mã ca | Giờ |\n'
          '|---|---|\n'
          '| D1 | 12h |\n\n'
          'Chúc bạn *thành công*!';
      const expected = 'Hướng dẫn ca làm việc\n\n'
          'Chào bạn, trong ca shift_day, bạn cần nhớ:\n'
          '- Đọc quy chuẩn an toàn\n'
          '- Thực hiện 5S mỗi ngày\n'
          '- Phép tính 2*3 = 6 và kiểm tra user_id\n\n'
          'Mã ca - Giờ\n'
          'D1 - 12h\n\n'
          'Chúc bạn thành công!';
      expect(stripMarkdown(raw), equals(expected));
    });

    test('15. Handles null and empty strings', () {
      expect(stripMarkdown(null), equals(''));
      expect(stripMarkdown(''), equals(''));
    });
  });
}
