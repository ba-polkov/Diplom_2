import allure 
import pytest
import requests
from data import *
from urls import *

class TestCreateOrder:
    @allure.title ('Проверка ответа на создание заказа с указанными ингредиентами авторизованным пользователем')
    @allure.description('ТЕстирование отправки запроса с разными ингедиентами с учетом аторизации пользователя в системе')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burg1, IngredientData.burg2])
    def test_create_order_authenticated_user_success(self, create_new_user_ande_delete, burger_ingredients):
        headers={'Authorization':create_new_user_ande_delete[1]['accessToken']}
        payload={'ingredients':[burger_ingredients]}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        deserials = response.json()
        
        assert response.status_code == 200
        assert deserials['success'] is True
        assert 'name' in deserials.keys()
        assert 'number' in deserials['order'].keys()
        
    @allure.title ('Проверка ответа на создание заказа с указанными ингредиентами неавторизованным пользователем')
    @allure.description('Тестрование отправки запроса с разными ингредиентами в бургере без автормзации пользоваетля')
    @pytest.mark.parametrize('burger_ingredients', [IngredientData.burg1, IngredientData.burg2])
    def test_createorder_unauthenticated_user_success(self, burger_ingredients):
        payload={'ingredients':burger_ingredients}
        response = requests.post(Urls.order_create, json=payload, headers=Urls.headers)
        
        assert response.status_code == 200 and response.json()["success"] is True
        
    @allure.title ('Проверка ответа от сервера при создани заказа без ингердиентов авторищированным пользователем')
    @allure.description ('Тестирование ответа от сервара при отправке запроса на создание заказа с пустым списком ингредиентов под авторизованным пользователем')
    def test_create_order_empty_ingredients_authenticated_user_expected_error(self, create_new_user_ande_delete):
        headers={'Authorization':create_new_user_ande_delete[1]['accessToken']}
        payload={'ingredients':[]}
        response=requests.post(Urls.order_create, json=payload, headers=headers)

        assert response.status_code == 400  and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}
     
    @allure.title('Проверка оттвета от сервера при создании заказа без ингредиентов неавторизированным польщователем')
    @allure.description('Тестирование ответа от сервера при отправке запроса на создание заказа с пустым списком ингредиентов от неаторищированного польщователя')
    def test_create_order_empty_ingredients_unauthenticated_user_expected_error(self):
        payload = {'ingredients':[]}
        response = requests.post(Urls.order_create, json=payload, headers=Urls.headers)
        
        assert response.status_code == 400 and response.json() == {'success': False,
                                                                   'message': 'Ingredient ids must be provided'}
        
    @allure.title ('Проверка ответа от сервера при создании заказа с неправильным хэшем ингредиента авторищированым пользователем')
    @allure.description('Тетстирование ответа от сервара при отправке запроса на создание заказа с неверным хэшем ингредиента авторизированным пользователем')
    def test_create_order_invalid_ingredients_auth_user_expected_error(self, create_new_user_ande_delete):
        headers = {'Authorization': create_new_user_ande_delete[1]['accessToken']}
        payload = {'ingredients':[IngredientData.invalid_hash]}
        response = requests.post(Urls.order_create, data=payload, headers=headers)
        
        assert response.status_code == 500