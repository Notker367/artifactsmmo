import db
import api.world_info
import cache_manager

"""
    +'Miner'             : 'mining',
    +'Woodcutter'        : 'woodcutting',
    +'Fisher'            : 'fishing',
    +'Weaponcrafter'     : 'weaponcrafting',
    +'Gearcrafter'       : 'gearcrafting',
    +'Jewelrycrafter'    : 'jewelrycrafting',
    +'Cooker'            : 'cooking',
    +'Fighter'            : 'fighting' #########
"""
def add_drops_from_code(drops_list, code):
    for item in drops_list:
        code_item = item['code']
        cache_manager.add_static_item(code_item+'_drop',  code)


def formater(data):
    print(data)
    craft = False

    drops = data.get('drops', None)
    skill = data.get('skill', None)
    craft = data.get('craft', None)
    is_spot = data.get('skin',None)

    if (drops is not None) and (skill is None):                   # fighting monster
        print('111111111111111111')
        skill = 'fighting'
        monster = data['code']
        add_drops_from_code(drops,monster)
        locations = get_positions_monster(monster)
        location = locations[0]

    elif (drops is not None) and (skill is not None):               #  spot item
        print('22222222222222')
        skill = skill
        spot = data['code']
        add_drops_from_code(drops,spot)
        locations = get_positions_spot(spot)
        location = locations[0]

    elif craft is not None:         # ['woodcutting', 'cooking', 'weaponcrafting', 'gearcrafting', 'jewelrycrafting','mining']
        print('3333333333333333333333')
        craft = True
        recept, skill = get_recept(data['code'])
        workshop_location = get_workshop(skill)
        data['craft']['recept'] = recept
        data['craft']['location'] = workshop_location
        location = (4, 1) #mock bank

    elif is_spot is not None:               # spot loc
        print('44444444444444444')
        location = [data['x'],data['y']]
        data['code'] = data['content']['code']

    else:                                   # mining woodcutting fishing fighting='mob'
        skill = data['subtype']
        print('55555555555555555555555')

        if skill == 'mob':                      # fighting resource
            print('66666666666666666666')
            skill = 'fighting'
            item_code = data['code']

            monster = add_to_drops(item_code, db.famous_monsters)
            locations = get_positions_monster(monster)
            location = locations[0]

        elif skill in ['woodcutting', 'fishing', 'mining']: # geting res
            print('77777777777777777777')
            item_code = data['code']

            spot = add_to_drops(item_code, db.famous_spots)
            locations = get_positions_spot(spot)
            location = locations[0]

        else:
            location = (0,0) # mock




    data['location'] = location
    data['need_craft'] = craft
    data['for_work'] = skill
    print('end data ', data)
    return {data['code'] : data}


def add_to_drops(item_code, db_from):
    know = cache_manager.have_in_cache(item_code + '_drop') # have_in_cache?
    if not know:
        for target_code in db_from:
            if cache_manager.have_in_cache(target_code):
                continue
            else:
                cache_manager.check_in_cache(target_code)
    need = cache_manager.check_in_cache(item_code + '_drop')
    return need


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

        response = api.world_info.get_monster(target) # mob
        if response.status_code == 200:
            data = response.json()['data']
        else:

            response = api.world_info.get_resource(target)  # res
            if response.status_code == 200:
                data = response.json()['data']
            else:

                response = api.world_info.get_all_maps(content_code=target, content_type='resource') # spot
                if response.status_code == 200:
                    data = response.json()['data'][0]
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

def get_positions_monster(monster):
    """
    Получает текущую позицию персонажа по его имени.

    :param monster: Имя персонажа, для которого требуется получить текущую позицию.
    :type monster: Str
    :return: Список с текущими координатами [x,y] монстра.
    :rtype: List[[x,y],[x,y]]
    """
    response = api.world_info.get_all_maps(content_code=monster, content_type='monster')
    data = response.json()['data']

    positions = []
    for info in data:
        now_position_x = info['x']
        now_position_y = info['y']
        positions += [[now_position_x, now_position_y]]

    return positions

def get_positions_spot(spot):
    """
    Получает текущую позицию персонажа по его имени.

    :param spot: Имя spot, для которого требуется получить текущую позицию.
    :type spot: Str
    :return: Список с текущими координатами [x,y] spot.
    :rtype: List[[x,y],[x,y]]
    """
    response = api.world_info.get_all_maps(content_code=spot, content_type='resource')
    data = response.json()['data']

    positions = []
    for info in data:
        now_position_x = info['x']
        now_position_y = info['y']
        positions += [[now_position_x, now_position_y]]

    return positions

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


