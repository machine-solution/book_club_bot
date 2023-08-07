from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import vk_bot.const as const

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]

vk_session = vk_api.VkApi(token = TOKEN)
longpoll = VkLongPoll(vk_session)


def send_message(id, text):
    vk_session.method('messages.send', {'user_id' : id, 'message' : text, 'random_id': 0})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.text.lower()
            id = event.user_id

            send_message(id, const.DEFAULT_REPLY)
