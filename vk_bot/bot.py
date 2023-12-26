from vk_api.longpoll import VkLongPoll, VkEventType

from vk_bot import const
from vk_bot import vk


session = vk.get_session()
longpoll = VkLongPoll(session)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            vk_id = event.user_id
            vk_tag = vk.get_vk_tag(
                session=session,
                vk_id=vk_id,
            )
            user = vk.get_user_by_vk_id(
                session=session,
                vk_id=vk_id,
            )
            name = "@" + user["vk_tag"] if user else "Незнакомец"

            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=const.REPLY_WITH_NAME % name,
            )
