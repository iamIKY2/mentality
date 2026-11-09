import 'package:flutter_test/flutter_test.dart';
import 'package:enigma/models/user.dart';
import 'package:enigma/models/user_model.dart';

void main() {
  group('Phone validation unit tests', () {
    String? validatePhone(String? v) {
      if (v == null || v.trim().isEmpty) {
        return null; // Optional
      }
      final clean = v.replaceAll(RegExp(r'[\s\-\.\(\)]'), '');
      final vnPhoneRegex = RegExp(r'^(0\d{9}|\+84\d{9})$');
      if (!vnPhoneRegex.hasMatch(clean)) {
        return 'Số điện thoại không hợp lệ (cần 10 số bắt đầu bằng 0 hoặc +84)';
      }
      return null;
    }

    test('validates 10-digit Vietnamese phone starting with 0', () {
      expect(validatePhone('0912345678'), isNull);
      expect(validatePhone('0381234567'), isNull);
      expect(validatePhone('0791234567'), isNull);
      expect(validatePhone('0861234567'), isNull);
      expect(validatePhone('0561234567'), isNull);
    });

    test('validates Vietnamese phone starting with +84', () {
      expect(validatePhone('+84912345678'), isNull);
      expect(validatePhone('+84381234567'), isNull);
    });

    test('validates phone with spaces, dashes, dots and parentheses', () {
      expect(validatePhone('091 234 5678'), isNull);
      expect(validatePhone('091-234-5678'), isNull);
      expect(validatePhone('(091) 234.5678'), isNull);
      expect(validatePhone('+84 912 345 678'), isNull);
    });

    test('allows empty or whitespace values (optional field)', () {
      expect(validatePhone(null), isNull);
      expect(validatePhone(''), isNull);
      expect(validatePhone('   '), isNull);
    });

    test('rejects invalid phone numbers with friendly error text', () {
      const expectedError = 'Số điện thoại không hợp lệ (cần 10 số bắt đầu bằng 0 hoặc +84)';
      expect(validatePhone('12345'), expectedError);
      expect(validatePhone('091234567890'), expectedError); // 12 digits
      expect(validatePhone('091234567'), expectedError); // 9 digits
      expect(validatePhone('091234567a'), expectedError); // Letters
      expect(validatePhone('+1912345678'), expectedError); // Non-VN country code
    });
  });

  group('User and UserModel phone & consent serialization', () {
    test('User fromJson and toJson preserves phone and allowCrisisContact', () {
      final json = {
        'id': 'u1',
        'email': 'student@enigma.edu.vn',
        'full_name': 'Nguyen Van A',
        'role': 'student',
        'phone': '+84912345678',
        'allow_crisis_contact': true,
      };

      final user = User.fromJson(json);
      expect(user.phone, '+84912345678');
      expect(user.allowCrisisContact, isTrue);

      final userJson = user.toJson();
      expect(userJson['phone'], '+84912345678');
      expect(userJson['allow_crisis_contact'], isTrue);

      final updated = user.copyWith(phone: '', allowCrisisContact: false);
      expect(updated.phone, '');
      expect(updated.allowCrisisContact, isFalse);
    });

    test('UserModel fromJson and toJson preserves phone and allowCrisisContact', () {
      final json = {
        'id': 'u2',
        'email': 'student2@enigma.edu.vn',
        'full_name': 'Nguyen Van B',
        'role': 'student',
        'phone': '0987654321',
        'allow_crisis_contact': false,
      };

      final userModel = UserModel.fromJson(json);
      expect(userModel.phone, '0987654321');
      expect(userModel.allowCrisisContact, isFalse);

      final modelJson = userModel.toJson();
      expect(modelJson['phone'], '0987654321');
      expect(modelJson['allow_crisis_contact'], isFalse);
    });
  });
}

