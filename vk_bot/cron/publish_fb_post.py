import time
import datetime

from common import text_templates as tt
from vk_bot import vk


session = vk.get_session()
user_session = vk.get_user_session()

fb_ids = vk.get_feedbacks_to_post(count=1)

if fb_ids:
    fb_id = fb_ids[0]

    fb_object = vk.get_feedback_by_id(
        session=session,
        feedback_id=fb_id,
    )
    feedback = fb_object["feedback"]
    attachments = fb_object["attachments"]
    author_id = feedback["user_id"]
    user = vk.get_user_by_id(
        session=session,
        user_id=author_id,
    )

    post_content = tt.POST_TEMPLATE_VK.format(
        content=feedback["content"],
        vk_tag=user["vk_tag"],
    )

    time_to_post = datetime.datetime.now() + datetime.timedelta(hours=1)
    unix_time = int(time.mktime(time_to_post.timetuple()))

    vk.create_post(
        user_session=user_session,
        text=post_content,
        attachment=attachments,
        publish_date=unix_time,
    )
    vk.mark_fb_posted(
        feedback_id=feedback["id"],
    )
