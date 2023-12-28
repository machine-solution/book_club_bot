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
    WHERE user_id = %(user_id)s
    RETURNING user_id
"""


CREATE_FEEDBACK = """
    WITH created_feedback AS (
        INSERT INTO book_club.feedbacks (content, created_at)
        VALUES (%(content)s, NOW())
        RETURNING id
    )
    INSERT INTO book_club.users_feedbacks (user_id, feedback_id)
    SELECT %(user_id)s, id FROM created_feedback
    RETURNING feedback_id
"""


GET_FEEDBACKS_FOR_USER = """
    SELECT
        feedbacks.content,
        feedbacks.id
    FROM book_club.feedbacks
    JOIN book_club.users_feedbacks
        ON (users_feedbacks.user_id = %(user_id)s
            AND feedbacks.id = users_feedbacks.feedback_id)
    ORDER BY created_at DESC
    OFFSET %(start_num)s
    LIMIT %(count)s
"""


GET_FEEDBACKS_COUNT_FOR_USER = """
    SELECT
        COUNT(*) as cnt
    FROM book_club.feedbacks
    JOIN book_club.users_feedbacks
        ON (users_feedbacks.user_id = %(user_id)s
            AND feedbacks.id = users_feedbacks.feedback_id)
"""


UPDATE_FEEDBACK = """
    UPDATE book_club.feedbacks
    SET
        content = %(content)s
    WHERE id = %(feedback_id)s
"""


DELETE_FEEDBACK = """
    DELETE FROM book_club.feedbacks
    WHERE id = %(feedback_id)s
"""
