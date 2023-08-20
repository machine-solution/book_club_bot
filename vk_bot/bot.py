from vk_api.longpoll import VkLongPoll, VkEventType

from vk_bot import const
from vk_bot import vk


session = vk.get_session()
longpoll = VkLongPoll(session)


def send_message(id, text):
    vk.method(
        session=session,
        name='messages.send',
        user_id=id,
        message=text
    )


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            id = event.user_id

            send_message(id, const.DEFAULT_REPLY)
