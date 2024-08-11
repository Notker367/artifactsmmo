import json
import os
import time
import requests

import info

CACHE_FILE = "cache.json"  # Имя файла для хранения кэша
CACHE_EXPIRY = 1800  # Время истечения кэша (30 минут в секундах)


def load_cache():
    # Загрузка кэша из файла, если он существует
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            return json.load(file)
    return {"static_data": {}, "dynamic_data": {}}  # Возвращаем пустую структуру, если файла нет


def save_cache(cache):
    # Сохранение кэша в файл
    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=4)


def is_cache_expired(last_update):
    # Проверка, истек ли срок действия кэша
    return (time.time() - last_update) > CACHE_EXPIRY


def check_in_cache(item_code):
    # Проверка наличия элемента в кэше
    cache = load_cache()
    if item_code in cache["static_data"]:
        return cache["static_data"][item_code]

    if item_code in cache["dynamic_data"]:
        if not is_cache_expired(cache["dynamic_data"][item_code]["last_update"]):
            return cache["dynamic_data"][item_code]["data"]

    response = info.about(item_code)
    save_item_data_to_cache(item_code, response)
    return response


def fetch_item_data(item_code):
    # Запрос данных об элементе из API
    url = f"https://api.artifactsmmo.com/items/{item_code}"
    response = requests.get(url, headers={"Accept": "application/json"})
    data = response.json()["data"]
    return {
        "name": data["item"]["name"],
        "level": data["item"]["level"],
        "type": data["item"]["type"],
        "subtype": data["item"]["subtype"],
        "stock": data["ge"]["stock"],
        "sell_price": data["ge"]["sell_price"],
        "buy_price": data["ge"]["buy_price"],
    }


def save_item_data_to_cache(item_code, data, is_static=False):
    # Сохранение данных элемента в кэш
    cache = load_cache()
    if is_static:
        cache["static_data"][item_code] = data
    else:
        cache["dynamic_data"][item_code] = {"data": data, "last_update": time.time()}
    save_cache(cache)


def add_static_item(item_code, data):
    # Добавление статического элемента в кэш
    save_item_data_to_cache(item_code, data, is_static=True)
