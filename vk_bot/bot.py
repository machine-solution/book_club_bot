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
        "one_time": False,
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


def _writing_feedback_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_BACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.BACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
            ],
        ]
    }


def _preview_page_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_FIRST_PAGE_FB,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.FIRST_PAGE_FB_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_PREV_PAGE_FB,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.PREV_PAGE_FB_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_NEXT_PAGE_FB,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.NEXT_PAGE_FB_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_LAST_PAGE_FB,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.LAST_PAGE_FB_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
            ],
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_BACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.BACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
            ],
        ]
    }


def _feedback_selected_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_EDIT_FEEDBACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.EDIT_FEEDBACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_DELETE_FEEDBACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.DELETE_FEEDBACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_SECONDARY,
                },
            ],
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_BACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.BACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_TO_MENU,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.TO_MENU_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
            ],
        ]
    }


def _editing_feedback_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_BACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.BACK_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
            ],
        ]
    }


def _deleting_feedback_state_keyboard():
    return {
        "one_time": False,
        "buttons": [
            [
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_CONFIRM_DELETE_FB,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.YES_LABEL,
                    },
                    "color": const.BUTTON_COLOR_POSITIVE,
                },
                {
                    "action": {
                        "type": const.BUTTON_TYPE_CALLBACK,
                        "payload": json.dumps({
                            "action": const.USER_ACTION_BACK,
                            "type": const.PAYLOAD_TYPE_CUSTOM,
                        }),
                        "label": tt.NO_LABEL,
                    },
                    "color": const.BUTTON_COLOR_NEGATIVE,
                },
            ],
        ]
    }


STATE_KEYBOARD_MAP = {
    const.USER_STATE_START: _start_state_keyboard(),
    const.USER_STATE_MENU: _menu_state_keyboard(),
    const.USER_STATE_WRITING_FEEDBACK: _writing_feedback_state_keyboard(),
    const.USER_STATE_PREVIEW_PAGE: _preview_page_state_keyboard(),
    const.USER_STATE_FEEDBACK_SELECTED: _feedback_selected_state_keyboard(),
    const.USER_STATE_EDITING_FEEDBACK: _editing_feedback_state_keyboard(),
    const.USER_STATE_DELETING_FEEDBACK: _deleting_feedback_state_keyboard(),
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
                message = tt.REGISTERED
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
            text=tt.USE_BUTTONS,
            keyboard=get_keyboard(const.USER_STATE_MENU),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        if payload.get("action", "") == const.USER_ACTION_ADD_FEEDBACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_WRITING_FEEDBACK,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.WRITE_YOUR_FEEDBACK,
                keyboard=get_keyboard(const.USER_STATE_WRITING_FEEDBACK),
            )
        if payload.get("action", "") == const.USER_ACTION_VIEW_FEEDBACKS:
            message = vk.get_preview_feedbacks(
                session=session,
                user_id=user_id,
                page_num=0,
            )
            if not message:
                vk.answer_event(
                    session=session,
                    vk_id=vk_id,
                    peer_id=event.obj.peer_id,
                    event_id=event.obj.event_id,
                )
                vk.send_message(
                    session=session,
                    vk_id=vk_id,
                    text=tt.NAS_NO_FEEDBACKS,
                    keyboard=get_keyboard(const.USER_STATE_MENU),
                )
                return

            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_PREVIEW_PAGE,
                    "params": {
                        "page": 0,
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.SELECT_FB_HINT,
                keyboard=get_keyboard(const.USER_STATE_PREVIEW_PAGE),
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=message,
                keyboard=get_keyboard(const.USER_STATE_PREVIEW_PAGE),
            )


# USER_STATE_WRITING_FEEDBACK
def _writing_feedback_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        feedback = event.obj.message["text"]
        vk.create_feedback(
            session=session,
            user_id=user_id,
            feedback=feedback,
        )
        vk.update_user_state(
            session=session,
            user_id=user_id,
            new_state={
                "state": const.USER_STATE_MENU,
                "params": {},
            }
        )
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.FEEDBACK_REGISTERED,
            keyboard=get_keyboard(const.USER_STATE_MENU),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        if payload.get("action", "") == const.USER_ACTION_BACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_MENU,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_BACK_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )


def _convert_to_int(s) -> tp.Optional[int]:
    try:
        # user 1 is computer 0 number
        return int(s) - 1
    except:
        return None


# USER_STATE_PREVIEW_PAGE
def _preview_page_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        number = event.obj.message["text"]
        num = _convert_to_int(s=number)

        feedback = None
        if num is not None:
            feedback = vk.get_feedback_for_user(
                session=session,
                user_id=user_id,
                num=num,
            )
        
        if feedback is None:
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.INCORRECT_FB_NUMBER,
                keyboard=get_keyboard(const.USER_STATE_PREVIEW_PAGE),
            )
            return
        

        vk.update_user_state(
            session=session,
            user_id=user_id,
            new_state={
                "state": const.USER_STATE_FEEDBACK_SELECTED,
                "params": {
                    "feedback_id": feedback["id"],
                },
            }
        )
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=feedback["content"],
            keyboard=get_keyboard(const.USER_STATE_FEEDBACK_SELECTED),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        action = payload.get("action", "")
        if action == const.USER_ACTION_BACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_MENU,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_BACK_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )
        else:
            show_page = user_state["params"]["page"]
            if action == const.USER_ACTION_FIRST_PAGE_FB:
                show_page = 0
            elif action == const.USER_ACTION_PREV_PAGE_FB:
                show_page = max(0, show_page - 1)
            elif action == const.USER_ACTION_NEXT_PAGE_FB:
                max_page = vk.get_feedbacks_pages_count(
                    session=session,
                    user_id=user_id,
                )
                show_page = min(max_page - 1, show_page + 1)
            elif action == const.USER_ACTION_LAST_PAGE_FB:
                max_page = vk.get_feedbacks_pages_count(
                    session=session,
                    user_id=user_id,
                )
                show_page = max_page - 1

            message = vk.get_preview_feedbacks(
                session=session,
                user_id=user_id,
                page_num=show_page,
            )

            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_PREVIEW_PAGE,
                    "params": {
                        "page": show_page,
                    },
                }
            )
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
                keyboard=get_keyboard(const.USER_STATE_PREVIEW_PAGE),
            )


# USER_STATE_FEEDBACK_SELECTED
def _feedback_selected_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.USE_BUTTONS,
            keyboard=get_keyboard(const.USER_STATE_FEEDBACK_SELECTED),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        action = payload.get("action", "")
        if action == const.USER_ACTION_BACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_PREVIEW_PAGE,
                    "params": {
                        "page": 0,
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_BACK_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_PREVIEW_PAGE),
            )
        elif action == const.USER_ACTION_TO_MENU:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_MENU,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_MENU_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )
        elif action == const.USER_ACTION_EDIT_FEEDBACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_EDITING_FEEDBACK,
                    "params": {
                        "feedback_id": user_state["params"]["feedback_id"],
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            print(get_keyboard(const.USER_STATE_EDITING_FEEDBACK))
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.EDIT_FEEDBACK_HINT,
                keyboard=get_keyboard(const.USER_STATE_EDITING_FEEDBACK),
            )
        elif action == const.USER_ACTION_DELETE_FEEDBACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_DELETING_FEEDBACK,
                    "params": {
                        "feedback_id": user_state["params"]["feedback_id"],
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.DELETE_CONFIRMATION,
                keyboard=get_keyboard(const.USER_STATE_DELETING_FEEDBACK),
            )


# USER_STATE_EDITING_FEEDBACK
def _edeting_feedback_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        feedback = event.obj.message["text"]
        vk.update_feedback(
            session=session,
            feedback_id=user_state["params"]["feedback_id"],
            content=feedback,
        )
        vk.update_user_state(
            session=session,
            user_id=user_id,
            new_state={
                "state": const.USER_STATE_MENU,
                "params": {},
            }
        )
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.FEEDBACK_UPDATED,
            keyboard=get_keyboard(const.USER_STATE_MENU),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        action = payload.get("action", "")
        if action == const.USER_ACTION_BACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_FEEDBACK_SELECTED,
                    "params": {
                        "feedback_id": user_state["params"]["feedback_id"],
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_BACK_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_FEEDBACK_SELECTED),
            )
        elif action == const.USER_ACTION_TO_MENU:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_MENU,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_MENU_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )


# USER_STATE_DELETING_FEEDBACK
def _deleting_feedback_process_vk(session, event: EventType, user_state: tp.Dict, user_id: tp.Optional[int], vk_id: int):
    # message from user
    if event.type == VkBotEventType.MESSAGE_NEW:
        vk.send_message(
            session=session,
            vk_id=vk_id,
            text=tt.USE_BUTTONS,
            keyboard=get_keyboard(const.USER_STATE_DELETING_FEEDBACK),
        )
    # keyboard callback
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        if payload.get("type", "") != "custom":
            return
        action = payload.get("action", "")
        if action == const.USER_ACTION_BACK:
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_FEEDBACK_SELECTED,
                    "params": {
                        "feedback_id": user_state["params"]["feedback_id"],
                    },
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.RETURN_BACK_EXPLAIN,
                keyboard=get_keyboard(const.USER_STATE_FEEDBACK_SELECTED),
            )
        elif action == const.USER_ACTION_CONFIRM_DELETE_FB:
            vk.delete_feedback(
                session=session,
                feedback_id=user_state["params"]["feedback_id"],
            )
            vk.update_user_state(
                session=session,
                user_id=user_id,
                new_state={
                    "state": const.USER_STATE_MENU,
                    "params": {},
                }
            )
            vk.answer_event(
                session=session,
                vk_id=vk_id,
                peer_id=event.obj.peer_id,
                event_id=event.obj.event_id,
            )
            vk.send_message(
                session=session,
                vk_id=vk_id,
                text=tt.FB_DELETED,
                keyboard=get_keyboard(const.USER_STATE_MENU),
            )


STATE_PROCESS_MAP = {
    const.USER_STATE_START: _start_process_vk,
    const.USER_STATE_MENU: _menu_process_vk,
    const.USER_STATE_WRITING_FEEDBACK: _writing_feedback_process_vk,
    const.USER_STATE_PREVIEW_PAGE: _preview_page_process_vk,
    const.USER_STATE_FEEDBACK_SELECTED: _feedback_selected_process_vk,
    const.USER_STATE_EDITING_FEEDBACK: _edeting_feedback_process_vk,
    const.USER_STATE_DELETING_FEEDBACK: _deleting_feedback_process_vk,
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
