import db
import info
import cache_manager
from db import char_I, char_II, char_III, char_IV, char_V,char_professions

task_dict = {
#    char_N    : [('code', 'quantity'),('str', 'int')],

    char_I    : [],
    char_II   : [],
    char_III  : [],
    char_IV   : [],
    char_V    : [],
}
task_board= {
#   'skill' : [task, task, task],
    'gearcrafting' : [('mushmush_wizard_hat', 1)]
}

default_tasks = {

}

def add_to_task_board(target_code, quantity=1, non_stop=False):
    skill = cache_manager.check_in_cache(target_code)['for_work']
    task = (target_code, quantity)
    task_board[skill] = [task] + task_board.get(skill, [])


def get_task(character_name):
    """

    :param character_name:
    :return: task ('code', 'quantity') or False
    """
    my_professions = char_professions[character_name]     #   'char_': ['profession', 'profession', 'profession']
    for profession in my_professions:
        skill = db.char_professions[profession]
        have_tasks = task_board[skill]
        if not have_tasks:
            continue                                # default case

        else:
            first_task = have_tasks.pop(0)
            return first_task

    return False



# задача (что, сколько) -> профессия -> персонаж -> условия -> добавить в список -> проверка списка -> дефолт действие

