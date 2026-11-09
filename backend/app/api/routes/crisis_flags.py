import html
from uuid import UUID
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, Field

from app.db.database import get_db
from app.db.models.user import User
from app.db.models.intern_profile import InternProfile
from app.db.models.crisis_flag import CrisisFlag
from app.api.routes.admin import get_authed_admin
from app.core.config import settings

router = APIRouter()


class UpdateCrisisFlagRequest(BaseModel):
    status: str = Field(..., description="'new', 'contacted', 'resolved'")
    admin_note: Optional[str] = None


@router.get("/crisis-flags", summary="Lấy danh sách cờ cảnh báo khủng hoảng")
async def get_crisis_flags(
    admin_user: User = Depends(get_authed_admin),
    db: AsyncSession = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[AUDIT] Admin {admin_user.email} (ID {admin_user.id}) xem danh sách crisis flags")

    stmt = (
        select(CrisisFlag, User, InternProfile)
        .join(User, CrisisFlag.user_id == User.id)
        .outerjoin(InternProfile, User.id == InternProfile.user_id)
        .order_by(CrisisFlag.created_at.desc())
        .limit(50)
    )
    res = await db.execute(stmt)
    rows = res.all()

    out = []
    for flag, u, p in rows:
        has_consent = bool(u.allow_crisis_contact)
        if has_consent:
            phone_val = u.phone if u.phone else None
            email_val = u.email if u.email else None
            contact_note = None
        else:
            phone_val = None
            email_val = None
            contact_note = "chưa có đồng ý liên hệ trực tiếp, hãy liên hệ qua mentor/nhà trường"

        out.append({
            "id": str(flag.id),
            "user_id": str(flag.user_id),
            "full_name": html.escape(u.full_name or ""),
            "student_id": html.escape(u.student_id or ""),
            "email": email_val,
            "phone": phone_val,
            "contact_note": contact_note,
            "allow_crisis_contact": has_consent,
            "company_name": html.escape(p.company_name or "") if p else None,
            "tier": str(flag.tier),
            "source": str(flag.source),
            "status": str(flag.status),
            "admin_note": html.escape(flag.admin_note or "") if flag.admin_note else None,
            "handled_by": str(flag.handled_by) if flag.handled_by else None,
            "handled_at": flag.handled_at.isoformat() if flag.handled_at else None,
            "created_at": flag.created_at.isoformat() if flag.created_at else None,
            "crisis_contacts": {
                "mentor": html.escape(settings.CRISIS_CONTACT_MENTOR or ""),
                "school_counseling": html.escape(settings.CRISIS_CONTACT_SCHOOL_COUNSELING or ""),
                "company_clinic": html.escape(settings.CRISIS_CONTACT_COMPANY_CLINIC or ""),
                "emergency": html.escape(settings.CRISIS_CONTACT_EMERGENCY or "115"),
            }
        })
    return out


@router.put("/crisis-flags/{flag_id}", summary="Cập nhật trạng thái xử lý cảnh báo khủng hoảng")
async def update_crisis_flag(
    flag_id: UUID,
    payload: UpdateCrisisFlagRequest,
    admin_user: User = Depends(get_authed_admin),
    db: AsyncSession = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)

    res = await db.execute(select(CrisisFlag).where(CrisisFlag.id == flag_id))
    flag = res.scalar_one_or_none()
    if not flag:
        raise HTTPException(status_code=404, detail="Không tìm thấy cảnh báo khủng hoảng.")

    old_status = flag.status
    flag.status = payload.status
    if payload.admin_note is not None:
        flag.admin_note = payload.admin_note
    flag.handled_by = admin_user.id
    flag.handled_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(flag)

    logger.critical(
        f"[AUDIT] Admin {admin_user.email} (ID {admin_user.id}) đã cập nhật crisis_flag {flag.id} "
        f"từ '{old_status}' sang '{flag.status}'"
    )
    return {"status": "updated", "id": str(flag.id), "new_status": flag.status}

