from db import char_I, char_II, char_III, char_IV, char_V

task_dict = {
#    char_N    : [('code', 'quantity'),('str', 'int')],

    char_I    : [],
    char_II   : [],
    char_III  : [],
    char_IV   : [],
    char_V    : [],
}
task_board= {
#   'skill' : ['task', 'task','task'],

}


def add_to_task_board(target_code, quantity=1, non_stop=False):
    skill = 'cooking'
    task = (target_code, quantity)
    task_board[skill] = [task] + task_board.get(skill, [])

# задача (что, сколько) -> профессия -> персонаж -> условия -> добавить в список -> проверка списка -> дефолт действие
