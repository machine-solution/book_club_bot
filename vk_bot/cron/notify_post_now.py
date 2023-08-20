from vk_bot import const
from vk_bot import vk


session = vk.get_session()

vk.method(
    session=session,
    name='messages.send',
    message=const.NOTIFY_NOW,
    chat_id= const.ADMIN_CHAT_ID,
)
