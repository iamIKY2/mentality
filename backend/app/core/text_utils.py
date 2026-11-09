import unicodedata
import re
from typing import Optional


def normalize_vietnamese_text(text: Optional[str]) -> str:
    """
    Normalizes Vietnamese text for accent-insensitive, case-insensitive comparison and search.
    - Converts to lower case
    - Decomposes combined diacritics (NFD) and strips them
    - Replaces 'đ' and 'Đ' with 'd'
    - Normalizes multiple spaces into a single space
    """
    if not text:
        return ""
    
    # Custom replacement for Vietnamese d-with-stroke
    cleaned = text.replace("đ", "d").replace("Đ", "D")
    
    # NFD decomposition separates base characters and combining diacritical marks
    decomposed = unicodedata.normalize("NFD", cleaned)
    
    # Strip combining diacritical marks (Unicode category 'Mn')
    without_marks = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    
    # Lowercase and collapse consecutive whitespaces
    lowered = without_marks.lower().strip()
    return re.sub(r"\s+", " ", lowered)


def is_accent_insensitive_match(pattern: str, target: str) -> bool:
    """
    Checks whether target contains pattern in an accent-insensitive and case-insensitive manner.
    """
    norm_pattern = normalize_vietnamese_text(pattern)
    norm_target = normalize_vietnamese_text(target)
    if not norm_pattern:
        return True
    return norm_pattern in norm_target


def normalize_vietnamese_phone(phone: Optional[str]) -> Optional[str]:
    """
    Validates and normalizes Vietnamese phone numbers:
    - Empty, whitespace or None returns None.
    - Strips spaces, dots, dashes, parentheses.
    - Accepts 10 digits starting with 0 (e.g. 0912345678) -> normalizes to +84912345678.
    - Accepts +84 followed by 9 digits (e.g. +84912345678) -> returns +84912345678.
    - Accepts 84 followed by 9 digits (e.g. 84912345678) -> returns +84912345678.
    - Any other format raises ValueError with friendly Vietnamese message.
    """
    if phone is None:
        return None
    cleaned = re.sub(r"[\s\-\.\(\)]", "", str(phone).strip())
    if not cleaned:
        return None
    if re.fullmatch(r"0\d{9}", cleaned):
        return "+84" + cleaned[1:]
    if re.fullmatch(r"\+84\d{9}", cleaned):
        return cleaned
    if re.fullmatch(r"84\d{9}", cleaned):
        return "+" + cleaned
    raise ValueError("Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số (bắt đầu bằng 0 hoặc +84).")

