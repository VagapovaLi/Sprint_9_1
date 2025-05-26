import pytest
import allure
from urls import BASE_URL
from api_client.api_client_session import ApiClient
from urls import ENDPOINT_SIGNUP
from utilities.data_generator import DataGenerator as Dg


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API с базовым URL"""
    with allure.step("Создание API клиента с базовым URL"):
        return ApiClient(BASE_URL)



@pytest.fixture
def registration_data():
    with allure.step("Генерация тестовых данных для регистрации пользователя"):
        fake_user = Dg.create_fake_user()
        data = {
            "email": fake_user.get("email"),
            "password": fake_user.get("password"),
            "submitPassword": fake_user.get("password")
        }
        allure.attach(str(data), name="Регистрационные данные", attachment_type=allure.attachment_type.TEXT)
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
