CONNECT_VK_USER = """
    WITH registered_user AS (
        INSERT INTO book_club.users (vk_id, vk_tag, join_at)
        VALUES (%(vk_id)s, %(vk_tag)s, NOW())
        ON CONFLICT DO NOTHING
        RETURNING user_id
    )
    INSERT INTO book_club.users_states (user_id, state, params)
    SELECT user_id, 'menu'::TEXT, '{}'::TEXT FROM registered_user
    RETURNING user_id
"""

GET_USER_BY_VK = """
    SELECT
        user_id, vk_id, vk_tag
    FROM book_club.users
    WHERE vk_id = %(vk_id)s
"""


GET_USER_STATE = """
    SELECT
        state,
        params
    FROM book_club.users_states
    WHERE user_id = %(user_id)s
"""


UPDATE_USER_STATE = """
    UPDATE book_club.users_states
    SET
        state = %(state)s,
        params = %(params)s
    FROM book_club.users_states
    WHERE user_id = %(user_id)s
    RETURNING COUNT(*)
"""
