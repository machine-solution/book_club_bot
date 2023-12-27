from dotenv import load_dotenv
import json
import os
import vk_api
from vk_api import utils as vk_utils

import typing as tp
from common import const
from common import sql
from common import sql_scripts

load_dotenv()
TOKEN = os.environ["VK_TOKEN"]


def get_session():
    return vk_api.VkApi(token = TOKEN)


def get_api():
    return get_session().get_api()


def method(session, name, **kwargs):
    kwargs["random_id"] = vk_utils.get_random_id()
    return session.method(name, kwargs)


def send_message(session, vk_id, text, keyboard=None) -> tp.Optional[tp.Dict]:
    return method(
        session=session,
        name="messages.send",
        user_id=vk_id,
        message=text,
        keyboard=keyboard,
    )


def edit_message(session, peer_id, conversation_message_id, text, keyboard=None) -> tp.Optional[tp.Dict]:
    return method(
        session=session,
        name="messages.edit",
        conversation_message_id=conversation_message_id,
        peer_id=peer_id,
        message=text,
        keyboard=keyboard,
    )


def answer_event(session, vk_id, peer_id, event_id, event_data = None) -> tp.Optional[tp.Dict]:
    return method(
        session=session,
        name="messages.sendMessageEventAnswer",
        user_id=vk_id,
        peer_id=peer_id,
        event_id=event_id,
        event_data=event_data,
    )


def get_vk_tag(session, vk_id) -> tp.Optional[str]:
    try:
        users_data = method(
            session=session,
            name="users.get",
            user_ids=[vk_id],
            fields=["screen_name"],
        )
    except:
        return None
    if not users_data:
        return None
    return users_data[0]["screen_name"]


def get_user_state(session, user_id: tp.Optional[int]):
    default_state = {
        "state": const.USER_STATE_START,
        "params": {},
    }
    if user_id is None:
        return default_state

    result = sql.fetch_one(
        query=sql_scripts.GET_USER_STATE,
        args={
            "user_id": user_id,
        }
    )
    if result is None:
        return default_state
    return {
        "state": result["state"],
        "params": json.loads(result["params"]),
    }


# new_state have to contain key 'state' with state and key 'params' with 
# state params of type dict
def update_user_state(session, user_id, new_state: tp.Dict) -> bool:
    result = sql.fetch_one(
        query=sql_scripts.UPDATE_USER_STATE,
        args={
            "user_id": user_id,
            "state": new_state["state"],
            "params": json.dumps(new_state["params"]),
        }
    )
    # result["count"] == 1 means updated successfully
    return result["count"] == 1


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


# register user and set state 'menu' into base
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
    return result["user_id"]
