CONNECT_VK_USER = """
    INSERT INTO book_club.users (vk_id, vk_tag, join_at)
    VALUES (%(vk_id)s, %(vk_tag)s, NOW())
    ON CONFLICT DO NOTHING
    RETURNING user_id
"""

GET_USER_BY_VK = """
    SELECT
        user_id, vk_id, vk_tag
    FROM book_club.users
    WHERE vk_id = %(vk_id)s
"""
