from dotenv import load_dotenv
import os
import vk_api
from vk_api import utils as vk_utils

import typing as tp
from common import sql
from common import sql_scripts

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]


def get_session():
    return vk_api.VkApi(token = TOKEN)


def get_api():
    return get_session().get_api()


def method(session, name, **kwargs):
    kwargs['random_id'] = vk_utils.get_random_id()
    return session.method(name, kwargs)


def send_message(session, vk_id, text) -> None:
    method(
        session=session,
        name='messages.send',
        user_id=vk_id,
        message=text
    )


def get_vk_tag(session, vk_id) -> tp.Optional[str]:
    try:
        users_data = method(
            session=session,
            name='users.get',
            user_ids=[vk_id],
            fields=['screen_name'],
        )
    except:
        return None
    user_data = users_data[0]
    return user_data['screen_name']


def get_user_by_vk_id(session, vk_id) -> tp.Optional[tp.Dict]:
    result = sql.fetch_one(
        query=sql_scripts.GET_USER_BY_VK,
        args={
            "vk_id": vk_id,
        }
    )
    if result is None:
        return None
    return result


def register_user(session, vk_id) -> tp.Optional[int]:
    vk_tag = get_vk_tag(
        session=session,
        vk_id=vk_id,
    )
    if vk_tag is None:
        return None
    result = sql.fetch_one(
        query=sql_scripts.CONNECT_VK_USER,
        args={
            "vk_id": vk_id,
            "vk_tag": vk_tag,
        }
    )
    if result is None:
        return None
    return result['user_id']
