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
    return result["user_id"] == user_id


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


def create_feedback(session, user_id, feedback):
    result = sql.fetch_one(
        query=sql_scripts.CREATE_FEEDBACK,
        args={
            "user_id": user_id,
            "content": feedback,
        }
    )
    if result is None:
        return None
    return result["feedback_id"]


def get_feedbacks_for_user(session, user_id, start_num: int, count: int):
    if start_num < 0:
        return []
    result = sql.fetch_all(
        query=sql_scripts.GET_FEEDBACKS_FOR_USER,
        args={
            "user_id": user_id,
            "start_num": start_num,
            "count": count,
        }
    )
    return result


def get_feedback_for_user(session, user_id, num: int):
    feedbacks = get_feedbacks_for_user(
        session=session,
        user_id=user_id,
        start_num=num,
        count=1,
    )
    if not feedbacks:
        return None
    return feedbacks[0]


def get_feedbacks_count(session, user_id):
    result = sql.fetch_one(
        query=sql_scripts.GET_FEEDBACKS_COUNT_FOR_USER,
        args={
            "user_id": user_id,
        }
    )
    return result["cnt"]


def get_feedbacks_pages_count(session, user_id):
    fb_cnt = get_feedbacks_count(session=session, user_id=user_id)
    return (fb_cnt - 1) // const.FEEDBACKS_PAGE_SIZE + 1


def _prepare_feedback(num: int, start_num: int, content: str) -> str:
    prefix = str(num + start_num + 1) + ". "
    suffix = "\n"
    if len(content) + len(prefix) + len(suffix) < const.FEEDBACK_PREVIEW_LINE_SIZE:
        return prefix + content + suffix
    suffix = "...\n"
    content_len = const.FEEDBACK_PREVIEW_LINE_SIZE - len(suffix) - len(prefix)
    return prefix + content[:content_len] + suffix


def get_preview_feedbacks(session, user_id, page_num):
    feedbacks = get_feedbacks_for_user(
        session=session,
        user_id=user_id,
        start_num=page_num * const.FEEDBACKS_PAGE_SIZE,
        count=const.FEEDBACKS_PAGE_SIZE,
    )
    answer = ""
    for num, feedback in enumerate(feedbacks):
        answer += _prepare_feedback(
            num=num,
            start_num=page_num * const.FEEDBACKS_PAGE_SIZE,
            content=feedback["content"],
        )
    return answer


def update_feedback(session, feedback_id, content):
    result = sql.fetch_one(
        query=sql_scripts.UPDATE_FEEDBACK,
        args={
            "feedback_id": feedback_id,
            "content": content,
        }
    )


def delete_feedback(session, feedback_id, content):
    result = sql.fetch_one(
        query=sql_scripts.DELETE_FEEDBACK,
        args={
            "feedback_id": feedback_id,
        }
    )
