import action
import cache_manager
import info
import tasks_manager

from main import wait_cooldown_from_response

# Обработка ответов при работе
async def response_processing(character_name, response, get_response_code=False):
    if response.status_code == 200:
        await wait_cooldown_from_response(character_name)
        if get_response_code:
            return True, response.status_code
        return True

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    elif response.status_code == 499:
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 598:
        # not in map
        pass

    else:
        print(response.json()['error'])

    if get_response_code:
        return False, response.status_code
    return False

async def complete_check(character_name, task):
    in_inv = info.get_item_dict(character_name)
    item_name, quantity = task[0], task[1]

    if item_name in list(in_inv.keys()):
        left = quantity - in_inv[item_name]
    else:
        left = quantity

    return left <= 0

async def complete_check_get_left(character_name,task):
    in_inv = info.get_item_dict(character_name)
    item_name, quantity  = task[0], task[1]

    if item_name in list(in_inv.keys()):
        left = quantity - in_inv[item_name]
    else:
        left = quantity + 0
    return left


async def ending_work(character_name, target, task, sub_task_list=None):
    # Проверка остатка по задаче
    quantity_left = await complete_check_get_left(character_name, task)

    if quantity_left > 0:
        tasks_manager.add_to_task_board(target, quantity=quantity_left, character_name=character_name)
    else:
        print(f"{character_name} has completed {task}.")

    if sub_task_list:
        print(f'{character_name} needs {sub_task_list} for {target}')
        tasks_manager.add_tasks_to_tasks_board(sub_task_list, character_name)

    await all_in_bank(character_name)

"""async def ending_work(character_name, target, task, sub_task_list = None):
    quantity = await complete_check_get_left(character_name, task)
    tasks_manager.add_to_task_board(target, quantity=quantity,character_name=character_name)
    if sub_task_list is not None:
        print(f'{character_name} need {sub_task_list} for {target}')
        tasks_manager.add_tasks_to_tasks_board(sub_task_list,character_name)
    await all_in_bank(character_name)"""

# Функция перемещения персонажа к указанным координатам
async def go_to(coordinates, character_name):
    coordinates = (coordinates[0],coordinates[1]) # for [x,y] and (x,y)

    if info.get_position(character_name) == coordinates:
        print(f"{character_name} - already in position now")
        return

    response_move = action.move(coordinates, character_name)
    if response_move.status_code == 200:
        print(f"{character_name} Move code: {response_move.status_code}")

    elif response_move.status_code == 499:
        await wait_cooldown_from_response(character_name)
        await go_to(coordinates, character_name)
        print(f'WARNING {character_name}  go_to - 499 !!!!!!')

    else:
        print(response_move.json()['error'])

    await wait_cooldown_from_response(character_name)

#Экономика
#__________________________________________________________________________
current_count = 30
recycl=False
async def all_in_bank(character_name):
    item_dict = info.get_item_dict(character_name)

    if item_dict == {}:
        print(f'{character_name} inventory is blank')
        return

    await go_to((4,1), character_name) # bank

    for name, quantity in item_dict.items():
        action.deposit_bank(character_name, name, quantity)
        print(f"{character_name} deposit {quantity} - {name} in bank")
        await wait_cooldown_from_response(character_name)


async def task_craft(character_name, task):
    target = task[0]
    need_craft = task[1]
    target_info = cache_manager.check_in_cache(target)
    work = target_info['for_work']
    location = target_info['craft']['location']
    recept  = target_info['craft']['recept'] # {name : quantity}
    skill = work

    global recycl
    recycl = False

    my_item = info.get_item_dict(character_name)
    recept_name_list = list(recept.keys())
    inv_max = info.get_inventory_max_items(character_name)
    can_craft = need_craft
    me_need_from_bank = {}
    not_have = []
    min_have_items_for_craft = need_craft

    if not recycl:
        bank_item = info.get_bank_items(recept_name_list) # {str : int}
        print('ssssssssssss', bank_item, recept_name_list)

        for item in recept_name_list:
            in_inv = my_item.get(item, 0)
            in_bank = bank_item.get(item, 0)
            in_recept = recept.get(item, 0)
            me_need_from_bank = recept.items()

            i_have = in_inv + in_bank
            have_items_for_craft = i_have // in_recept

            if have_items_for_craft < can_craft:
                count = (need_craft * in_recept) - i_have
                print('!!!!!!!!', item, count, need_craft, in_recept, in_inv, in_bank)
                not_have += [(item,count)]
                print(f"{character_name} not can craft {target} not have {count} {item}")

            if have_items_for_craft < min_have_items_for_craft:
                min_have_items_for_craft = have_items_for_craft


    else:
        item = target
        bank_item = info.get_bank_items([item]) # {str : int}
        in_inv = my_item.get(item, 0)
        in_bank = bank_item.get(item, 0)
        me_need_from_bank = [(target, 1)] # Вернется примерно 30% поэтому можно взять х2 предметов

        have_items_for_craft = in_inv + in_bank

        if have_items_for_craft == 0 or need_craft == 0:
            print(f"{character_name} not can recycl {target} needed more {item}")
            await farm(character_name, target='mushmush')
            #return

    print('aaaaaaaaaaaaaaa', min_have_items_for_craft, can_craft)

    if min_have_items_for_craft < can_craft:
        can_craft = min_have_items_for_craft


    if can_craft <= 0:
        print(f'WARNING {character_name} task_craft need_craft = 0 {task}')
        await ending_work(character_name, target, task, sub_task_list=not_have)
        return


    need_slots_for_one = 0

    for item, quantity_need in recept.items():
        need_slots_for_one += quantity_need

    if need_slots_for_one * can_craft > inv_max:
        can_craft = inv_max // need_slots_for_one

    await all_in_bank(character_name)

    for item, quantity in me_need_from_bank: # me_need_from_bank = recept.items() dict_items([('greater_wooden_staff', 50)])
        print(f'{character_name} me need {quantity * can_craft} {item} from bank')
        action.withdraw_bank(character_name, item, quantity * can_craft)
        await wait_cooldown_from_response(character_name)

    await go_to(location, character_name) # go workshop

    if recycl:
        response = action.recycl(character_name, target, can_craft)


    else:
        print('!!!!!!!!!', character_name, target, can_craft)
        response = action.craft(character_name, target, can_craft)

    if recycl:
        complete_action = 'Recycl'
    else:
        complete_action = 'Craft'

    ok = await response_processing(character_name, response)

    if ok:
        print(f"{character_name} {complete_action} code: {response.status_code} {complete_action} {can_craft} {target}")
    else:
        for needed_item in recept_name_list:
            print(
                f"{character_name} - not can {complete_action} {recept[needed_item]} {needed_item} -> {can_craft} {target}")

        # check inv
        # create new task
    await ending_work(character_name, target, task, sub_task_list=not_have)




def craft_need(count=None, now=False):
    global current_count

    if now:
        # Вернуть текущее значение, не изменяя его
        return current_count

    elif count is not None:
        # Обновить текущее значение на переданное значение
        if count <= 0:
            current_count = 0
        else:
            current_count = count
    else:
        # Уменьшить текущее значение на единицу
        current_count -= 1

    return current_count
async def craft_from_bank(character_name, target, need_craft = 0):
    recept, skill  = info.get_recept(target) # {name : quantity}, skill

    global recycl

    my_item = info.get_item_dict(character_name)

    recept_name_list = list(recept.keys())

    inv_max = info.get_inventory_max_items(character_name)

    can_craft = need_craft

    me_need = {}

    if not recycl:
        bank_item = info.get_bank_items(recept_name_list) # {str : int}

        for item in recept_name_list:
            in_inv = my_item.get(item, 0)
            in_bank = bank_item.get(item, 0)
            in_recept = recept.get(item, 0)
            me_need = recept.items()

            have_items_for_craft = (in_inv + in_bank) // in_recept

            if have_items_for_craft == 0 or need_craft == 0:
                print(f"{character_name} not can craft {target} needed more {item}")
                await farm(character_name, target='mushmush')
                return

            if have_items_for_craft < can_craft:
                can_craft = have_items_for_craft

    else:
        item = target
        bank_item = info.get_bank_items([item]) # {str : int}
        in_inv = my_item.get(item, 0)
        in_bank = bank_item.get(item, 0)
        me_need = [(target, 1)] # Вернется примерно 30% поэтому можно взять х2 предметов

        have_items_for_craft = in_inv + in_bank

        if have_items_for_craft == 0 or need_craft == 0:
            print(f"{character_name} not can recycl {target} needed more {item}")
            await farm(character_name, target='mushmush')
            return

        if have_items_for_craft < can_craft:
            can_craft = have_items_for_craft

    need_slots_for_one = 0

    for item, quantity_need in recept.items():
        need_slots_for_one += quantity_need

    if need_slots_for_one * can_craft > inv_max:
        can_craft = inv_max // need_slots_for_one

    await all_in_bank(character_name)

    for item, quantity in me_need: # me_need = recept.items() dict_items([('greater_wooden_staff', 50)])
        print(f'{character_name} me need {quantity * can_craft} {item} from bank')
        action.withdraw_bank(character_name, item, quantity * can_craft)
        await wait_cooldown_from_response(character_name)

    await go_to(info.get_workshop(skill), character_name) # go workshop


    if recycl:
        response = action.recycl(character_name, target, can_craft)


    else:
        response = action.craft(character_name, target, can_craft)

    if recycl:
        complete_action = 'Recycl'
    else:
        complete_action = 'Craft'

    if response.status_code == 200:

        print(f"{character_name} {complete_action} code: {response.status_code} {complete_action} {can_craft} {target}")

        left = craft_need(now=True) - can_craft
        craft_need(left)
        print(f'{character_name} left ', craft_need(now=True))
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])
        for needed_item in recept_name_list:
            print(f"{character_name} - not can {complete_action} {recept[needed_item]} {needed_item} -> {can_craft} {target}")

    await all_in_bank(character_name)

#Битвы
#__________________________________________________________________________
monsters = {
    'chicken'       :   (0,  1),
    'blue_slime'    :   (2, -1),
    'red_slime'     :   (1, -1),
    'green_slime'   :   (0, -1),
    'yellow_slime'  :   (4, -1),
    'cow'           :   (0,  2),
    'wolf'          :   (-2, 1),
    'mushmush'      :   (5,  3),
    'flying_serpent':   (5,  4),

}
async def farm(character_name, target):
    await go_to(monsters[target], character_name)

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


async def task_farm(character_name, task):
    #
    target = task[0]
    target_info = cache_manager.check_in_cache(target)
    location = target_info['location']  # get_monster_info[]
    work = target_info['for_work']

    await go_to(location, character_name)

    complete = False
    while not complete:

        response = action.fight(character_name, debug=False)

        ok = await response_processing(character_name, response)

        if ok:
            print(f"{character_name} Fight code: ok")
            # check inv
            # create new task
        else:
            print(f"ERROR task_farm {character_name, task}")
            complete = True


    await ending_work(character_name, target, task)



#Добыча
#__________________________________________________________________________
resources = {
    # Метал
    'copper'       : (2,  0),
    'iron'         : (1,  7),
    'coal'         : (1,  6),
    # Дерево
    'ash'          : (-1, 0),
    'spruce'       : (-2, 5),
    # Рыба
    'gudgeon'      : (4,  2),
    'shrimp'       : (5,  2),
    'trout'        : (-2, 6),
}

wood_info = {
    'ash'          : 6,
    'spruce'       : 6,

    'craft'        : (-2,-3)
}

bars_info = {
    'copper'       : 6,
    'iron'         : 6,

    'craft'        : (1, 5)

}

fish_info = {
    'gudgeon'      : 1,
    'shrimp'       : 1,
    'trout'        : 1,

    'craft'        : (1, 1)
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

async def task_gathering(character_name, task):
    target = task[0]
    target_info = cache_manager.check_in_cache(target)
    location = target_info['location']
    work = target_info['for_work']
    need_craft = target_info['need_craft']

    # Проверка, нужно ли сразу переходить к крафту
    if need_craft:
        print(f'{character_name} i do craft {task}')
        await task_craft(character_name, task)
        return

    await go_to(location, character_name)

    complete = False
    status_code = 111
    while not complete:
        response = action.gathering(character_name)

        # Обработка ответа от действия `gathering`
        ok, status_code = await response_processing(character_name, response, get_response_code=True)

        if ok:
            print(f"{character_name} Gathering code: ok")
            # Проверка завершения задачи
            complete = await complete_check(character_name, task)

        else:
            print(f"ERROR task_gathering {character_name, task}, - {status_code}")
            complete = True

    else:
        await ending_work(character_name, target, task)




async def go_crafting(character_name, to_item_code):

    item_dict = info.get_item_dict(character_name) # Инвентарь

    if to_item_code in bars_info:
        await go_to(bars_info['craft'], character_name)
        postfix_craft = ""
        prefix_craft = ""
        postfix_inv = "_ore"
        #                         to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# Название в инвентаре
        craft_coof = bars_info[to_item_code]       # Коэффициент крафта из инфо


    elif to_item_code in wood_info:
        await go_to(wood_info['craft'], character_name)
        postfix_craft = "_plank"
        prefix_craft = ""
        postfix_inv = "_wood"
        #                      to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# кол-во по Название в инвентаре
        craft_coof = wood_info[to_item_code]       # Коэффициент крафта из инфо


    elif to_item_code in fish_info:
        await go_to(fish_info['craft'], character_name)
        postfix_craft = ""
        prefix_craft = "cooked_"
        postfix_inv = ""
        #                      to_item_code = target из def gathering(character_name, target)
        # Название в инвентаре и коэффициент крафта
        count_in_inv = item_dict.get(to_item_code + postfix_inv, 0)# кол-во по Название в инвентаре
        craft_coof = fish_info[to_item_code]       # Коэффициент крафта из инфо


    else:
        print(f"{character_name} - ERROR crafting item_code !!!")
        return

    can_craft = count_in_inv // craft_coof # Счет сколько можем скрафтить

    response = action.craft(character_name, prefix_craft+to_item_code+postfix_craft, can_craft, debug=False)
    if response.status_code == 200:
        print(f"{character_name} Craft code: {response.status_code} craft {can_craft} {prefix_craft+to_item_code+postfix_craft}")
        await wait_cooldown_from_response(character_name)

    elif response.status_code == 497:
        print(f"{character_name} - inventory is full")
        await all_in_bank(character_name)
        print(f"{character_name} - all_in_bank completed")

    else:
        print(response.json()['error'])
        print(f"{character_name} - not can craft {count_in_inv} {to_item_code+postfix_inv} -> {can_craft} {to_item_code+postfix_craft}")



#    'Miner'             : 'mining',
 #   'Woodcutter'        : 'woodcutting',
  #  'Fisher'            : 'fishing',
#    'Weaponcrafter'     : 'weaponcrafting',
 #   'Gearcrafter'       : 'gearcrafting',
  #  'Jewelrycrafter'    : 'jewelrycrafting',
   # 'Cooker'            : 'cooking',
  #  'Fighter'           : 'fighting'