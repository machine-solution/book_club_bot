CREATE TABLE IF NOT EXISTS book_club.users_states (
    user_id         INTEGER UNIQUE NOT NULL REFERENCES book_club.users(user_id) ON DELETE CASCADE,
    state           TEXT NOT NULL,
    params          TEXT NOT NULL
);
