import action
import pytest

import api.world_info
import tasks_manager
import cache_manager

character_name = "Pivos"

def test_move():
    response = action.move((0,1),character_name)
    assert response.status_code == 200, response.status_code

def test_chicken_farm():
    response_move = action.move((0,1), character_name, debug=False)
    assert response_move.status_code in (200, 490)
    response_fight = action.fight(character_name,debug=True)
    assert response_fight.status_code == 200, response_fight.status_code

def test_cooldown():
    response = api.world_info.get_character_info(character_name)

#def test_map_info():

def test_tasks():
    x = cache_manager.check_in_cache('copper_boots')
    print(x)
    print(tasks_manager.task_board)