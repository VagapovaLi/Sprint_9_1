import time
import allure
import pytest

from urls import ENDPOINT_UPDATE_LISTING, BASE_URL
from utilities.data_generator import DataGenerator as Dg
from faker import Faker


@allure.feature("Обновление объявлений")
class TestUpdateListing:
    fake = Faker("ru_RU")


    @pytest.mark.parametrize("field, new_value", [
        ("name", f"Объявление обновленное {Dg.generator_uid()}"),
        ("category", 'Технологии'),
        ("condition", 'Б/у'),
        ("city", 'Казань'),
        ("description", fake.sentence(nb_words=10)),
        ("price", fake.pyint(min_value=100, max_value=1000000)),
    ])

    def test_update_single_field_listing_success(self, api_client, auth_token, create_test_listing, delete_test_listing,
                                                 field, new_value):
            listing_id = create_test_listing["id"]
            delete_test_listing['id'] = listing_id
            update_data = create_test_listing.copy()
            update_data[field] = new_value

            allure.attach(
                f"Обновляемое поле: {field}\n"
                f"Новое значение: {new_value}",
                name="Данные для обновления",
                attachment_type=allure.attachment_type.TEXT
            )

            headers = {
                "Authorization": f"Bearer {auth_token}",
                "Accept": "application/json"
            }

            time.sleep(1)  # Для различия дат создания и обновления
            response = api_client.patch(
                endpoint=f"{ENDPOINT_UPDATE_LISTING}/{listing_id}",
                headers=headers,
                json=update_data
            )

            assert response.status_code == 200, (
                f"Ожидался статус код 200, но получен {response.status_code}. "
                f"Ответ сервера: {response.text}"
            )

            updated_listing = response.json()
            expected_value = new_value
            assert updated_listing[field] == expected_value, (
                f"Поле {field} не обновилось. "
                f"Ожидалось: {expected_value}, получено: {updated_listing[field]}"
            )
            allure.attach(f"Поле {field} успешно обновлено", name="Результат проверки",
                              attachment_type=allure.attachment_type.TEXT)

            unchanged_fields = [key for key in create_test_listing
                                if key not in [field, "updatedAt", "id", "img1", "img2", "img3"]]
            for key in unchanged_fields:
                assert updated_listing[key] == create_test_listing[key], (
                    f"Поле {key} изменилось, хотя не должно было. "
                    f"Было: {create_test_listing[key]}, стало: {updated_listing[key]}"
                )
            allure.attach(f"Проверено {len(unchanged_fields)} неизменившихся полей", name="Результат проверки",
                          attachment_type=allure.attachment_type.TEXT)


            assert updated_listing["updatedAt"] != create_test_listing["updatedAt"], (
                "Дата обновления должна измениться после редактирования")



    @allure.story("Редактирование объявления, созданного не тем пользователем")
    @allure.title("Проверка запрета обновления чужого объявления")
    def test_update_listing_by_other_user_should_fail(self, api_client, auth_token, another_auth_token,
                                                      create_test_listing, delete_test_listing):

        listing_id = create_test_listing["id"]
        delete_test_listing['id'] = listing_id
        update_data = create_test_listing.copy()
        update_data["name"] = "Попытка изменения другим пользователем"

        headers = {
            "Authorization": f"Bearer {another_auth_token}",
            "Accept": "application/json"
        }

        response = api_client.patch(
            endpoint=f"{ENDPOINT_UPDATE_LISTING}/{listing_id}",
            headers=headers,
            data=update_data
        )

        allure.attach(
            f"Request: PATCH {BASE_URL}{ENDPOINT_UPDATE_LISTING}/{listing_id}\n"
            f"Headers: {headers}\n"
            f"Data: {update_data}\n"
            f"Response Status: {response.status_code}\n"
            f"Response Body: {response.text}",
            name="Детали запроса и ответа",
            attachment_type=allure.attachment_type.TEXT
        )

        assert response.status_code == 401, (
            f"Ожидался статус код 401 (Unauthorized), но получен {response.status_code}. "
            f"Ответ сервера: {response.text}"
        )

        error_response = response.json()

        required_fields = ["message", "error", "statusCode"]
        missing_fields = [field for field in required_fields if field not in error_response]
        assert not missing_fields, f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"

        expected_values = {
            "message": "Оффер не найден или у вас нет прав на его редактирование",
            "error": "Unauthorized",
            "statusCode": 401
        }

        for field, expected in expected_values.items():
            assert error_response[field] == expected, (
                f"Неверное значение поля {field}. "
                f"Ожидалось: '{expected}', получено: '{error_response[field]}'"
            )

