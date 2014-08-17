from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Crypto.Hash import SHA256

import models

Base = declarative_base()


class Account:

    @classmethod
    def __init__(cls, session):
        cls.session = session

# TODO: add check for proportions
    @classmethod
    def set_account(cls, name, password, weight, height, gender,
                    activity_level, age, percent_proteins, percent_carbs,
                    percent_fats):
        cls.name = name
        cls.password = password
        cls.weight = weight
        cls.height = height
        cls.gender = gender
        cls.activity_level = activity_level
        cls.age = age
        cls.percent_proteins = percent_proteins
        cls.percent_carbs = percent_carbs
        cls.percent_fats = percent_fats
        cls.recomended_calories = cls.__calculate_recomended_calories__()
        cls.recomended_proteins = \
            cls.recomended_calories * cls.percent_proteins
        cls.recomended_carbs = cls.recomended_calories * cls.percent_carbs
        cls.recomended_fats = cls.recomended_calories * cls.percent_fats

    @classmethod
    def add_account(cls):
        account = models.Account(
            name=cls.name,
            password=cls.__crypt__(cls.password),
            weight=cls.weight,
            height=cls.height,
            gender=cls.gender,
            activity_level=cls.activity_level,
            age=cls.age,
            recomended_calories=cls.recomended_calories,
            recomended_proteins=cls.recomended_proteins,
            recomended_carbs=cls.recomended_carbs,
            recomended_fats=cls.recomended_fats,
            percent_proteins=cls.percent_proteins,
            percent_carbs=cls.percent_carbs,
            percent_fats=cls.percent_fats)
        cls.session.add(account)
        cls.session.commit()

# The Harris–Benedict equations revised by Roza and Shizgal
    @classmethod
    def __calculate_recomended_calories__(cls):
        if (cls.gender == 'M'):
            cls.BMR = 88.362 + (13.397 * cls.weight) + \
                (4.799 * cls.height) - (5.677 * cls.age)
        if (cls.gender == 'F'):
            cls.BMR = 447.593 + (9.247 * cls.weight) + \
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

    @classmethod
    def match_user_password(cls, user, password):
        for row in cls.session.query(models.Account).filter_by(name=user):
            return row.password == cls.__crypt__(password)

    @classmethod       
    def update_field(cls, field, value):
        pass

Account(models.connect())
Account.set_account("Felix", "6n9b3xcw74", 110, 194, 'M', 5, 28, 0.4, 0.4, 0.2)
Account.add_account()
print(Account.match_user_password("Borisious", "61b3xcw74"))
