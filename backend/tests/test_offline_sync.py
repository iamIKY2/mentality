"""Offline replay contracts, using mocked DB sessions (no network)."""
import sys
from pathlib import Path
from datetime import date, timedelta
from types import SimpleNamespace
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.life_log_service import LifeLogService
from app.services.checkin_service import CheckinService
from app.services.task_service import TaskService


def session():
    db = MagicMock()
    db.execute = AsyncMock(return_value=MagicMock())
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    return db


class OfflineReplayTests(IsolatedAsyncioTestCase):
    async def test_journal_keeps_original_day_and_client_identity(self):
        db = session()
        db.execute.return_value.scalar_one_or_none.return_value = None
        client_id = uuid4()
        recorded = date.today() - timedelta(days=3)
        result = await LifeLogService.create_life_log(
            db, uuid4(), 2, 7.5, recorded_date=recorded, client_id=client_id)
        self.assertEqual(result['journal'].journal_date, recorded)
        self.assertEqual(result['journal'].id, client_id)
        db.commit.assert_awaited_once()

    async def test_checkin_replay_finds_original_day_without_inserting_again(self):
        db = session()
        day = date.today() - timedelta(days=2)
        existing = SimpleNamespace(gacha_message='message')
        streak = SimpleNamespace(current_streak=2)
        first, second = MagicMock(), MagicMock()
        first.scalar_one_or_none.return_value = existing
        second.scalar_one_or_none.return_value = streak
        db.execute.side_effect = [first, second]
        result = await CheckinService.perform_daily_checkin(
            db, uuid4(), 'good', recorded_date=day)
        params = db.execute.call_args_list[0].args[0].compile().params
        self.assertIn(day, params.values())
        self.assertTrue(result['already_checked_in'])
        db.add.assert_not_called()

    async def test_delayed_old_checkin_does_not_rewind_current_streak(self):
        db = session()
        streak = SimpleNamespace(last_checkin_date=date.today(), current_streak=5)
        db.execute.return_value.scalar_one_or_none.return_value = streak
        result = await CheckinService._update_streak(
            db, uuid4(), date.today() - timedelta(days=4))
        self.assertEqual(result.current_streak, 5)
        self.assertEqual(result.last_checkin_date, date.today())

    async def test_task_retries_set_state_instead_of_toggling_it_again(self):
        db = session()
        progress = SimpleNamespace(is_completed=True, completed_at=None)
        db.execute.return_value.scalar_one_or_none.return_value = progress
        user_id, task_id = uuid4(), uuid4()
        self.assertTrue(await TaskService.toggle_task_completion(db, user_id, task_id, True))
        self.assertTrue(await TaskService.toggle_task_completion(db, user_id, task_id, True))
        self.assertFalse(await TaskService.toggle_task_completion(db, user_id, task_id, False))
