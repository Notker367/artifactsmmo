import action
import info
from main import wait_cooldown_from_response


async def go_to(coordinates, character_name):
    if info.get_position(character_name) == coordinates:
        print(f"{character_name} - already in position now")
        return

    response_move = action.move(coordinates, character_name)
    if response_move.status_code == 200:
        print(f"{character_name} Move code: {response_move.status_code}")
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

#Битвы
#__________________________________________________________________________
async def chicken_farm(character_name):
    await go_to((0,1), character_name) # chicken

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
    'ash'          : (-1, 0),
    'copper'            : (2,  0),

}

wood_info = {
    'ash'          : 6,

    'craft'        : (-2,-3)
}

bars_info = {
    'copper'            : 6,
    'iron'              : 6,

    'craft'         : (1, 5)

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
        postfix_inv = "_ore"
        postfix_craft = ""
        #                         to_item_code = target из def gathering(character_name, target)
#                           Название в инвентаре           Коэффициент крафта из инфо
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# Название в инвентаре
        craft_coof = bars_info[to_item_code]       # Коэффициент крафта из инфо


    elif to_item_code in wood_info:
        await go_to(wood_info['craft'], character_name)
        postfix_craft = "_plank"
        postfix_inv = "_wood"
        #                      to_item_code = target из def gathering(character_name, target)
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# кол-во по Название в инвентаре
        craft_coof = wood_info[to_item_code]       # Коэффициент крафта из инфо


    else:
        print(f"{character_name} - ERROR crafting item_code !!!")
        return

    can_craft = count_in_inv // craft_coof # Счет сколько можем скрафтить

    response = action.craft(character_name, to_item_code+postfix_craft, can_craft, debug=False)
    if response.status_code == 200:
        print(f"{character_name} Craft code: {response.status_code} craft {can_craft} {to_item_code+postfix_craft}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])
        print(f"{character_name} - not can craft {count_in_inv} {to_item_code+postfix_inv} -> {can_craft} {to_item_code+postfix_craft}")


