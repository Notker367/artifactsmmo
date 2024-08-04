import action
import asyncio

import api.world_info
import info

from tqdm import tqdm

from dotenv import load_dotenv
import os

# Загрузка переменных из файла .env
load_dotenv()

# Получение переменных
char_I = os.getenv('CHARACTER_ONE')
char_II = os.getenv('CHARACTER_TWO')
char_III = os.getenv('CHARACTER_THREE')
char_IV = os.getenv('CHARACTER_FOUR')
char_V = os.getenv('CHARACTER_FIVE')


# Указываем, для каких персонажей отображать прогресс-бар
show_progress_bars = {
    char_I: True,
    char_II: False,
    char_III: False,
    char_IV: False,
    char_V: False
}


async def wait_cooldown_from_response(character_name):
    delay = api.world_info.get_character_info(character_name).json()['data']['cooldown']

    show_progress = show_progress_bars.get(character_name, False)

    if show_progress:
        for _ in tqdm(range(delay), desc=f"{character_name} cooldown"):
            await asyncio.sleep(1)
    else:
        await asyncio.sleep(delay)


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

# Персонаж: 'Работа'
professions = {
    char_I      : 'farm',
    char_II     : 'farm',
    char_III    : 'farm',
    char_IV     : 'farm',
    char_V      : 'farm'
}

# 'Работа' : Функция
works = {
    'farm': chicken_farm,
#    'b': case_b,
#    'c': case_c
}

def default_case(value):
    print(f"Error works case {value} !!!")


async def task(character_name):
    print(f"Starting task for {character_name}")
    work_function = works.get(professions.get(character_name), default_case)
    await work_function(character_name)
    print(f"Finished task for {character_name}")

characters = [
    char_I,
    char_II,
    char_III,
    char_IV,
    char_V
]
tasks = {}

async def main():
    while True:
        for character in characters:
            if character not in tasks or tasks[character].done():
                tasks[character] = asyncio.create_task(task(character))
        await asyncio.sleep(1)  # Маленькая задержка, чтобы не перегружать цикл

if __name__ == "__main__":
    asyncio.run(main())