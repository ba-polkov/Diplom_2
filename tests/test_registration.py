import requests
import pytest
import allure
from urls import *
from data import *

class TestRegistrations:
    @allure.title ('Проверка успешной регисатрици акканта')
    @allure.description('Создание и удаление аккаунта')
    def test_registration_new_account_success_sumbit(self):
        payload = {
            'email': create_random_email(),
            'password': create_random_password(),
            'name':create_random_username()
        }
        
        response=requests.post(Urls.user_create, data=payload)
        deserials=response.json()
        
        assert response.status_code==200
        assert deserials['success'] is True
        assert 'accessToken' in deserials.keys()
        assert 'refreshToken' in deserials.keys()
        assert deserials['user']['email'] == payload['email']
        assert deserials['user']['name'] == payload['name']
        
        acess_token = deserials['accessToken']
        requests.delete(Urls.user_delete, headers={'Authorization':acess_token})
        
    @allure.title('Проверка регистрации пользователя с путыми полями в запросе')
    @allure.description('Проверка регистрации пользователя с пустыми полями пароль, e-mail, имя')
    @pytest.mark.parametrize('credentials', UserData.credentials_with_empty_field)
    def test_registration_one_required_field_is_empty_failed_submit(self, credentials):
        response=requests.post(Urls.user_create, data=credentials)
        
        assert (response.status_code == 403 and 
                response.json() == {'success': False, 'message': 'Email, password and name are required fields'})
        
    @allure.title('Проверка создания уже существующего пользователя')
    @allure.description('Регистрация пользователя уже существующего в БД')
    def test_registration_login_taken_failde_sumbit(self):
        payload = {
            'email': UserData.email,
            'password': create_random_password(),
            'name': create_random_username()
        }
        response = requests.post(Urls.user_create, data=payload)
        
        assert response.status_code == 403 and response.json() == {'success': False, 'message': 'User already exists'}