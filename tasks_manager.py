import db
import info
import cache_manager

task_dict = {
#    char_N    : [('code', 'quantity'),('str', 'int')],

}
task_board= {
#   'skill' : [task, task, task],
    'gearcrafting' : [('mushmush_wizard_hat', 1)],
    'woodcutting'  : [('spruce_plank', 10)]
}

default_tasks = {

}

def add_to_task_board(target_code, quantity=1, non_stop=False):
    if non_stop:
        quantity = 999
    elif quantity <= 0:
        return
    skill = cache_manager.check_in_cache(target_code)['for_work']
    task = (target_code, quantity)
    task_board[skill] = [task] + task_board.get(skill, [])
    print('_____________TASKS IN BOARD_____________')
    for prof in list(task_board.keys()):
        print(f"{prof} - {task_board[prof]}")


def get_task(character_name):
    """

    :param character_name:
    :return: task ('code', 'quantity') or False
    """
    from db import char_professions

    my_professions = char_professions[character_name]     #   'char_': ['profession', 'profession', 'profession']
    for profession in my_professions:
        skill = char_professions[profession]
        have_tasks = task_board[skill]
        if not have_tasks:
            continue                                # default case

        else:
            first_task = have_tasks.pop(0)
            return first_task

    return False



# задача (что, сколько) -> профессия -> персонаж -> условия -> добавить в список -> проверка списка -> дефолт действие

