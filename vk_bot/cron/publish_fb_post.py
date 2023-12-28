from dotenv import load_dotenv
import os

from common import text_templates as tt
from common import const
from vk_bot import vk

load_dotenv()
VK_PEER_ID = -os.environ["VK_GROUP_ID"]

session = vk.get_session()


