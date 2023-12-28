from vk_api import VkApi
from vk_api.upload import VkUpload
from vk_api.utils import get_random_id
import requests
from io import BytesIO


TOKEN = 'vk1.a.s5h3QG51IQm79fSe9b5SSiuRPf7_MwbsvE9lsBEIuyhPZ6ocjo31KZC4P3f4nYbQKtia8w5sj5xhHF7nOFA8LJY16YMBin8NxouEu55G1IKOUVP1w1xq9jebhCXmKklWon_VpDNlg9Sj3oGvTk4gCUMwUxaijNYiC_FtqPvG1qFsO_TSekjuntD8-SHYPeNrSc4YSscHXrji9tKwdwZY4A'
PEER_ID = 326743647
URL = 'https://sun9-41.userapi.com/impf/4r0V5b8DfMkGOxg-i5qQ7gFnI1KOoh_ZfaHPmg/zU4cai0aXO0.jpg?size=436x604&quality=96&sign=5387e9b6343aa925cf1d198e4ab526a4&c_uniq_tag=phyTmLOuC5igE2YNpT7RmZOtzdh7lUCl3jicttrQXvY&type=album'


def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)

    response = upload.photo_messages(f)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )


def main():
    vk_session = VkApi(token=TOKEN)
    vk = vk_session.get_api()
    upload = VkUpload(vk)

    send_photo(vk, PEER_ID, *upload_photo(upload, URL))


if __name__ == '__main__':
    main()
