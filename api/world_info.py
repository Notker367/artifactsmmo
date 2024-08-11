from dotenv import load_dotenv
import requests
import os

# Загрузка переменных из файла .env
load_dotenv()

# Получение переменных
token = os.getenv('TOKEN')



def get_character_info(character_name):
    """

    :param character_name:
    :return:
    """

    url = f"https://api.artifactsmmo.com/characters/{character_name}"

    response = requests.get(url)

    return response


def get_item_info(code):
    """

    :param code: item code
    :return: response
    """

    url = f"https://api.artifactsmmo.com/items/{code}"

    response = requests.get(url)

    return response

def get_item_monsters(code):
    """

    :param code: monsters code
    :return: response
    """

    url = f"https://api.artifactsmmo.com/monsters/{code}"

    response = requests.get(url)

    return response


def get_all_maps(content_type, content_code=None, page=1, size=100 ):
    """

    :param content_type: monster resource workshop bank grand_exchange tasks_master
    :param content_code:
    :param page: 1
    :param size: 100
    :return: response
    """

    url = f"https://api.artifactsmmo.com/maps/"

    data = {
        'content_code' : content_code,
        'content_type' : content_type,
        'page'         : page,
        'size'         : size
    }

    response = requests.get(url, params=data)

    if response.json()['total'] >= size:
        print(f"WARNING - size in get_all_maps !!!")

    return response


def get_all_monsters(drop, max_level=None, min_level=None, page=1, size=100 ):
    """

    :param drop: item_code
    :param min_level: int
    :param max_level: int
    :param page: 1
    :param size: 100
    :return: response
    """

    url = f"https://api.artifactsmmo.com/monsters/"

    data = {
        'drop'          : drop,
        'max_level'     : max_level,
        'min_level'     : min_level,
        'page'          : page,
        'size'          : size
    }

    response = requests.get(url, params=data)

    if response.json()['total'] >= size:
        print(f"WARNING - size in get_all_monsters !!!")

    return response


def get_bank_items(item_code=None, page=1, size=100):
    url = f"https://api.artifactsmmo.com/my/bank/items"

    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {
        'item_code'    : item_code,
        'page'         : page,
        'size'         : size
    }

    response = requests.get(url, params=data, headers=headers)

    return response