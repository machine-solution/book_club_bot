from vk_bot import const
from vk_bot import vk


vk_session = vk.get_session()

vk_session.method(
    'messages.send',
    {
        'message': const.NOTIFY_NOW,
        'chat_id': const.ADMIN_CHAT_ID,
        'random_id': 0,
    }
)
