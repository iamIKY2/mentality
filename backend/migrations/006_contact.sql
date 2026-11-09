-- Migration 006: Add contact and crisis contact consent to users
-- Idempotent and safe to re-run.
-- DO NOT RUN directly if asked by user instruction.

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'phone'
    ) THEN
        ALTER TABLE users ADD COLUMN phone VARCHAR(20) NULL;
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'allow_crisis_contact'
    ) THEN
        ALTER TABLE users ADD COLUMN allow_crisis_contact BOOLEAN NOT NULL DEFAULT FALSE;
    END IF;
END $$;

