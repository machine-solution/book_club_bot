CREATE TABLE IF NOT EXISTS book_club.attachments (
    id          SERIAL PRIMARY KEY,
    feedback_id INTEGER NOT NULL REFERENCES book_club.feedbacks(id) ON DELETE CASCADE,
    url         TEXT NOT NULL,
    type        TEXT NOT NULL
);
