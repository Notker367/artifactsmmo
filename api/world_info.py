from dotenv import load_dotenv
import requests
import os

# Загрузка переменных из файла .env
load_dotenv()

# Получение переменных
token = os.getenv('TOKEN')



def get_character_info(character_name):
    """

    :param character_name:
    :return:
    """

    url = f"https://api.artifactsmmo.com/characters/{character_name}"

    response = requests.get(url)

    return response



#def get_all_maps():
