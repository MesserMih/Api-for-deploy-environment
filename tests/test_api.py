from fastapi import HTTPException, status, Depends
from fastapi.testclient import TestClient
from api.api import app, get_db
import json
import requests

client = TestClient(app)



def test_post_add_user(): # Проверка добавления юзера
    url = 'http://127.0.0.1:8000/add/?access_right=user'
    file = {'data': open('../dir_for_tests/Alina-love-of-my-life.json', 'rb')}
    response = requests.post(url=url, files=file)
    assert response.status_code == 200

def test_post_add_admin(): # Проверка добавления админа
    url = 'http://127.0.0.1:8000/add/?access_right=admin'
    file = {'data': open('../dir_for_tests/Alina-love-of-my-life.json', 'rb')}
    response = requests.post(url=url, files=file)
    assert response.status_code == 200

def test_show_employers(): # Проверка вывода всех работников
    url = 'http://127.0.0.1:8000/show-employers/'
    response = requests.get(url=url)
    assert response.status_code == 200

def test_show_resume(): # Проверка вывода резюме
    ids = client.get('/show-employers/')
    max_id = (max(map(int, [value for value in ids.json().keys()])))
    url = f'http://127.0.0.1:8000/show-resume/{max_id}'
    response = requests.get(url=url)
    file = json.loads(open('../dir_for_tests/Alina-love-of-my-life.json', 'rb').read())
    assert response.status_code == 200
    assert response.json() == file

def test_show_token(): # проверка вывода токенов
    ids = client.get('/show-employers/')
    max_id = (max(map(int, [value for value in ids.json().keys()])))
    response = client.get(url=f'http://127.0.0.1:8000/show-token/{max_id}')

def test_update_token(): # Проверка изменения токенов
    ids = client.get('/show-employers/')
    max_id = (max(map(int, [value for value in ids.json().keys()])))
    token_1 = client.get(url=f'http://127.0.0.1:8000/show-token/{max_id}')
    response = requests.put(url=f'http://127.0.0.1:8000/update-token/{max_id}')
    token_2 = client.get(url=f'http://127.0.0.1:8000/show-token/{max_id}')
    assert response.status_code == 200
    assert token_1 != token_2

def test_delete_admin(): # Проверка удаления админов
    ids = client.get('/show-employers/')
    max_id = (max(map(int, [value for value in ids.json().keys()])))
    response = client.delete(f"/remove/{max_id}")
    assert response.status_code == 200


def test_delete_user(): # Проверка удаления юзеров
    ids = client.get('/show-employers/')
    max_id = (max(map(int, [value for value in ids.json().keys()])))
    response = client.delete(f"/remove/{max_id}")
    assert response.status_code == 200
