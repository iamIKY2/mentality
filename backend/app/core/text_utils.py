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


def strip_markdown(text: Optional[str]) -> str:
    """
    Sanitizes markdown text into plain prose for consistent UI display:
    1. Converts leading '* ' and '• ' bullets to '- ' while preserving indentation.
    2. Removes separator rows like |---|---| or |:---|---:|, and turns '| a | b |' into 'a - b'.
    3. Drops headings (#, ##, etc. at start of line).
    4. Turns [text](url) links into plain text.
    5. Removes inline-code and block-code backticks (e.g. `code` -> code).
    6. Removes bold (**text** and __text__).
    7. Removes italics (*text* and _text_) without touching math (like 2*3) or
       underscores inside words/identifiers/URLs (like shift_day, user_id).
    8. Normalizes excessive consecutive newlines.
    """
    if not text:
        return ""
    
    # 1. Convert leading '* ' and '• ' bullets to '- '
    s = re.sub(r'(?m)^([ \t]*)[\*•][ \t]+', r'\1- ', text)

    # 2. Remove table separator rows (e.g. |---|---| or |:---|---:|)
    s = re.sub(r'(?m)^[ \t]*\|[\s:\-\|]+\|[ \t]*$\n?', '', s)

    # 3. Convert table data rows '| a | b |' -> 'a - b'
    def _convert_table_row(m: re.Match) -> str:
        cells = [c.strip() for c in m.group(1).split('|') if c.strip()]
        return " - ".join(cells)

    s = re.sub(r'(?m)^[ \t]*\|(.*)\|[ \t]*$', _convert_table_row, s)

    # 4. Drop headings (#, ##, etc. at start of line)
    s = re.sub(r'(?m)^[ \t]*#{1,6}[ \t]*', '', s)

    # 4. Turn [text](url) into text
    s = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', s)

    # 5. Remove code blocks and inline-code backticks
    s = re.sub(r'```[a-zA-Z0-9]*\n?', '', s)
    s = re.sub(r'`([^`\n]+)`', r'\1', s)
    s = s.replace('`', '')

    # 6. Remove bold **text** and __text__
    s = re.sub(r'\*\*([^*\n]+?)\*\*', r'\1', s)
    s = re.sub(r'(?<![a-zA-Z0-9_])__([^_\n\s](?:.*?[^_\n\s])?)__(?![a-zA-Z0-9_])', r'\1', s)

    # 7. Remove italics *text* and _text_ without touching math or words with underscores
    s = re.sub(r'(?<![a-zA-Z0-9])\*([^*\n\s](?:.*?[^*\n\s])?)\*(?![a-zA-Z0-9])', r'\1', s)
    s = re.sub(r'(?<![a-zA-Z0-9_])_([^_\n\s](?:.*?[^_\n\s])?)_(?![a-zA-Z0-9_])', r'\1', s)

    # 8. Clean up extra blank lines
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip('\r\n')


