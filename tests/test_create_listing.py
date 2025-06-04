import pytest

from datetime import datetime
from urls import ENDPOINT_CREATE_LISTING
from utilities.data_generator import DataGenerator as Dg
import allure
from pathlib import Path


@allure.feature("Создание объявлений")
@allure.story("Успешное создание объявления")
class TestCreateListing:
    @allure.title("Проверка успешного создания объявления")
    def test_successful_listing_creation_success_expected_answer_201(self, api_client, auth_token, delete_test_listing):

        data = Dg.create_listing_data()
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

        #Проверка статус-кода ответа
        assert response.status_code == 201, (
            f"Ожидался статус код 201, но получен {response.status_code}. "
            f"Ответ сервера: {response.text}"
        )

        response_data = response.json()
        delete_test_listing['id'] = response_data['id']

        required_fields = [
            'id', 'name', 'category', 'condition', 'city',
            'description', 'price', 'img1', 'owner',
            'updatedAt', 'createdAt'
        ]
        missing_fields = [field for field in required_fields if field not in response_data]
        assert not missing_fields, f"Отсутствуют обязательные поля: {', '.join(missing_fields)}"

        type_checks = [
            ('id', int),
            ('name', str),
            ('category', str),
            ('condition', str),
            ('city', str),
            ('description', str),
            ('price', int),
            ('owner', int)
        ]

        type_errors = []
        for field, expected_type in type_checks:
            if not isinstance(response_data[field], expected_type):
                type_errors.append(
                    f"Поле '{field}': ожидался {expected_type.__name__}, получен {type(response_data[field]).__name__}")

            assert not type_errors, "Ошибки проверки типов:\n" + "\n".join(type_errors)

        try:
            datetime.fromisoformat(response_data['createdAt'].replace('Z', ''))
            datetime.fromisoformat(response_data['updatedAt'].replace('Z', ''))

        except ValueError :
            data_comparison = [
                ('name', 'Название'),
                ('category', 'Категория'),
                ('condition', 'Состояние'),
                ('city', 'Город'),
                ('description', 'Описание')
            ]

            comparison_errors = []
            for field, name in data_comparison:
                if response_data[field] != data[field]:
                    comparison_errors.append(
                        f"{name}: ожидалось '{data[field]}', получено '{response_data[field]}'")

                # Проверка цены отдельно, так как она преобразуется в int
            if response_data['price'] != int(data['price']):
                comparison_errors.append(f"Цена: ожидалось {data['price']}, получено {response_data['price']}")

            assert not comparison_errors, "Несоответствия данных:\n" + "\n".join(comparison_errors)

            assert response_data['img1'].startswith('http'), "Ссылка на изображение должна быть URL"
            assert 'isFavorite' in response_data, "Отсутствует поле isFavorite"
            assert response_data['createdAt'] == response_data[
                'updatedAt'], "Даты создания и обновления должны совпадать для нового объявления"
