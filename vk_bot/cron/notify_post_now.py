from dotenv import load_dotenv
import os
import vk_api
from vk_api.utils import get_random_id

import const

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]

vk_session = vk_api.VkApi(token = TOKEN)
vk = vk_session.get_api()

#===================================

vk.messages.send(
    random_id=get_random_id(),
    message=const.NOTIFY_NOW,
    chat_id=const.ADMIN_CHAT_ID,
)
