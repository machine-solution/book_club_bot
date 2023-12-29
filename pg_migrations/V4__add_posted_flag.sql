ALTER TABLE IF EXISTS book_club.feedbacks
    ADD COLUMN IF NOT EXISTS is_posted BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX IF NOT EXISTS posted_fb_idx ON book_club.feedbacks(is_posted);
