import action
import info
from main import wait_cooldown_from_response

# Функция перемещения персонажа к указанным координатам
async def go_to(coordinates, character_name):
    if info.get_position(character_name) == coordinates:
        print(f"{character_name} - already in position now")
        return

    response_move = action.move(coordinates, character_name)
    if response_move.status_code == 200:
        print(f"{character_name} Move code: {response_move.status_code}")

    elif response_move.status_code == 499:
        await wait_cooldown_from_response(character_name)
        await go_to(coordinates, character_name)
        print(f'WARNING {character_name}  go_to - 499 !!!!!!')

    else:
        print(response_move.json()['error'])

    await wait_cooldown_from_response(character_name)

#Экономика
#__________________________________________________________________________
async def all_in_bank(character_name):
    await go_to((4,1), character_name) # bank

    item_dict = info.get_item_dict(character_name)

    for name, quantity in item_dict.items():
        action.deposit_bank(character_name, name, quantity)
        print(f"{character_name} deposit {quantity} - {name} in bank")
        await wait_cooldown_from_response(character_name)


async def craft_from_bank(character_name, target, need_craft = 999):
    recept, skill  = info.get_recept(target) # {name : quantity}, skill

    my_item = info.get_item_dict(character_name)

    recept_name_list = list(recept.keys())
    bank_item = info.get_bank_items(recept_name_list) # {str : int}

    inv_max = info.get_inventory_max_items(character_name)

    can_craft = need_craft

    for item in recept_name_list:
        in_inv = my_item.get(item, 0)
        in_bank = bank_item.get(item, 0)
        in_recept = recept.get(item, 0)

        have_items_for_craft = (in_inv + in_bank) // in_recept

        if have_items_for_craft == 0:
            print(f"{character_name} not can craft {target} needed more {item}")
            return

        if have_items_for_craft < can_craft:
            can_craft = have_items_for_craft

    need_slots_for_one = 0

    for item, quantity_need in recept.items():
        need_slots_for_one += quantity_need

    if need_slots_for_one * can_craft > inv_max:
        can_craft = inv_max // need_slots_for_one

    await all_in_bank(character_name)

    for item, quantity in recept.items():
        print(f'{character_name} me need {quantity * can_craft} {item} from bank')
        action.withdraw_bank(character_name, item, quantity * can_craft)
        await wait_cooldown_from_response(character_name)

    await go_to(info.get_workshop(skill), character_name) # go workshop

    response = action.craft(character_name, target, can_craft)

    if response.status_code == 200:
        print(
            f"{character_name} Craft code: {response.status_code} craft {can_craft} {target}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])
        print(f"{character_name} - not can craft {recept_name_list} -> {can_craft} {target}")

    await all_in_bank(character_name)

#Битвы
#__________________________________________________________________________
monsters = {
    'chicken'       :   (0,  1),
    'blue_slime'    :   (2, -1),
    'red_slime'     :   (1, -1),
    'green_slime'   :   (0, -1),
    'yellow_slime'  :   (4, -1),
    'cow'           :   (0,  2),
    'wolf'          :   (-2, 1),
    'mushmush'      :   (5,  3),
    'flying_serpent':   (5,  4),

}
async def farm(character_name, target):
    await go_to(monsters[target], character_name)

    response = action.fight(character_name,debug=False)
    if response.status_code == 200:
        print(f"{character_name} Fight code: {response.status_code}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])



#Добыча
#__________________________________________________________________________
resources = {
    # Метал
    'copper'       : (2,  0),
    'iron'         : (1,  7),
    # Дерево
    'ash'          : (-1, 0),
    'spruce'       : (-2, 5),
    # Рыба
    'gudgeon'      : (4,  2),
    'shrimp'       : (5,  2),
}

wood_info = {
    'ash'          : 6,
    'spruce'       : 6,

    'craft'        : (-2,-3)
}

bars_info = {
    'copper'       : 6,
    'iron'         : 6,

    'craft'        : (1, 5)

}

fish_info = {
    'gudgeon'      : 1,
    'shrimp'       : 1,

    'craft'        : (1, 1)
}

async def gathering(character_name, target):

    await go_to(resources[target], character_name)

    response = action.gathering(character_name)
    if response.status_code == 200:
        print(f"{character_name} Gathering code: {response.status_code}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")

        await go_crafting(character_name, target)
        print(f"{character_name} - go_crafting completed")

        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])




async def go_crafting(character_name, to_item_code):

    item_dict = info.get_item_dict(character_name) # Инвентарь

    if to_item_code in bars_info:
        await go_to(bars_info['craft'], character_name)
        postfix_craft = ""
        prefix_craft = ""
        postfix_inv = "_ore"
        #                         to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# Название в инвентаре
        craft_coof = bars_info[to_item_code]       # Коэффициент крафта из инфо


    elif to_item_code in wood_info:
        await go_to(wood_info['craft'], character_name)
        postfix_craft = "_plank"
        prefix_craft = ""
        postfix_inv = "_wood"
        #                      to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# кол-во по Название в инвентаре
        craft_coof = wood_info[to_item_code]       # Коэффициент крафта из инфо


    elif to_item_code in fish_info:
        await go_to(fish_info['craft'], character_name)
        postfix_craft = ""
        prefix_craft = "cooked_"
        postfix_inv = ""
        #                      to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# кол-во по Название в инвентаре
        craft_coof = fish_info[to_item_code]       # Коэффициент крафта из инфо


    else:
        print(f"{character_name} - ERROR crafting item_code !!!")
        return

    can_craft = count_in_inv // craft_coof # Счет сколько можем скрафтить

    response = action.craft(character_name, prefix_craft+to_item_code+postfix_craft, can_craft, debug=False)
    if response.status_code == 200:
        print(f"{character_name} Craft code: {response.status_code} craft {can_craft} {prefix_craft+to_item_code+postfix_craft}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])
        print(f"{character_name} - not can craft {count_in_inv} {to_item_code+postfix_inv} -> {can_craft} {to_item_code+postfix_craft}")


