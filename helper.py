import random
import string
import allure


class StringGenerator:
    @staticmethod
    #Генерирует случайную строку из букв нижнего регистра заданной длины.
    def generate_random_string(length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))

class UserDataGenerator:
    @allure.step('Генерация данных пользователя с случайным логином, паролем и именем')
    def generate_random_data_user(self):
        return {
            "email": StringGenerator.generate_random_string(10) + '@yandex.ru',
            "password": StringGenerator.generate_random_string(10),
            "name": StringGenerator.generate_random_string(10)
        }