from dotenv import load_dotenv
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# from vk_api.longpoll import VkLongPoll, VkEventType

from vk_bot import const
from vk_bot import vk
import json

load_dotenv()
VK_GROUP_ID = os.environ["VK_GROUP_ID"]

session = vk.get_session()
bot_longpoll = VkBotLongPoll(session, VK_GROUP_ID)
# longpoll = VkLongPoll(session)


for event in bot_longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk_id = event.obj.message["from_id"]
        vk_tag = vk.get_vk_tag(
            session=session,
            vk_id=vk_id,
        )
        user = vk.get_user_by_vk_id(
            session=session,
            vk_id=vk_id,
        )
        name = "@" + user["vk_tag"] if user else "Незнакомец"

        keyboard=json.dumps({
            "one_time": False,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "callback",
                            "payload": json.dumps({
                                "type": "custom",
                                "state": "1",
                            }),
                            "label": "Вступить в клуб",
                        },
                        "color": "primary",
                    },
                ],
            ]
        })

        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=const.REPLY_WITH_NAME % name,
            keyboard=keyboard,
        )
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        vk_id = event.obj.user_id
        if event.obj.payload.get("type", "") != "custom" or event.obj.payload.get("state", "") != "1":
            continue
        user_id = vk.register_user(
            session=session,
            vk_id=vk_id,
        )
        if user_id is None:
            message = "Вы уже были зарегистрированы ранее"
        else:
            message = "Вы зарегистрированы под id %s" % user_id
        vk.answer_event(
            session=session,
            vk_id=vk_id,
            peer_id=event.obj.peer_id,
            event_id=event.obj.event_id,
        )
        keyboard=json.dumps({
            "one_time": False,
            "buttons": [],
        })
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=message,
            keyboard=keyboard,
        )
