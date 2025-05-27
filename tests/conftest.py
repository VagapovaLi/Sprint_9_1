import pytest
import allure
from urls import BASE_URL
from api_client.api_client_session import ApiClient
from urls import ENDPOINT_SIGNUP , ENDPOINT_SIGNIN , ENDPOINT_LISTINGS
from utilities.data_generator import DataGenerator as Dg


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API с базовым URL"""
    with allure.step("Создание API клиента с базовым URL"):
        return ApiClient(BASE_URL)



@pytest.fixture
def registration_data():
    #with allure.step("Генерация тестовых данных для регистрации пользователя"):
        fake_user = Dg.create_fake_user()
        data = {
            "email": fake_user.get("email"),
            "password": fake_user.get("password"),
            "submitPassword": fake_user.get("password")
        }
        #allure.attach(str(data), name="Регистрационные данные", attachment_type=allure.attachment_type.TEXT)
        return data

@pytest.fixture
def create_user(api_client, registration_data):
    with allure.step("Создание нового пользователя"):
        response = api_client.post(
            endpoint=ENDPOINT_SIGNUP,
            json=registration_data
        )

    assert response.status_code == 201
    user = {
        "email": registration_data.get("email"),
        "password": registration_data.get("password")
    }
    return user



@pytest.fixture
def auth_token(api_client, create_user):
    #with allure.step("Получение токена аутентификации"):
        payload = create_user

        response = api_client.post(
            endpoint=ENDPOINT_SIGNIN,
            json=payload
        )

        # allure.attach(
        #     f"Request: POST {Sd.BASE_URL}{Sd.ENDPOINT_SIGNIN}\n"
        #     f"Request Body: {payload}\n"
        #     f"Response Status: {response.status_code}\n"
        #     f"Response Body: {response.text}",
        #     name="Детали запроса/ответа аутентификации",
        #     attachment_type=allure.attachment_type.TEXT
        # )

        # Проверка статус-кода
        assert response.status_code == 201, f"Ожидался статус код 201, но получен {response.status_code}"

        # Проверка структуры ответа
        response_data = response.json()
        token_data = response_data["token"]
        token = token_data["access_token"]
        return token





@pytest.fixture
def delete_test_listing(api_client, auth_token):
    data_delete_listing = {'id': None}
    yield data_delete_listing


    with allure.step("Удаление тестового объявления"):
        if data_delete_listing['id'] is None:
            return

        # Заголовки с токеном авторизации
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        }

        delete_response = api_client.delete(
            endpoint=f"{ENDPOINT_LISTINGS}/{data_delete_listing['id']}",
            headers=headers
        )

        # allure.attach(
        #     f"Request: DELETE {Sd.BASE_URL}{Sd.ENDPOINT_LISTINGS}/{data_delete_listing['id']}\n"
        #     f"Headers: {headers}\n"
        #     f"Response Status: {delete_response.status_code}\n"
        #     f"Response Body: {delete_response.text}",
        #     name="Детали запроса удаления объявления",
        #     attachment_type=allure.attachment_type.TEXT
        # )

        assert delete_response.status_code == 200, (
            f"Ожидался статус код 200 (Ok), но получен {delete_response.status_code}. "
            f"Ответ сервера: {delete_response.text}"
        )
