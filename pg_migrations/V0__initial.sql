CREATE SCHEMA IF NOT EXISTS book_club;

CREATE TABLE IF NOT EXISTS book_club.users (
    user_id     SERIAL PRIMARY KEY,
    vk_id       INTEGER NOT NULL,
    vk_tag      TEXT NOT NULL,
    join_at     TIMESTAMP WITH TIME ZONE NOT NULL
);
