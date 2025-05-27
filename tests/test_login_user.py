
import allure

from urls import ENDPOINT_SIGNIN

@allure.story('Сценарии авторизации пользователя')
# adadad@mail.ru 112233
@allure.title('Авторизация пользователя.Ожидаемый результат: 201')
def test_login_user_expected_answer_201(api_client, create_user):
        payload = create_user

        response = api_client.post(
            endpoint=ENDPOINT_SIGNIN,
            json=payload
        )

        # 1. Проверка наличия основных полей в ответе
        assert response.status_code == 201, f"Ожидался статус код 201, но получен {response.status_code}"
        response_data = response.json()
        assert "user" in response_data, "Ответ должен содержать объект 'user'"
        assert "token" in response_data, "Ответ должен содержать объект 'token'"

        # 2. Проверка данных пользователя
        user_data = response_data["user"]
        assert "id" in user_data and isinstance(user_data["id"], int), "ID пользователя должен быть целым числом"
        assert "name" in user_data and user_data["name"] == "User", "Имя пользователя должно быть 'User'"
        assert "email" in user_data and user_data["email"] == payload["email"], (
            f"Email пользователя должен совпадать с email из запроса ({payload['email']})"
        )
        assert "avatar" in user_data, "Должно присутствовать поле 'avatar'"
        assert "admin" in user_data and isinstance(user_data["admin"], bool), "Поле 'admin' должно быть boolean"

        # 3. Проверка токена
        token_data = response_data["token"]
        assert "access_token" in token_data, "Токен должен содержать поле 'access_token'"
        assert isinstance(token_data["access_token"], str), "Access token должен быть строкой"
        assert len(token_data["access_token"]) > 50, "Access token должен быть достаточно длинным"
