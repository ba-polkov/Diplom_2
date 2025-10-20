from helpers import *

class UserData:
    email='bogdan-polk1@yandex.ru'
    password=123
    username='Bogdan'
    
    credentials_with_empty_field = [
        {'email':'',
         'password':create_random_password(),
         'name':create_random_username()
        },
        {'email':create_random_email(),
         'password': '',
         'name':create_random_username()
        },
        {'email':create_random_email(),
         'password':create_random_password(),
         'name': ''
        }
    ]
    
class IngredientData:
    burg1=['61c0c5a71d1f82001bdaaa73', '61c0c5a71d1f82001bdaaa6c',
           '61c0c5a71d1f82001bdaaa76', '61c0c5a71d1f82001bdaaa79']
    
    burg2=['61c0c5a71d1f82001bdaaa74', '61c0c5a71d1f82001bdaaa6d',
           '61c0c5a71d1f82001bdaaa7a', '61c0c5a71d1f82001bdaaa6f']
    
    invalid_hash='61c0c5a71d1f088005553535'