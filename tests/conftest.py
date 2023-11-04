import pytest
import requests
import example
url = 'https://qa-scooter.praktikum-services.ru/api/v1/'
user_id = None


@pytest.fixture()
def new_courier():
    return example.data_for_new_courier()


@pytest.fixture(scope='function')
def prepare_user():

    def _prepare_user(payload):
        global user_id
        response = requests.post(f'{url}courier/login', data=payload)
        user_id = response.json()['id']
        return response

    yield _prepare_user
    requests.delete(f'{url}courier/{user_id}')


@pytest.fixture()
def register_courier():
    return example.register_new_courier_and_return_login_password()
