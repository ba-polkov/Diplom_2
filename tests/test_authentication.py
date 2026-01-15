import pytest
import allure
import requests
from helpers import *
from urls import *
from data import *

class TestAuthentication:
    @allure.title ('Проверка успешной аутентификации пользовтаеля')
    @allure.description('Аутентификация пользователя с созданным аккаунтом')
    def test_auth_existing_account_success(self, create_new_user_ande_delete):
        payload=create_new_user_ande_delete[0]
        response=requests.post(Urls.user_auth, data=payload)
        deserials=response.json()
        
        assert response.status_code == 200
        assert deserials['success'] is True 
        assert 'accessToken' in deserials.keys()
        assert 'refreshToken' in deserials.keys()
        assert deserials['user']['email'] == create_new_user_ande_delete[0]['email']
        assert deserials['user']['name'] == create_new_user_ande_delete[0]['name']
        
    @allure.title('Проверка ответа от сервара на аутентификацию пользователя с незарегистрированым email')
    def test_auth_with_wrong_login_expected_error(self):
        payload = {
            'email': create_random_email(),
            'password': UserData.password
        }
        response = requests.post(Urls.user_auth, data=payload)
        
        assert response.status_code == 401 and response.json() == {"success": False,
                                                                   "message": "email or password are incorrect"}
        
    @allure.title ('Проверка ответа от сервера на аутентификацию с неверным паролем')
    def test_auth_with_wrong_password_expected_error(self):
        payload = {
            'email':UserData.email,
            'password':create_random_password()
        }
        response = requests.post(Urls.user_auth, data=payload)
        
        assert response.status_code == 401 and response.json() == {"success": False,
                                                                   "message": "email or password are incorrect"}