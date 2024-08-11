import action
import api.world_info

"""
    +'Miner'             : 'mining',
    +'Woodcutter'        : 'woodcutting',
    +'Fisher'            : 'fishing',
    +'Weaponcrafter'     : 'weaponcrafting',
    +'Gearcrafter'       : 'gearcrafting',
    +'Jewelrycrafter'    : 'jewelrycrafting',
    +'Cooker'            : 'cooking',
    'Fighter'           : 'fighting' #########
"""

def formater(data):
    print(data)

    drops = data.get('drops', None)

    if drops is not None:
        skill = 'fighting'
    elif data['craft'] is not None:         # weaponcrafting gearcrafting jewelrycrafting cooking
        skill = data['craft']['skill']
    else:                                   # mining woodcutting fishing fighting='mob'
        skill = data['subtype']

    if skill == 'mob':
        skill = 'fighting'

    data['for_work'] = skill
    return {data['code'] : data}


def about(target):
    """
    and add data['for_work'] = skill
    :param target: 'code' (name item or mob)
    :return: dict {name : info from data.item or data}
    """
    response = api.world_info.get_item_info(target) # item

    if response.status_code == 200:
        data = response.json()['data']['item']
    else:
        response = api.world_info.get_item_monsters(target) # mob
        if response.status_code == 200:
            data = response.json()['data']
        else:
            print('ERROR info.about ', target)
            return

    data = formater(data)

    return data[target]

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


def get_recept(item_code):
    """
    Получает текущую позицию персонажа по его имени.

    :param item_code: name to craft item
    :return: {name : quantity}, str
    :rtype: Tuple(str, int)
    """
    data = api.world_info.get_item_info(item_code).json()['data']['item']

    craft_info = data['craft']

    skill = craft_info['skill']

    craft_dict = {item['code'] : item['quantity'] for item in craft_info['items']}

    return craft_dict, skill


def get_item_dict(character_name, debug=False):
    """

    :param character_name:
    :param debug:
    :return: {item_name : quantity}
    """
    character_info = api.world_info.get_character_info(character_name).json()["data"]

    items_list = character_info["inventory"]

    items_dict = {item['code'] : item['quantity'] for item in items_list if item['quantity'] != 0}

    if debug:
        print(items_dict)

    return items_dict

def get_inventory_max_items(character_name, debug=False):
    """

    :param character_name:
    :param debug:
    :return: {item_name : quantity}
    """
    character_info = api.world_info.get_character_info(character_name).json()["data"]

    inventory_max_items = character_info["inventory_max_items"]

    return inventory_max_items

def get_available_gold(character_name):
    character_info = api.world_info.get_character_info(character_name).json()["data"]

    available_gold = character_info["gold"]

    return available_gold

def get_workshop(workshop_code):
    """
    :param workshop_code:
    :return:
    """
    if workshop_code not in ['woodcutting', 'cooking', 'weaponcrafting', 'gearcrafting', 'jewelrycrafting','mining']:
        print(f"get_workshop ERROR workshop_code = {workshop_code}")
        return

    workshops_info = api.world_info.get_all_maps('workshop').json()
    workshop_dict = { workshop['content']['code'] : (workshop['x'], workshop['y'])
                      for workshop
                      in workshops_info['data'] }

    return workshop_dict[workshop_code] if workshop_code != 'all' else workshops_info


def get_monster_from_drop(item_code):
    """
    :param item_code: str
    :return:
    """
    response = api.world_info.get_all_monsters(item_code)
    data = response.json()['data']
    monster = data['code']

    pass

"""    if workshop_code not in ['woodcutting', 'cooking', 'weaponcrafting', 'gearcrafting', 'jewelrycrafting','mining']:
        print(f"get_workshop ERROR workshop_code = {workshop_code}")
        return

    workshops_info = api.world_info.get_all_maps('workshop').json()
    workshop_dict = { workshop['content']['code'] : (workshop['x'], workshop['y'])
                      for workshop
                      in workshops_info['data'] }

    return workshop_dict[workshop_code] if workshop_code != 'all' else workshops_info"""


def get_bank_items(items_list):
    """

    :param items_list: list[]
    :return: {str : int}
    """
    items_dict = {}
    for item_name in items_list:
        response = api.world_info.get_bank_items(item_code=item_name).json()
#        data = response['data']

        if "error" in response:
            print(f"WARNING get_bank_items for {item_name}"
                  f"{response}" )
            return {'code': item_name, 'quantity': 0}

        if response['total'] > response['size']:
            print(f"WARNING - size in get_bank_items !!!")

        quantity = response['data'][0]['quantity']
        items_dict[item_name] = quantity

    return items_dict


