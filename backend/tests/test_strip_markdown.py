import pytest
from app.core.text_utils import strip_markdown


def test_bullets_conversion_star():
    raw = "* Mục thứ nhất\n* Mục thứ hai"
    expected = "- Mục thứ nhất\n- Mục thứ hai"
    assert strip_markdown(raw) == expected


def test_bullets_conversion_bullet_point():
    raw = "• Điều 1\n• Điều 2"
    expected = "- Điều 1\n- Điều 2"
    assert strip_markdown(raw) == expected


def test_indented_bullets():
    raw = "  * Cấp 1\n    • Cấp 2"
    expected = "  - Cấp 1\n    - Cấp 2"
    assert strip_markdown(raw) == expected


def test_shift_day_underscore_preserved():
    raw = "Bạn đang làm ca shift_day hôm nay."
    expected = "Bạn đang làm ca shift_day hôm nay."
    assert strip_markdown(raw) == expected


def test_math_multiplication_preserved():
    raw = "Phép tính 2*3 = 6 và 4*5"
    expected = "Phép tính 2*3 = 6 và 4*5"
    assert strip_markdown(raw) == expected


def test_math_multiplication_isolated():
    raw = "2*3"
    expected = "2*3"
    assert strip_markdown(raw) == expected


def test_identifiers_and_urls_preserved():
    raw = "Kiểm tra user_id tại https://api.enigma.vn/v1/user_id?sort=created_at"
    expected = "Kiểm tra user_id tại https://api.enigma.vn/v1/user_id?sort=created_at"
    assert strip_markdown(raw) == expected


def test_headings_removed():
    raw = "# Tiêu đề 1\n## Tiêu đề 2\n### Tiêu đề 3"
    expected = "Tiêu đề 1\nTiêu đề 2\nTiêu đề 3"
    assert strip_markdown(raw) == expected


def test_tables_converted_to_plain_prose():
    raw = (
        "Dưới đây là bảng thông tin:\n"
        "| Tiêu chí | Điểm |\n"
        "|---|---|\n"
        "| Thể chất | 8 |\n"
        "| Tinh thần | 9 |\n"
        "Chúc bạn khỏe mạnh."
    )
    expected = (
        "Dưới đây là bảng thông tin:\n"
        "Tiêu chí - Điểm\n"
        "Thể chất - 8\n"
        "Tinh thần - 9\n"
        "Chúc bạn khỏe mạnh."
    )
    assert strip_markdown(raw) == expected


def test_table_row_single_conversion():
    assert strip_markdown("| a | b |") == "a - b"
    assert strip_markdown("|---|---|") == ""
    assert strip_markdown("|:---|---:|") == ""


def test_links_to_text():
    raw = "Vui lòng xem [Cẩm nang 5S](https://handbook.enigma.vn/5s) để biết thêm."
    expected = "Vui lòng xem Cẩm nang 5S để biết thêm."
    assert strip_markdown(raw) == expected


def test_backticks_inline_code_removed():
    raw = "Dùng lệnh `flutter test` hoặc biến `work_shift`."
    expected = "Dùng lệnh flutter test hoặc biến work_shift."
    assert strip_markdown(raw) == expected


def test_bold_removed():
    raw = "Hãy luôn **chú ý an toàn** và __uống đủ nước__."
    expected = "Hãy luôn chú ý an toàn và uống đủ nước."
    assert strip_markdown(raw) == expected


def test_italics_removed():
    raw = "Đây là *lời khuyên* rất _quan trọng_ cho bạn."
    expected = "Đây là lời khuyên rất quan trọng cho bạn."
    assert strip_markdown(raw) == expected


def test_complex_mixed_markdown():
    raw = (
        "### Hướng dẫn ca làm việc\n\n"
        "Chào bạn, trong ca **shift_day**, bạn cần nhớ:\n"
        "* Đọc [quy chuẩn an toàn](https://example.com/safety)\n"
        "* Thực hiện `5S` mỗi ngày\n"
        "* Phép tính 2*3 = 6 và kiểm tra `user_id`\n\n"
        "| Mã ca | Giờ |\n"
        "|---|---|\n"
        "| D1 | 12h |\n\n"
        "Chúc bạn *thành công*!"
    )
    expected = (
        "Hướng dẫn ca làm việc\n\n"
        "Chào bạn, trong ca shift_day, bạn cần nhớ:\n"
        "- Đọc quy chuẩn an toàn\n"
        "- Thực hiện 5S mỗi ngày\n"
        "- Phép tính 2*3 = 6 và kiểm tra user_id\n\n"
        "Mã ca - Giờ\n"
        "D1 - 12h\n\n"
        "Chúc bạn thành công!"
    )
    assert strip_markdown(raw) == expected


def test_empty_or_none():
    assert strip_markdown(None) == ""
    assert strip_markdown("") == ""


@pytest.mark.asyncio
async def test_get_user_approved_company_name():
    from unittest.mock import AsyncMock, MagicMock
    from app.services.chat_service import ChatService
    from uuid import uuid4

    uid = uuid4()

    # 1. Approved company
    mock_db = AsyncMock()
    mock_db.begin_nested = MagicMock(return_value=AsyncMock())
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = "Samsung Electronics"
    mock_db.execute.return_value = mock_res
    name = await ChatService.get_user_approved_company_name(mock_db, uid)
    assert name == "Samsung Electronics"

    # 2. Not approved or None
    mock_res.scalar_one_or_none.return_value = None
    name2 = await ChatService.get_user_approved_company_name(mock_db, uid)
    assert name2 is None

    # 3. Exception in query -> returns None safely
    mock_db.execute.side_effect = RuntimeError("DB connection failure")
    name3 = await ChatService.get_user_approved_company_name(mock_db, uid)
    assert name3 is None

