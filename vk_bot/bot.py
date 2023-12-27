from dotenv import load_dotenv
import os
import typing as tp

from vk_api import bot_longpoll
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# from vk_api.longpoll import VkLongPoll, VkEventType

from common import const
from common import text_templates as tt
from vk_bot import vk
import json

EventType = tp.Union[bot_longpoll.VkBotEvent, bot_longpoll.VkBotMessageEvent]


load_dotenv()
VK_GROUP_ID = os.environ["VK_GROUP_ID"]

session = vk.get_session()
bot_longpoll = VkBotLongPoll(session, VK_GROUP_ID)
# longpoll = VkLongPoll(session)


def extract_vk_id(event: EventType):
    vk_id = None
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk_id = event.obj.message["from_id"]
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        vk_id = event.obj.user_id
    return vk_id


def _empty_keyboard():
    return {
        "one_time": False,
        "buttons": [],
    }


def _start_state_keyboard():
    return {
        "one_time": True,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_REGISTER,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.JOIN_CLUB_LABEL,
                    },
                    "color": const.BUTTON_COLOR_PRIMARY,
                },
            ],
        ]
    }


def _menu_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_ADD_FEEDBACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.ADD_FEEDBACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_VIEW_FEEDBACKS,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.VIEW_FEEDBACKS_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
            ],
        ]
    }


STATE_KEYBOARD_MAP = {
    const.USER_STATE_START: _start_state_keyboard(),
    const.USER_STATE_MENU: _menu_state_keyboard(),
}


def get_keyboard(state: str) -> str:
    if state in STATE_KEYBOARD_MAP:
        return json.dumps(STATE_KEYBOARD_MAP[state])
    else:
        return json.dumps(_empty_keyboard())


# USER_STATE_START
def _start_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.START_GREETING,
            keyboard=get_keyboard(const.USER_STATE_START),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        if payload.get("action", "") == const.USER_ACTION_REGISTER:
            # state updated here to -> const.USER_STATE_MENU if success
            user_id = vk.register_user(
                session=session,
                vk_id=vk_id,
            )
            if user_id is None:
                message = tt.REGISTERED_ERLIER
            else:
                message = tt.REGISTERED_T % user_id
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=message,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )


# USER_STATE_MENU
def _menu_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.DEFAULT_MESSAGE,
            keyboard=get_keyboard(const.USER_STATE_MENU),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        if payload.get("action", "") == const.USER_ACTION_ADD_FEEDBACK:
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.DEFAULT_MESSAGE,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )
        if payload.get("action", "") == const.USER_ACTION_VIEW_FEEDBACKS:
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.DEFAULT_MESSAGE,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )


STATE_PROCESS_MAP = {
    const.USER_STATE_START: _start_process_vk,
    const.USER_STATE_MENU: _menu_process_vk,
}


def process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    state = user_state["state"]
    if state not in STATE_PROCESS_MAP:
        return
    state_process = STATE_PROCESS_MAP[state]
    return state_process(
        session=session,
        event=event,
        user_state=user_state,
        user_id=user_id,
        vk_id=vk_id,
    )


for event in bot_longpoll.listen():
    vk_id = extract_vk_id(event)
    if vk_id is None:
        continue # user has not vk_id. I don't want to deal with him
    user = vk.get_user_by_vk_id(
        session=session,
        vk_id=vk_id,
    )
    user_id = user["user_id"] if user is not None else None
    user_state = vk.get_user_state(
        session=session,
        user_id=user_id,
    )

    process_vk(
        session=session,
        event=event,
        user_state=user_state,
        user_id=user_id,
        vk_id=vk_id,
    )
