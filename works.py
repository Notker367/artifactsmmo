import action
import info
from main import wait_cooldown_from_response


async def go_to(x,y, character_name):
    if info.get_position(character_name) == (x, y):
        print(f"{character_name} already in position now")
        return

    response_move = action.move(x, y, character_name)
    if response_move.status_code == 200:
        print(f"Move code: {response_move.status_code}")
    else:
        print(response_move.json()['error'])

    await wait_cooldown_from_response(character_name)


async def all_in_bank(character_name):
    await go_to(4,1, character_name) # bank

    item_dict = info.get_item_dict(character_name)

    for name, quantity in item_dict.items():
        action.deposit_bank(character_name, name, quantity)
        print(f"deposit {quantity} - {name} in bank")
        await wait_cooldown_from_response(character_name)


async def chicken_farm(character_name):
    await go_to(0,1, character_name) # chicken

    response_fight = action.fight(character_name,debug=False)
    if response_fight.status_code == 200:
        print(f"Fight code: {response_fight.status_code}")
    elif response_fight.status_code == 497:
        print(f"inventory {character_name} full")
        await all_in_bank(character_name)
        print("all_in_bank completed")
    else:
        print(response_fight.json()['error'])

    await wait_cooldown_from_response(character_name)
