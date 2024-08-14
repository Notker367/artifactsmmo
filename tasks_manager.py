from dotenv import load_dotenv
import os

"""
    +'Miner'             : 'mining',
    +'Woodcutter'        : 'woodcutting',
    +'Fisher'            : 'fishing',
    +'Weaponcrafter'     : 'weaponcrafting',
    +'Gearcrafter'       : 'gearcrafting',
    +'Jewelrycrafter'    : 'jewelrycrafting',
    +'Cooker'            : 'cooking',
    +'Fighter'           : 'fighting' #########
"""


# Загрузка переменных из файла .env
load_dotenv()


# Получение переменных
char_I = os.getenv('CHARACTER_ONE')
char_II = os.getenv('CHARACTER_TWO')
char_III = os.getenv('CHARACTER_THREE')
char_IV = os.getenv('CHARACTER_FOUR')
char_V = os.getenv('CHARACTER_FIVE')


start_tasks = [
    ('mushmush_wizard_hat', 20)
]


task_board= {
#   'skill' : [task, task, task],
    'gearcrafting' : [('mushmush_wizard_hat', 20)]
}

default_tasks = {
#    char_N    : [('code', 'quantity'),('str', 'int')],
    char_I      : [
        ('skeleton_bone', 1)
    ],
    char_II     : [
        ('cooked_bass', 1),
    ],
    char_III    :  [
        ('mushmush_wizard_hat', 1)
    ],
    char_IV     : [
        ('steel', 1)
    ],
    char_V      : [
        ('hardwood_plank', 1)
    ],
}


def add_to_task_board(target_code, quantity=1, non_stop=False):
    if non_stop:
        quantity *= 100
    elif quantity <= 0:
        return

    from cache_manager import check_in_cache  # Перемещаем импорт сюда

    skill = check_in_cache(target_code)['for_work']
    task = (target_code, quantity)
    task_board[skill] = [task] + task_board.get(skill, [])
    view_task_board()


def view_task_board():
    print('_____________TASKS IN BOARD_____________')
    if not task_board:
        print("No tasks available.")
    else:
        for prof in task_board:
            print(f"{prof}:")
            for task in task_board[prof]:
                task_name, quantity = task
                print(f"  - {task_name}: {quantity} units")
    print('________________________________________')


async def get_task(character_name):
    """

    :param character_name:
    :return: task ('code', 'quantity') or False
    """
#    global have_tasks
    view_task_board()
    from db import char_professions,professions_dict

    my_professions = char_professions[character_name]     #   'char_': ['profession', 'profession', 'profession']
    my_actual_task = []
    for profession in my_professions:
        skill = professions_dict[profession]
        have_tasks = task_board.get(skill, [])
        my_actual_task += [have_tasks]
        if not have_tasks:
            continue                                # default case

        else:
            first_task = have_tasks.pop(0)
            print(f'{character_name} get task {first_task[1]} - {first_task[0]}')
            return first_task

    return False

async def add_default_task_board(character_name):
    await get_task(character_name)
    me_tasks = default_tasks[character_name]
    for task in me_tasks:
        add_to_task_board(task[0],task[1],non_stop=True)


async def add_start_tasks_board():
    tasks = start_tasks
    print(tasks)
    for task in tasks:
        add_to_task_board(task[0],task[1])

# add_start_tasks_board()

# задача (что, сколько) -> профессия -> персонаж -> условия -> добавить в список -> проверка списка -> дефолт действие

