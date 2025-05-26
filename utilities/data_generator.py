from faker import Faker
import allure
from datetime import datetime
import random
import string



class DataGenerator:

    @staticmethod
    def create_fake_user():
        """Метод для создания фейковых данных заказчика."""
        with allure.step("Создаём фейковые данные заказчика"):
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