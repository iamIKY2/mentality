# Offline storage and synchronization

Android/iOS store the cached account, feature snapshots and pending writes in
`enigma_offline.db` using SQLite. Tokens remain in secure storage. Existing
SharedPreferences caches and pending writes migrate on the next startup.

Startup restores the cached profile immediately. Server validation runs in the
background, so Render cold starts and Supabase downtime do not block the splash
screen. A first login/registration still needs the server; guest access remains
available through the login screen. AI chat still needs the backend.

Life logs and check-ins commit their local snapshot and pending upload in one
SQLite transaction. Tasks and profile changes also queue uploads. Queues and
feature caches belong to the account that created them; guest data is not
automatically uploaded into a different account.

Uploads run after a write, on reconnect and every 60 seconds while the app runs.
Timeouts and HTTP errors keep pending data for retry. Invalid entries remain
queued; they are not silently discarded. Original recording dates accompany
check-ins and journals. Journals use a stable UUID, and task retries set the
desired completion state, so retries do not toggle a task twice.

## Deployment

Deploy the backend changes before distributing the updated mobile app. The new
backend accepts `recorded_date` and `client_id`, and the task toggle endpoint
accepts `{ "is_completed": true/false }`. No database schema migration is needed.
This source change does not deploy Render or install a new mobile build.

## Verification

- `flutter analyze --no-pub`
- `flutter test`
- Backend service unit tests: `python -m unittest discover -s backend/tests -p test_offline_sync.py`
  (requires the backend Python dependencies; sessions are mocked).

On a device, sign in once, stop the backend, restart the app, save a journal and
check-in, then restart again. Verify the data remains. Restore the backend and
use the sync action or wait for the automatic retry. Verify the queue clears and
the original dates appear on the server. Repeat a sync to check for duplicates.
