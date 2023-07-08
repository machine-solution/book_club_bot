from dotenv import load_dotenv
import os
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

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

            if message == 'привет':
                send_message(id, 'Привет, я бот!')

            elif message == 'как дела?':
                send_message(id, 'Хорошо, а твои как?' )

            else:
                send_message(id, 'Я вас не понимаю! :(')
