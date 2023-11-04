import requests
from data import url
import allure


class TestCourier:

    @allure.title('Проверка создания курьера с валидными данными')
    def test_create_courier(self, new_courier, prepare_user):
        with allure.step('Генерация данных курьера'):
            login, password, first_name = new_courier
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        with allure.step('Отправка POST запроса'):
            response = requests.post(f'{url}courier', data=payload)
            prepare_user(payload)

        with allure.step("Запрос отправлен, посмотрим тело ответа"):
            assert response.json() == {"ok": True}
        with allure.step("Статус код ответа равен 200"):
            assert response.status_code == 201, f"Неверный код ответа, получен {response.status_code}"

    @allure.title('Проверка создания курьера без логина или пароля')
    def test_create_courier_without_field(self, new_courier):
        with allure.step('Генерация данных курьера без логина или без пароля'):
            login, password, first_name = new_courier
            data = {
                "login": login,
                "firstName": first_name
            }
            data2 = {
                "password": password,
                "firstName": first_name
            }
        with allure.step('Отправка POST запросов, используя сгенерированные данные'):
            response = requests.post(f'{url}courier', data=data)
            response2 = requests.post(f'{url}courier', data=data2)
        r = response.json()
        r2 = response2.json()

        with allure.step("Проверка сообщения об ошибке"):
            assert r['message'] == "Недостаточно данных для создания учетной записи"
            assert r2['message'] == "Недостаточно данных для создания учетной записи"
        with allure.step("Статус код ответа равен 400"):
            assert response.status_code == 400, f"Неверный код ответа, получен {response.status_code}"
            assert response2.status_code == 400, f"Неверный код ответа, получен {response.status_code}"

    @allure.title('Проверка создания курьера с повторяющимся логином ')
    def test_create_two_courier(self, new_courier, prepare_user):
        with allure.step('Генерация данных курьера'):
            login, password, first_name = new_courier
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
        with allure.step('Отправка двух POST запросов, используя сгенерированные данные'):
            response = requests.post(f'{url}courier', data=payload)
            response2 = requests.post(f'{url}courier', data=payload)
        r = response2.json()
        prepare_user(payload)

        with allure.step("Проверка сообщения об ошибке"):
            assert r['message'] == "Этот логин уже используется"
        with allure.step("Статус код ответа равен 409"):
            assert response.status_code == 409, f"Неверный код ответа, получен {response.status_code}"
