import allure
import requests

from data import url


class TestLoginCourier:

    @allure.title('Проверка логина курьера с валидными данными')
    def test_login(self, register_courier, prepare_user):
        with allure.step('Генерация данных и регистрация курьера'):
            login = register_courier[0]
            password = register_courier[1]
            payload = {
                "login": login,
                "password": password
            }
        with allure.step('Отправка POST запроса, используя сгенерированные данные'):
            response = requests.post(f'{url}courier/login', data=payload)
        prepare_user(payload)

        with allure.step("Проверка, что успешный запрос возвращает id"):
            assert 'id' in response.json()
        with allure.step("Статус код ответа равен 200"):
            assert response.status_code == 200

    @allure.title('Проверка логина курьера без логина или пароля')
    def test_login_courier_without_field(self, register_courier):
        with allure.step('Генерация данных и регистрация курьера'):
            login = register_courier[0]
            password = register_courier[1]

            data = {
                "login": login
                }

            data1 = {
                "password": password
                }

        with allure.step('Отправка POST запросов, используя сгенерированные данные'):
            response = requests.post(f'{url}courier/login', data=data)
            response2 = requests.post(f'{url}courier/login', data=data1)

        with allure.step("Проверка сообщения об ошибке"):
            assert response2.json()['message'] == "Недостаточно данных для входа"
            assert response.json()['message'] == "Недостаточно данных для входа"
        with allure.step("Статус код ответа равен 400"):
            assert response.status_code, response2.status_code == 400

    @allure.title('Проверка логина несуществующего курьера')
    def test_login_non_existent_courier(self, new_courier):
        with allure.step('Генерация данных курьера'):
            login = new_courier[0]
            password = new_courier[1]
            payload = {
                "login": login,
                "password": password
            }
        with allure.step('Отправка POST запроса, используя сгенерированные данные'):
            response = requests.post(f'{url}courier/login', data=payload)

        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()['message'] == "Учетная запись не найдена"
        with allure.step("Статус код ответа равен 404"):
            assert response.status_code == 404
