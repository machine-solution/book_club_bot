from vk_bot import const
from vk_bot import vk


vk_session = vk.get_session()

vk_session.method(
    'messages.send',
    message=const.NOTIFY_SOON,
    chat_id=const.ADMIN_CHAT_ID,
)
