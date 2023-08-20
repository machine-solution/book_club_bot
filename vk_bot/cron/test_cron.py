from vk_bot import const
from vk_bot import vk


session = vk.get_session()

vk.method(
    session=session,
    name='messages.send',
    message=const.TEST_MESSAGE,
    chat_id= const.TEST_CHAT_ID,
)