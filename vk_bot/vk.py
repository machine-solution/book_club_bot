from dotenv import load_dotenv
import os
import vk_api

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]


def get_session():
    return vk_api.VkApi(token = TOKEN)
