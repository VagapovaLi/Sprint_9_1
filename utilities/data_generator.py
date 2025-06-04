from faker import Faker
import allure

from datetime import datetime
import random
import string


class DataGenerator:

    @staticmethod
    def create_fake_user():
        """Метод для создания фейковых данных заказчика."""
        #with allure.step("Создаём фейковые данные заказчика"):
        fake = Faker("ru_RU")
        name = fake.first_name_female()
        surname = fake.last_name_female()
        email = fake.email()
        phone = fake.phone_number()
        password = fake.password(length=10)

        user = {"name": name,
                    "surname": surname,
                    "email": email,
                    "phone": phone,
                    "password": password
                    }
        return user


    @staticmethod
    def generator_uid():
        with allure.step("Генерируем uid"):
            """Метод для генерации uid"""
            fake = Faker()
            uid = fake.uuid4()
            return uid


    @staticmethod
    def create_listing_data():
        fake = Faker("ru_RU")  # Инициализация Faker для русского языка
        data = {
            'name': f'Объявление {DataGenerator.generator_uid()}',  # Случайное слово
            'category': 'Авто',
            'condition': 'Новый',
            'city': 'Москва',
            'description': fake.sentence(nb_words=10),  # Случайное предложение из 10 слов
            'price': fake.pyint(min_value=100, max_value=1000000)  # Случайное целое число в диапазоне
        }
        return data

