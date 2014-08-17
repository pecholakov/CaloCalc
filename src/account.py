from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Crypto.Hash import SHA256

import models

Base = declarative_base()


class Account:

    @classmethod
    def __init__(cls, session, name, password, weight, height, gender, activity_level, age):
        cls.session = session
        cls.name = name
        cls.password = password
        cls.weight = weight
        cls.height = height
        cls.gender = gender
        cls.activity_level = activity_level
        cls.age = age

    @classmethod    
    def add_account(cls):
        account = models.Account(name = cls.name,
                                 password = cls.__crypt__(cls.password),
                                 weight = cls.weight,
                                 height = cls.height,
                                 gender = cls.gender,
                                 activity_level = cls.activity_level,
                                 age = cls.age,
                                 recomended_calories = cls.__calculate_recomended_calories__())
        cls.session.add(account)
        cls.session.commit()

# The Harris–Benedict equations revised by Roza and Shizgal
    @classmethod
    def __calculate_recomended_calories__(cls):
        if (cls.gender == 'M'):
            cls.BMR = 88.362 + (13.397 * cls.weight) + \
                (4.799 * cls.height) - (5.677 * cls.age)
        if (cls.gender == 'F'):
            cls.BMR = 447.593 + \
                (9.247 * cls.weight) + \
                (3.098 * cls.height) - (4.330 * cls.age)

        if (cls.activity_level == 1):
            cls.calories = cls.BMR * 1.2
        elif (cls.activity_level == 2):
            cls.calories = cls.BMR * 1.375
        elif (cls.activity_level == 3):
            cls.calories = cls.BMR * 1.55
        elif (cls.activity_level == 4):
            cls.calories = cls.BMR * 1.725
        elif (cls.activity_level == 5):
            cls.calories = cls.BMR * 1.9

        return int(cls.calories)
    @classmethod    
    def __crypt__(cls, password):
        cls.pw_bytes = password.encode('utf-8')
        return SHA256.new(cls.pw_bytes).hexdigest()
    @classmethod    

    def check_password(cls, given_pass, password_hash):
        return SHA256.new(given_pass).hexdigest() == password_hash

#TODO: Fix IvanlidRequestError
    @classmethod   
    def match_user_password(cls):
        for row in cls.session.query(Account).all(): 
            print(row.name)    


Account(models.connect(), "Borisious", "952xcw74", 79, 183, 'M', 2, 21)
#Account.add_account()
#account.match_user_password() 
