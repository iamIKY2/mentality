import os
import sys
import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.text_utils import normalize_vietnamese_phone
from app.db.models.user import User, UserRole
from app.db.models.crisis_flag import CrisisFlag
from app.api.routes.crisis_flags import get_crisis_flags
from app.api.routes.admin import get_admin_students, get_admin_user_detail


# ── 1. Phone validation & normalization tests ────────────────────────────────
def test_normalize_vietnamese_phone_valid():
    # 10 digits starting with 0
    assert normalize_vietnamese_phone("0912345678") == "+84912345678"
    assert normalize_vietnamese_phone("0381234567") == "+84381234567"
    assert normalize_vietnamese_phone("0791234567") == "+84791234567"

    # +84 followed by 9 digits
    assert normalize_vietnamese_phone("+84912345678") == "+84912345678"
    assert normalize_vietnamese_phone("+84381234567") == "+84381234567"

    # 84 followed by 9 digits
    assert normalize_vietnamese_phone("84912345678") == "+84912345678"

    # Numbers with spaces, hyphens, dots, parentheses
    assert normalize_vietnamese_phone("091 234 5678") == "+84912345678"
    assert normalize_vietnamese_phone("091-234-5678") == "+84912345678"
    assert normalize_vietnamese_phone("(091) 234.5678") == "+84912345678"
    assert normalize_vietnamese_phone("+84 912 345 678") == "+84912345678"


def test_normalize_vietnamese_phone_empty_clears():
    assert normalize_vietnamese_phone(None) is None
    assert normalize_vietnamese_phone("") is None
    assert normalize_vietnamese_phone("   ") is None


def test_normalize_vietnamese_phone_invalid():
    # Too short
    with pytest.raises(ValueError):
        normalize_vietnamese_phone("091234567")

    # Too long
    with pytest.raises(ValueError):
        normalize_vietnamese_phone("091234567890")

    # Non-digit characters
    with pytest.raises(ValueError):
        normalize_vietnamese_phone("091234567a")

    # Invalid country code
    with pytest.raises(ValueError):
        normalize_vietnamese_phone("+1912345678")


# ── 2. Crisis Flags Phone & Email Consent Filtering Tests ────────────────────
@pytest.mark.asyncio
async def test_crisis_flags_returns_phone_and_email_when_consent_true():
    admin = User(
        id=uuid4(),
        email="admin@enigma.edu.vn",
        full_name="Admin",
        role=UserRole.admin,
    )
    student = User(
        id=uuid4(),
        email="student@enigma.edu.vn",
        full_name="Nguyen Van A",
        student_id="2026001",
        phone="+84912345678",
        allow_crisis_contact=True,
    )
    flag = CrisisFlag(
        id=uuid4(),
        user_id=student.id,
        tier="explicit",
        source="chat",
        status="new",
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.all.return_value = [(flag, student, None)]
    db.execute.return_value = mock_res

    out = await get_crisis_flags(admin_user=admin, db=db)
    assert len(out) == 1
    item = out[0]
    assert item["phone"] == "+84912345678"
    assert item["email"] == "student@enigma.edu.vn"
    assert item["allow_crisis_contact"] is True
    assert item["contact_note"] is None
    assert "crisis_contacts" in item
    assert "mentor" in item["crisis_contacts"]
    assert "school_counseling" in item["crisis_contacts"]


@pytest.mark.asyncio
async def test_crisis_flags_nulls_phone_and_email_when_consent_false():
    admin = User(
        id=uuid4(),
        email="admin@enigma.edu.vn",
        full_name="Admin",
        role=UserRole.admin,
    )
    student = User(
        id=uuid4(),
        email="student@enigma.edu.vn",
        full_name="Nguyen Van B",
        student_id="2026002",
        phone="+84987654321",
        allow_crisis_contact=False,  # NO CONSENT
    )
    flag = CrisisFlag(
        id=uuid4(),
        user_id=student.id,
        tier="ambiguous",
        source="chat",
        status="new",
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.all.return_value = [(flag, student, None)]
    db.execute.return_value = mock_res

    out = await get_crisis_flags(admin_user=admin, db=db)
    assert len(out) == 1
    item = out[0]
    # Phone & email must be NULL when consent is false!
    assert item["phone"] is None
    assert item["email"] is None
    assert item["contact_note"] == "chưa có đồng ý liên hệ trực tiếp, hãy liên hệ qua mentor/nhà trường"
    assert item["allow_crisis_contact"] is False


@pytest.mark.asyncio
async def test_crisis_flags_when_phone_is_none_but_consent_true():
    admin = User(id=uuid4(), email="admin@enigma.edu.vn", role=UserRole.admin)
    student = User(
        id=uuid4(),
        email="student@enigma.edu.vn",
        full_name="Nguyen Van C",
        phone=None,
        allow_crisis_contact=True,
    )
    flag = CrisisFlag(
        id=uuid4(),
        user_id=student.id,
        tier="ambiguous",
        source="chat",
        status="new",
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.all.return_value = [(flag, student, None)]
    db.execute.return_value = mock_res

    out = await get_crisis_flags(admin_user=admin, db=db)
    assert len(out) == 1
    item = out[0]
    assert item["phone"] is None
    assert item["email"] == "student@enigma.edu.vn"
    assert item["contact_note"] is None
    assert item["allow_crisis_contact"] is True


@pytest.mark.asyncio
async def test_crisis_flags_returns_raw_values_without_html_escaping():
    admin = User(id=uuid4(), email="admin@enigma.edu.vn", role=UserRole.admin)
    raw_email = "student+test<dev>&co@enigma.edu.vn"
    raw_phone = "+84912345678"
    student = User(
        id=uuid4(),
        email=raw_email,
        full_name="Nguyen Van A",
        student_id="2026001",
        phone=raw_phone,
        allow_crisis_contact=True,
    )
    flag = CrisisFlag(
        id=uuid4(),
        user_id=student.id,
        tier="explicit",
        source="chat",
        status="new",
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.all.return_value = [(flag, student, None)]
    db.execute.return_value = mock_res

    out = await get_crisis_flags(admin_user=admin, db=db)
    assert len(out) == 1
    item = out[0]
    # Check that phone and email are raw, unescaped
    assert item["phone"] == raw_phone
    assert item["email"] == raw_email
    assert "&lt;" not in item["email"]
    assert "&amp;" not in item["email"]


def test_app_js_tel_and_email_rules():
    import re
    import urllib.parse
    phone_pattern = re.compile(r"^\+84\d{9}$")
    email_pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    # Helper simulating app.js action button logic
    def compute_action_buttons(item):
        has_consent = bool(item.get("allow_crisis_contact"))
        phone_str = str(item.get("phone") or "").strip()
        is_valid_vn_phone = bool(phone_pattern.fullmatch(phone_str))
        can_call = bool(has_consent and is_valid_vn_phone)
        tel_href = f"tel:{phone_str}" if can_call else None

        email_str = str(item.get("email") or "").strip()
        is_valid_email = bool(email_pattern.fullmatch(email_str))
        can_email = bool(has_consent and is_valid_email)

        mailto_href = None
        if can_email:
            at_idx = email_str.rfind("@")
            if 0 < at_idx < len(email_str) - 1:
                local_part = email_str[:at_idx]
                domain_part = email_str[at_idx + 1:]
                mailto_href = f"mailto:{urllib.parse.quote(local_part)}@{urllib.parse.quote(domain_part)}"

        return can_call, tel_href, can_email, mailto_href

    # Case 1: Consent true, normalized phone, valid email -> local and domain encoded with literal @
    call, tel, email, mailto = compute_action_buttons({
        "allow_crisis_contact": True,
        "phone": "+84912345678",
        "email": "student+test@enigma.edu.vn"
    })
    assert call is True
    assert tel == "tel:+84912345678"
    assert email is True
    assert mailto == "mailto:student%2Btest@enigma.edu.vn"
    assert "@" in mailto
    assert "%40" not in mailto

    # Case 2: Consent true, but invalid email format -> canCall true, canEmail false
    call, tel, email, mailto = compute_action_buttons({
        "allow_crisis_contact": True,
        "phone": "+84912345678",
        "email": "not-an-email"
    })
    assert call is True
    assert email is False
    assert mailto is None

    # Case 3: Consent false -> neither call nor email even if email & phone exist
    call, tel, email, mailto = compute_action_buttons({
        "allow_crisis_contact": False,
        "phone": "+84912345678",
        "email": "student@enigma.edu.vn"
    })
    assert call is False
    assert tel is None
    assert email is False
    assert mailto is None

    # Case 4: Phone not in ^\+84\d{9}$ format (e.g. starts with 0 or too short) -> cannot call
    call, tel, email, mailto = compute_action_buttons({
        "allow_crisis_contact": True,
        "phone": "0912345678",
        "email": "student@enigma.edu.vn"
    })
    assert call is False
    assert tel is None
    assert email is True
    assert mailto == "mailto:student@enigma.edu.vn"


@pytest.mark.asyncio
async def test_get_admin_students_never_leaks_phone_or_consent_in_serialization():
    import json
    secret_phone = "+84912345678"
    student = User(
        id=uuid4(),
        email="student@enigma.edu.vn",
        full_name="Nguyen Van A",
        student_id="2026001",
        phone=secret_phone,
        allow_crisis_contact=True,
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.all.return_value = [(student, None, None, None, None)]
    mock_subq_res = MagicMock()
    mock_subq_res.all.return_value = []
    db.execute.side_effect = [mock_res, mock_subq_res]

    students = await get_admin_students(db=db)
    assert len(students) == 1
    record = students[0]

    # Assert no "phone" or "allow_crisis_contact" key in the output dict
    assert "phone" not in record
    assert "allow_crisis_contact" not in record

    # Assert the phone string is completely absent from the serialized output
    serialized = json.dumps(students)
    assert secret_phone not in serialized
    assert "phone" not in serialized
    assert "allow_crisis_contact" not in serialized


# ── 3. No Leakage into Student List and User Detail Tests ────────────────────
@pytest.mark.asyncio
async def test_no_phone_leakage_in_admin_student_list():
    student = User(
        id=uuid4(),
        email="student@enigma.edu.vn",
        full_name="Secret Student",
        student_id="2026999",
        phone="+84912345678",
        allow_crisis_contact=True,
        created_at=datetime.now(timezone.utc),
    )

    db = AsyncMock()
    mock_res = MagicMock()
    # select(User, InternProfile, UserStreak, University, Company)
    mock_res.all.return_value = [(student, None, None, None, None)]
    mock_subq_res = MagicMock()
    mock_subq_res.all.return_value = []
    db.execute.side_effect = [mock_res, mock_subq_res]

    students = await get_admin_students(db=db)
    assert len(students) == 1
    record = students[0]

    # Verify phone and allow_crisis_contact are NEVER leaked in student list!
    assert "phone" not in record
    assert "allow_crisis_contact" not in record
    assert "+84912345678" not in str(record)


@pytest.mark.asyncio
async def test_no_phone_leakage_in_admin_user_detail():
    student_id = uuid4()
    student = User(
        id=student_id,
        email="student@enigma.edu.vn",
        full_name="Secret Student",
        phone="+84912345678",
        allow_crisis_contact=True,
    )

    db = AsyncMock()
    mock_res = MagicMock()
    mock_res.first.return_value = (student, None, None, None, None)
    mock_journals_res = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_journals_res.scalars.return_value = mock_scalars
    db.execute.side_effect = [mock_res, mock_journals_res]

    res = await get_admin_user_detail(user_id=student_id, db=db)
    user_data = res["user"]
    assert "phone" not in user_data
    assert "allow_crisis_contact" not in user_data
    assert "+84912345678" not in str(res)
