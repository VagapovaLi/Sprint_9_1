
import allure
from urls import ENDPOINT_LISTINGS

@allure.feature("Удаление объявлений")
@allure.story("Успешное удаление объявления")
class TestDeleteListing:
    @allure.title("Проверка успешного удаления объявления")

    def test_delete_listing_success_expected_answer_200(self, api_client, auth_token, create_test_listing):

        listing_id = create_test_listing["id"]
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
            }


        delete_response = api_client.delete(
            endpoint=f"{ENDPOINT_LISTINGS}/{listing_id}",
            headers=headers
        )

        assert delete_response.status_code == 200, (
            f"Ожидался статус код 200 (Ok), но получен {delete_response.status_code}. "
            f"Ответ сервера: {delete_response.text}"
        )

        delete_data = delete_response.json()
        assert "message" in delete_data, "Ответ должен содержать поле 'message'"
        expected_message = "Объявление удалено успешно"
        actual_message = delete_data["message"]
        assert actual_message == expected_message, (
            f"Ожидалось сообщение '{expected_message}', получено '{actual_message}'"
        )
