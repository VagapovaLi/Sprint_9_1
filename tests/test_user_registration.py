from urls import ENDPOINT_SIGNUP
import allure


@allure.feature("Регистрация пользователя")
class TestRegistrationUser:

    @allure.story("Успешная регистрация нового пользователя с уникальным email")
    @allure.title("Проверка успешной регистрации")
    def test_registration_success_expected_answer_201(self, api_client, registration_data):
        response = api_client.post(
            endpoint=ENDPOINT_SIGNUP,
            json=registration_data
        )
        assert response.status_code == 201, \
            f"Ожидался статус код 201, но получен {response.status_code}"

        response_data = response.json()
        # allure.attach(str(response_data), name="Полный ответ сервера",
        #               attachment_type=allure.attachment_type.JSON)

        assert "user" in response_data, "Ответ должен содержать объект 'user'"
        assert "access_token" in response_data, "Ответ должен содержать объект 'access_token'"

        user_data = response_data["user"]
        # allure.attach(str(user_data), name="Данные пользователя",
        #               attachment_type=allure.attachment_type.JSON)

        assert "id" in user_data and isinstance(user_data["id"], int), \
            "Пользователь должен иметь целочисленный 'id'"
        assert "name" in user_data and user_data["name"] == "User", \
            "Имя пользователя должно быть 'User'"
        assert "email" in user_data and user_data["email"] == registration_data["email"], \
            f"Email пользователя должен совпадать с email из запроса {registration_data['email']}"

        token_data = response_data["access_token"]
        assert "access_token" in token_data and isinstance(token_data["access_token"], str), \
            "Access token должен быть строкой"
        assert len(token_data["access_token"]) > 50, "Access token должен быть достаточно длинным"


    @allure.story("Регистрация с уже существующим email")
    @allure.title("Проверка обработки повторной регистрации")
    def test_registration_with_repeat_email_expected_answer_400(self, api_client, registration_data):
        #with allure.step("1. Первая регистрация (успешная)"):
            first_response = api_client.post(
                endpoint=ENDPOINT_SIGNUP,
                json=registration_data
            )
            # allure.attach(str(first_response.json()), name="Ответ первой регистрации",
            #               attachment_type=allure.attachment_type.JSON)
            assert first_response.status_code == 201

            repeat_response = api_client.post(
                endpoint=ENDPOINT_SIGNUP,
                json=registration_data
            )

            assert repeat_response.status_code == 400, \
                f"Ожидался статус код 400, но получен {repeat_response.status_code}"

            repeat_response_data = repeat_response.json()
            # allure.attach(str(repeat_response_data), name="Ответ на повторную регистрацию",
            #               attachment_type=allure.attachment_type.JSON)

            assert "statusCode" in repeat_response_data, "Ответ должен содержать поле 'statusCode'"
            assert repeat_response_data["statusCode"] == 400, \
                f"Ожидался statusCode 400, но получен {repeat_response_data['statusCode']}"

            assert "message" in repeat_response_data, "Ответ должен содержать поле 'message'"
            expected_message = "Почта уже используется"
            actual_message = repeat_response_data["message"]
            assert actual_message == expected_message, \
                f"Ожидалось '{expected_message}', получено '{actual_message}'"
