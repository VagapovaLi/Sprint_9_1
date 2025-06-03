
import allure
from urls import ENDPOINT_LISTINGS, BASE_URL

@allure.feature("Удаление объявлений")
@allure.story("Успешное удаление объявления")
class TestDeleteListing:
    @allure.title("Проверка успешного удаления объявления")

    def test_delete_listing_success(self, api_client, auth_token, create_test_listing):

        listing_id = create_test_listing["id"]
        allure.attach(str(listing_id), name="ID объявления", attachment_type=allure.attachment_type.TEXT)

        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
            }
        allure.attach(str(headers), name="Заголовки запроса", attachment_type=allure.attachment_type.TEXT)

        delete_response = api_client.delete(
            endpoint=f"{ENDPOINT_LISTINGS}/{listing_id}",
            headers=headers
        )

        # allure.attach(
        #     f"Request: DELETE {BASE_URL}{ENDPOINT_LISTINGS}/{listing_id}\n"
        #     f"Headers: {headers}\n"
        #     f"Response Status: {delete_response.status_code}\n"
        #     f"Response Body: {delete_response.text}",
        #     name="Детали запроса и ответа",
        #     attachment_type=allure.attachment_type.TEXT
        # )

        assert delete_response.status_code == 200, (
            f"Ожидался статус код 200 (Ok), но получен {delete_response.status_code}. "
            f"Ответ сервера: {delete_response.text}"
        )

        delete_data = delete_response.json()
        #allure.attach(str(delete_data), name="Тело ответа", attachment_type=allure.attachment_type.JSON)



        assert "message" in delete_data, "Ответ должен содержать поле 'message'"

        expected_message = "Объявление удалено успешно"
        actual_message = delete_data["message"]
        assert actual_message == expected_message, (
            f"Ожидалось сообщение '{expected_message}', получено '{actual_message}'"
        )
        # allure.attach(
        #     f"Ожидаемое сообщение: {expected_message}\n"
        #     f"Фактическое сообщение: {actual_message}",
        #     name="Сравнение сообщений",
        #     attachment_type=allure.attachment_type.TEXT
        # )
