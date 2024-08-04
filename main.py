import action
import time
import threading

import api.world_info
import info
from tqdm import tqdm



RUN=False



def wait_cooldown_from_response(character_name):
    delay = api.world_info.get_character_info(character_name).json()['data']['cooldown']

    print(f'{character_name} cooldown: {delay} seconds')

    #Прогресс бар
    for _ in tqdm(range(delay), desc="Cooldown", unit="s"):
        time.sleep(1)

def go_to(x,y, character_name):
    if info.get_position(character_name) == (x, y):
        print(f"{character_name} already in position now")
        return

    response_move = action.move(x, y, character_name)
    if response_move.status_code == 200:
        print(f"Move code: {response_move.status_code}")
    else:
        print(response_move.json()['error'])

    wait_cooldown_from_response(character_name)


def all_in_bank(character_name):
    go_to(4,1, character_name) # bank

    item_dict = info.get_item_dict(character_name)

    for name, quantity in item_dict.items():
        action.deposit_bank(character_name, name, quantity)
        print(f"deposit {quantity} - {name} in bank")
        wait_cooldown_from_response(character_name)



def chicken_farm(character_name="Pivos"):
    global RUN
    while RUN:
        go_to(0,1, character_name) # chicken

        response_fight = action.fight(character_name,debug=False)
        if response_fight.status_code == 200:
            print(f"Fight code: {response_fight.status_code}")
        elif response_fight.status_code == 497:
            print(f"inventory {character_name} full")
            all_in_bank(character_name)
            print("all_in_bank completed")
        else:
            print(response_fight.json()['error'])

        wait_cooldown_from_response(character_name)



# Функция для управления потоком
def manage_farming():
    global RUN
    farm_thread = None

    command = ""
    while command not in ["exit", "q"]:
        command = input("Enter command (start/stop/exit): ").strip().lower()

        if command in ["start", "s"] and not RUN:
            RUN = True
            farm_thread = threading.Thread(target=chicken_farm("Other"))
            farm_thread.start()

        elif command in ["stop", "p"]:
            RUN = False
            if farm_thread:
                farm_thread.join()

        elif command in ["exit", "q"]:
            RUN = False
            if farm_thread:
                farm_thread.join()

manage_farming()