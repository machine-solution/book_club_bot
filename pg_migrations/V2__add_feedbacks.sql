CREATE TABLE IF NOT EXISTS book_club.feedbacks (
    id          SERIAL PRIMARY KEY,
    content     TEXT NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE IF NOT EXISTS book_club.users_feedbacks (
    user_id     INTEGER NOT NULL REFERENCES book_club.users(user_id) ON DELETE CASCADE,
    feedback_id INTEGER NOT NULL REFERENCES book_club.feedbacks(id) ON DELETE CASCADE
);
