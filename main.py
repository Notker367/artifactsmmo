import asyncio

import api.world_info

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

# Функция ожидания окончания кулдауна с возможностью отображения прогресс-бара
async def wait_cooldown_from_response(character_name):
    # Получаем время задержки (кулдаун) из информации о персонаже
    delay = api.world_info.get_character_info(character_name).json()['data']['cooldown']

    # Проверяем, нужно ли отображать прогресс-бар для данного персонажа
    show_progress = show_progress_bars.get(character_name, False)

    if show_progress:
        # Отображаем прогресс-бар
        for _ in tqdm(range(delay), desc=f"{character_name} cooldown"):
            await asyncio.sleep(1)
    else:
        # Ждем окончания кулдауна без отображения прогресс-бара
        await asyncio.sleep(delay)

# Персонаж: 'Работа'
professions = {
    char_I:     'wolf',
    char_II:    'craft_from_bank',
    char_III:   'cow',
    char_IV:    'iron',
    char_V:     'spruce'
}

# Функция по умолчанию для обработки неизвестных работ
async def default_case(value):
    print(f"Error works case {value} !!!")
    await asyncio.sleep(30)

# Основная задача для персонажа
async def task(character_name):
    print(f"Starting task for {character_name}")

    from works import farm,gathering,craft_from_bank  # Отложенный импорт

    # 'Работа': Функция
    works_dict = {
        'craft_from_bank'   : (craft_from_bank,        'cooked_chicken'),

        'farm_chicken'      : (farm,        'chicken'),         #1
        'farm_red_slime'    : (farm,        'red_slime'),       #7
        'farm_blue_slime'   : (farm,        'blue_slime'),      #6
        'farm_green_slime'  : (farm,        'green_slime'),     #4
        'yellow_slime'      : (farm,        'yellow_slime'),    #2
        'cow'               : (farm,        'cow'),             #8
        'wolf'              : (farm,        'wolf'),            #15

        'copper'            : (gathering,   'copper'),
        'iron'              : (gathering,   'iron'),
        'ash'               : (gathering,   'ash'),
        'gudgeon'           : (gathering,   'gudgeon'),
        'shrimp'            : (gathering,   'shrimp'),
        'spruce'            : (gathering,   'spruce')
    }

    work_function,add_param = works_dict.get(professions.get(character_name), default_case)
    if add_param:
        await work_function(character_name,target=add_param)
    else:
        await work_function(character_name)
    print(f"Finished task for {character_name}")

# Список персонажей
characters = [
    char_I,
    char_II,
    char_III,
    char_IV,
    char_V
]

# Словарь для хранения задач
tasks = {}

# Основная функция
async def main():
    while True:
        for character in characters:
            if character not in tasks or tasks[character].done():
                tasks[character] = asyncio.create_task(task(character))
        await asyncio.sleep(1)  # Маленькая задержка, чтобы не перегружать цикл

if __name__ == "__main__":
    asyncio.run(main())
