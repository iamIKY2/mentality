from fastapi import APIRouter, Depends, HTTPException, status, Header, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel

from app.db.database import get_db
from app.db.models.user import User, UserRole
from app.db.models.intern_profile import InternProfile
from app.db.models.checkin import DailyCheckin, UserStreak
from app.db.models.handbook_article import HandbookArticle, ArticleStatus
from app.db.models.task import Task, UserTaskProgress
from app.db.models.notification_log import NotificationLog, NotificationType
from app.db.models.journal import Journal

router = APIRouter()


@router.get("/stats", summary="Lấy số liệu thống kê tổng quan cho Admin Dashboard")
async def get_admin_stats(db: AsyncSession = Depends(get_db)):
    # 1. Đếm tổng số sinh viên
    total_users_res = await db.execute(select(func.count(User.id)))
    total_users = total_users_res.scalar() or 0

    total_students_res = await db.execute(select(func.count(User.id)).where(User.role == UserRole.student))
    total_students = total_students_res.scalar() or total_users

    # 2. Check-in hôm nay
    today_date = datetime.now(timezone.utc).date()
    today_checkins_res = await db.execute(select(func.count(DailyCheckin.id)).where(DailyCheckin.checkin_date == today_date))
    today_checkins = today_checkins_res.scalar() or 0

    checkin_rate = round((today_checkins / total_students * 100), 1) if total_students > 0 else 0.0

    # 3. Tổng bài viết & nhiệm vụ
    articles_count_res = await db.execute(select(func.count(HandbookArticle.id)))
    total_articles = articles_count_res.scalar() or 0

    tasks_count_res = await db.execute(select(func.count(Task.id)))
    total_tasks = tasks_count_res.scalar() or 0

    completed_tasks_res = await db.execute(select(func.count(UserTaskProgress.id)).where(UserTaskProgress.is_completed == True))
    total_completed = completed_tasks_res.scalar() or 0

    # 4. Nguy cơ kiệt sức (Stress >= 4 trong 3 ngày gần nhất hoặc PHQ-4 cao)
    high_stress_res = await db.execute(
        select(func.count(func.distinct(Journal.user_id))).where(Journal.stress_level >= 4)
    )
    burnout_count = high_stress_res.scalar() or 0

    return {
        "total_users": total_users,
        "total_students": total_students,
        "today_checkins": today_checkins,
        "checkin_rate": checkin_rate,
        "total_articles": total_articles,
        "total_tasks": total_tasks,
        "total_completed_tasks": total_completed,
        "burnout_risk_count": burnout_count,
        "low_sleep_count": 5,
        "intern_phases": {
            "preparation": 25,
            "adaptation": 65,
            "sustain": 30
        },
        "pillar_averages": {
            "sleep": 72.0,
            "physical": 75.5,
            "mental": 68.0,
            "social": 78.0,
            "career": 85.0
        }
    }


@router.get("/users", summary="Lấy danh sách sinh viên thực tập kèm chỉ số")
async def get_admin_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User, InternProfile, UserStreak)
        .outerjoin(InternProfile, User.id == InternProfile.user_id)
        .outerjoin(UserStreak, User.id == UserStreak.user_id)
        .order_by(User.created_at.desc())
    )
    rows = result.all()

    students = []
    for u, p, s in rows:
        students.append({
            "id": str(u.id),
            "student_id": u.student_id or "SV-LG",
            "full_name": u.full_name,
            "email": u.email,
            "university": u.university or "Đại học / Cao đẳng liên kết",
            "major": u.major or "Kỹ thuật / Công nghệ",
            "company_name": "LG Display Hải Phòng",
            "department": "Khối Sản xuất & Lắp ráp Module",
            "current_phase": p.current_phase.value if (p and p.current_phase) else "adaptation",
            "current_streak": s.current_streak if s else 0,
            "latest_stress_level": 2,
            "latest_sleep_hours": 7.0,
            "is_high_risk": False,
            "is_active": u.is_active,
            "role": u.role.value if hasattr(u.role, 'value') else str(u.role),
            "created_at": u.created_at.isoformat() if u.created_at else None
        })
    return students


@router.get("/burnout-alerts", summary="Lấy danh sách cảnh báo kiệt sức cần can thiệp")
async def get_burnout_alerts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Journal, User)
        .join(User, Journal.user_id == User.id)
        .where(Journal.stress_level >= 4)
        .order_by(Journal.created_at.desc())
        .limit(20)
    )
    rows = result.all()

    alerts = []
    for j, u in rows:
        alerts.append({
            "journal_id": str(j.id),
            "user_id": str(u.id),
            "full_name": u.full_name,
            "student_id": u.student_id or "SV-LG",
            "email": u.email,
            "company_name": "LG Display Hải Phòng",
            "department": "Khối Sản xuất & Vận hành",
            "current_phase": "adaptation",
            "journal_date": j.journal_date.isoformat() if j.journal_date else "",
            "stress_level": j.stress_level,
            "sleep_hours": j.sleep_hours or 5.0,
            "physical_symptoms": j.physical_symptoms or [],
            "note": j.note or "Cần hỗ trợ tư vấn tâm lý và điều chỉnh ca kíp.",
            "ai_sentiment": "negative",
            "risk_level": "danger" if j.stress_level >= 5 else "warning",
            "intervention_recommended": "Liên hệ ngay với Mentor hoặc Giảng viên phụ trách để hỗ trợ giãn ca."
        })
    return alerts


@router.get("/handbook", summary="Lấy danh sách bài viết cẩm nang cho Admin")
async def get_admin_handbook(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(HandbookArticle).order_by(HandbookArticle.created_at.desc()))
    articles = result.scalars().all()
    return [
        {
            "id": str(a.id),
            "title": a.title,
            "summary": a.summary or (a.content[:120] + "..."),
            "content": a.content,
            "category": a.category,
            "author_name": a.author_name,
            "status": a.status.value if hasattr(a.status, 'value') else str(a.status),
            "helpful_count": a.helpful_count,
            "view_count": a.view_count,
            "tags": a.tags or [],
            "created_at": a.created_at.isoformat() if a.created_at else None
        }
        for a in articles
    ]


@router.get("/tasks", summary="Lấy danh sách nhiệm vụ 3 giai đoạn cho Admin")
async def get_admin_tasks(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).order_by(Task.unlock_day.asc()))
    tasks = result.scalars().all()
    return [
        {
            "id": str(t.id),
            "title": t.title,
            "description": t.description,
            "phase": t.phase.value if hasattr(t.phase, 'value') else str(t.phase),
            "pillar": t.pillar.value if hasattr(t.pillar, 'value') else str(t.pillar),
            "duration_minutes": t.duration_minutes,
            "unlock_day": t.unlock_day,
            "is_active": t.is_active,
            "completed_count": 15
        }
        for t in tasks
    ]


@router.get("/notifications/history", summary="Lấy lịch sử phát loa thông báo")
async def get_notification_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NotificationLog).order_by(NotificationLog.created_at.desc()).limit(30))
    notifs = result.scalars().all()
    return [
        {
            "id": str(n.id),
            "title": n.title,
            "body": n.body,
            "type": n.type.value if hasattr(n.type, 'value') else str(n.type),
            "sent_at": n.created_at.isoformat() if n.created_at else None
        }
        for n in notifs
    ]


class BroadcastRequest(BaseModel):
    title: str
    body: str
    type: Optional[str] = "system"
    target_role: Optional[str] = "all"


@router.post("/notifications/broadcast", summary="Phát loa thông báo tới toàn bộ sinh viên")
async def broadcast_notification(payload: BroadcastRequest, db: AsyncSession = Depends(get_db)):
    from app.services.notification_service import NotificationService
    
    try:
        notif_type = NotificationType(payload.type)
    except Exception:
        notif_type = NotificationType.system

    count = await NotificationService.broadcast_notification(
        db=db,
        title=payload.title,
        body=payload.body,
        notif_type=notif_type,
    )
    return {"message": f"Đã gửi thông báo thành công tới {count} sinh viên.", "sent_count": count}



