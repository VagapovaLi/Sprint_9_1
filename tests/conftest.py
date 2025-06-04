import pytest
import allure
from urls import BASE_URL
from api_client.api_client_session import ApiClient
from urls import ENDPOINT_SIGNUP , ENDPOINT_SIGNIN , ENDPOINT_LISTINGS, ENDPOINT_CREATE_LISTING
from utilities.data_generator import DataGenerator as Dg
from pathlib import Path


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API с базовым URL"""
    with allure.step("Создание API клиента с базовым URL"):
        return ApiClient(BASE_URL)



@pytest.fixture
def registration_data():
    #Генерация тестовых данных для регистрации пользователя
        fake_user = Dg.create_fake_user()
        data = {
            "email": fake_user.get("email"),
            "password": fake_user.get("password"),
            "submitPassword": fake_user.get("password")
        }
        return data

@pytest.fixture
def create_user(api_client, registration_data):
    #Создание нового пользователя
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
        payload = create_user
        response = api_client.post(
            endpoint=ENDPOINT_SIGNIN,
            json=payload
        )

        # Проверка статус-кода
        assert response.status_code == 201, f"Ожидался статус код 201, но получен {response.status_code}"

        # Проверка структуры ответа
        response_data = response.json()
        token_data = response_data["token"]
        token = token_data["access_token"]
        return token

@pytest.fixture
def create_test_listing(api_client, auth_token):

    """Фикстура создания тестового объявления"""
    with allure.step("Создание тестового объявления"):
        # Генерация тестовых данных
        data = Dg.create_listing_data()

        with allure.step("Подготовка файлов для отправки"):
            # Путь к изображению в проекте
            image_path = Path(__file__).parent.parent / "settings" / "test_image.jpg"

            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            test_files = [
                ('images', (f'image_{Dg.generator_uid()}.jpg', image_data, 'image/jpeg'))
            ]

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        }

        response = api_client.post(
            endpoint=ENDPOINT_CREATE_LISTING,
            headers=headers,
            data=data,
            files=test_files
        )

        assert response.status_code == 201, (
            f"Ожидался статус код 201, но получен {response.status_code}. "
            f"Ответ сервера: {response.text}"
        )

        response_data = response.json()
        return response_data


@pytest.fixture
def delete_test_listing(api_client, auth_token):
    data_delete_listing = {'id': None}
    yield data_delete_listing

    #Удаление тестового объявления
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

    assert delete_response.status_code == 200, (
        f"Ожидался статус код 200 (Ok), но получен {delete_response.status_code}. "
        f"Ответ сервера: {delete_response.text}"
    )

@pytest.fixture
def another_auth_token(api_client):

    # Регистрация и логин другого пользователя
    another_user = {
        "email": "another_user@example.com",
        "password": "another_password123",
        "submitPassword": "another_password123"
    }

    # Регистрация
    reg_response = api_client.post(
        endpoint=ENDPOINT_SIGNUP,
        json=another_user
    )

    # Логин
    login_response = api_client.post(
        endpoint=ENDPOINT_SIGNIN,
        json=another_user
    )

    return login_response.json()["token"]["access_token"]

