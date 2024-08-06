from dotenv import load_dotenv
import requests
import os

# Загрузка переменных из файла .env
load_dotenv()

# Получение переменных
token = os.getenv('TOKEN')



def move(coordinates, character_name, debug=False):
    """
    200-The character has moved successfully.

    404-Map not found.

    486-Character is locked. Action is already in progress.

    490-Character already at destination.

    498-Character not found.

    499-Character in cooldown.
    :param coordinates: (x , y)
    :param character_name:
    :param debug:
    :return: status_code
    """
    postfix = 'action/move'
    url = f"https://api.artifactsmmo.com/my/{character_name}/{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    data = {
        "x": coordinates[0],
        "y": coordinates[1]
    }

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.status_code)
        print(response.json())

    return response



def deposit_bank(character_name, item_code, item_quantity, debug=False):
    """

    :param item_code: str item name
    :param item_quantity: int item quantity
    :param character_name:
    :param debug:
    :return:
    """

    postfix = 'action/bank/deposit'
    url = f"https://api.artifactsmmo.com/my/{character_name}/{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {
        "code": item_code,
        "quantity": item_quantity
    }

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response



def deposit_bank_gold(character_name, item_quantity, debug=False):
    """

    :param item_quantity: int item quantity
    :param character_name:
    :param debug:
    :return:
    """

    postfix = 'action/bank/deposit/gold'
    url = f"https://api.artifactsmmo.com/my/{character_name}/{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {
        "quantity": item_quantity
    }

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response


def withdraw_bank(character_name, item_code, item_quantity, debug=False):
    """

    :param item_code: str item name
    :param item_quantity: int item quantity
    :param character_name:
    :param debug:
    :return:
    """

    name = character_name
    postfix = f'/my/{name}/action/bank/withdraw'
    url = f"https://api.artifactsmmo.com{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {
        "code": item_code,
        "quantity": item_quantity
    }

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response


def fight(character_name, debug=False):
    """

    :param character_name:
    :param debug:
    :return:
    """

    postfix = 'action/fight'
    url = f"https://api.artifactsmmo.com/my/{character_name}/{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {}

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response


def gathering(name, debug=False):
    """

    :param name:
    :param debug:
    :return:
    """
    postfix = f'/my/{name}/action/gathering'
    url = f"https://api.artifactsmmo.com{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {}

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response



def craft(name, item_code, quantity, debug=False):
    """

    :param quantity: int
    :param item_code: str
    :param name: str
    :param debug: bool
    :return:
    """
    postfix = f'/my/{name}/action/crafting'
    url = f"https://api.artifactsmmo.com{postfix}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    data = {
        "code": item_code,
        "quantity": quantity
    }

    response = requests.post(url, headers=headers, json=data)

    if debug:
        print(name, item_code, quantity, debug)
        print(response.request)
        print(response.status_code)
        print(response.json())

    return response