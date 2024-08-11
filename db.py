from dotenv import load_dotenv
from works import task_gathering, task_craft, task_farm
import os


# Загрузка переменных из файла .env
load_dotenv()

# Получение переменных
char_I = os.getenv('CHARACTER_ONE')
char_II = os.getenv('CHARACTER_TWO')
char_III = os.getenv('CHARACTER_THREE')
char_IV = os.getenv('CHARACTER_FOUR')
char_V = os.getenv('CHARACTER_FIVE')

professions_dict = {
#   'professions'       : 'skill',

    'Miner'             : 'mining',
    'Woodcutter'        : 'woodcutting',
    'Fisher'            : 'fishing',
    'Weaponcrafter'     : 'weaponcrafting',
    'Gearcrafter'       : 'gearcrafting',
    'Jewelrycrafter'    : 'jewelrycrafting',
    'Cooker'            : 'cooking',
    'Fighter'           : 'fighting' #########
    }
char_professions = {
#   'char_': ['profession', 'profession', 'profession'],

    char_I    : ['Fighter'],
    char_II   : ['Cooker','Fisher'],
    char_III  : ['Weaponcrafter','Gearcrafter','Jewelrycrafter','Fighter'],
    char_IV   : ['Miner'],
    char_V    : ['Woodcutter'],
}

works_dict = {
    'mining'            : task_gathering,
    'woodcutting'       : task_gathering,
    'fishing'           : task_gathering,
    'weaponcrafting'    : task_craft,
    'gearcrafting'      : task_craft,
    'jewelrycrafting'   : task_craft,
    'cooking'           : task_craft,
    'fighting'          : task_farm,

}

# задача (что, сколько) -> профессия -> персонаж -> условия -> добавить в список -> проверка списка -> дефолт действие


