from dotenv import load_dotenv
import os
import vk_api
from vk_api import utils as vk_utils

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]


def get_session():
    return vk_api.VkApi(token = TOKEN)


def get_api():
    return get_session().get_api()


def method(session, name, **kwargs):
    kwargs['random_id'] = vk_utils.get_random_id()
    session.method(name, kwargs)
