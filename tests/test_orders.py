import json
from random import randint

import allure
import pytest
import requests
from faker import Faker

from data import url


class TestOrders:
    @allure.title('Проверка создания заказа')
    @pytest.mark.parametrize('color', [
        "BLACK", "GREY", "BLACK, GREY", ''
    ])
    def test_orders(self, color):
        with allure.step('Генерация данных'):
            fake = Faker()
            payload = {
                "firstName": fake.first_name(),
                "lastName": fake.last_name(),
                "address": fake.address(),
                "metroStation": randint(0, 100),
                "phone": fake.phone_number(),
                "rentTime": randint(0, 100),
                "deliveryDate": f'{randint(2023,2025)}-{randint(1,12)}-{randint(1,31)}',
                "comment": fake.text(),
                "color": [
                    color
                ]
            }
        with allure.step("Сериализация данных"):
            json_string = json.dumps(payload)
        with allure.step('Отправка POST запроса, используя сгенерированные данные'):
            response = requests.post(f'{url}orders', data=json_string)

        with allure.step("Проверяем, что тело ответа содержит track"):
            assert 'track' in response.json()
        with allure.step("Статус код ответа равен 201"):
            assert response.status_code == 201

    @allure.title('Проверка списка заказов')
    def test_orders_list(self):
        with allure.step('Отправка GET запроса на получение списка заказов'):
            response = requests.get(f'{url}orders')

        with allure.step("Проверка на содержание списка заказов в теле ответа"):
            assert 'orders' in response.json()
        with allure.step("Статус код ответа равен 200"):
            assert response.status_code == 200
