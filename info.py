import action
import api.world_info
import api.world_info as w

def get_position(character_name):
    """
    Получает текущую позицию персонажа по его имени.

    :param character_name: Имя персонажа, для которого требуется получить текущую позицию.
    :type character_name: Str
    :return: Кортеж с текущими координатами (x, y) персонажа.
    :rtype: Tuple(int, int)
    """
    data = api.world_info.get_character_info(character_name).json()['data']

    now_position_x = data['x']
    now_position_y = data['y']

    return now_position_x,now_position_y


def get_item_dict(character_name, debug=False):
    character_info = api.world_info.get_character_info(character_name).json()["data"]

    items_list = character_info["inventory"]

    items_dict = {item['code'] : item['quantity'] for item in items_list if item['quantity'] != 0}

    if debug:
        print(items_dict)

    return items_dict


def get_available_gold(character_name):
    character_info = api.world_info.get_character_info(character_name).json()["data"]

    available_gold = character_info["gold"]

    return available_gold



