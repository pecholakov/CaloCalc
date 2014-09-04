from sqlalchemy.orm import sessionmaker
from Crypto.Hash import SHA256
from sqlalchemy.orm.attributes import instance_state
from sqlalchemy.orm import object_session
from sqlalchemy.orm.util import has_identity

import models
from models import Account as account_db
#import consumed_food, statistics


class Account:

    def __init__(self, session):
        self.session = session

    def add_account(self, account_info):
        self.__calculate_nutrition__(account_info)
        account = account_db(
            name=account_info["name"],
            password=account_info["password"],
            weight=account_info["weight"],
            height=account_info["height"],
            gender=account_info["gender"],
            activity_level=account_info["activity_level"],
            age=account_info["age"],
            recomended_calories=account_info["recomended_calories"],
            recomended_proteins=account_info["recomended_proteins"],
            recomended_carbs=account_info["recomended_carbs"],
            recomended_fats=account_info["recomended_fats"],
            percent_proteins=account_info["percent_proteins"],
            percent_carbs=account_info["percent_carbs"],
            percent_fats=account_info["percent_fats"])
        self.session.add(account)
        self.session.commit()

 # tuk samo da add-va i navednyj da commitva
 # can be implement with one() instead of first)
 # ne slaga preizchislnite recomended_stuff obratno v tablicata
    def update_field(self, user_name, field, value):
        user = self.session.query(account_db).filter_by(
            name=user_name).first()
        setattr(user, field, value)
        # print(user.__dict__, "@@@@@@@@@@@@@@@")
        # print("############################")
        user_info = user.__dict__
        self.__calculate_nutrition__(user_info)
        # print(dir(user))
        user.recomended_calories = user_info["recomended_calories"]
        # setattr(user, "recomended_calories",
        # user.__dict__["recomended_calories"])
        self.session.add(user)
        self.session.commit()

    def __calculate_nutrition__(self, account_info):
        self.__calculate_recomended_calories__(account_info)
        self.__calculate_recomended_proteins__(account_info)
        self.__calculate_recomended_carbs__(account_info)
        self.__calculate_recomended_fats__(account_info)


# Harris–Benedict equations revised by Roza and Shizgal
    def __calculate_recomended_calories__(self, account_info):
        self.weight = account_info["weight"]
        self.age = account_info["age"]
        self.height = account_info["height"]
        self.activity = account_info["activity_level"]

        if (account_info["gender"] == 'M'):
            self.BMR = 88.362 + (13.397 * self.weight) + \
                (4.799 * self.height) - (5.677 * self.age)

        if (account_info["gender"] == 'F'):
            self.BMR = 447.593 + (9.247 * self.weight) + \
                (3.098 * self.height) - (4.330 * self.age)

        if (self.activity == 1):
            self.calories = self.BMR * 1.2
        elif (self.activity == 2):
            self.calories = self.BMR * 1.375
        elif (self.activity == 3):
            self.calories = self.BMR * 1.55
        elif (self.activity == 4):
            self.calories = self.BMR * 1.725
        elif (self.activity == 5):
            self.calories = self.BMR * 1.9
        account_info["recomended_calories"] = int(self.calories)

    def __calculate_recomended_proteins__(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_proteins = account_info["percent_proteins"]

        account_info["recomended_proteins"] =  int(self.recomended_calories * \
            self.percent_proteins)

    def __calculate_recomended_carbs__(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_carbs = account_info["percent_carbs"]

        account_info["recomended_carbs"] = int(self.recomended_calories * \
            self.percent_carbs)

    def __calculate_recomended_fats__(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_fats = account_info["percent_fats"]

        account_info["recomended_fats"] = int(self.recomended_calories * \
            self.percent_fats)

    @classmethod
    def crypt(cls, password):
        cls.pw_bytes = password.encode('utf-8')
        return SHA256.new(cls.pw_bytes).hexdigest()

# one catch exception
    def match_user_password(self, user_name, password):
        user = self.session.query(account_db).filter_by(name=user_name).one()
        return user.password == self.crypt(password)


info = {
    "name": "Josefina",
    "password": Account.crypt("11da3cu7"),
    "gender": 'F',
    "weight": 56,
    "height": 176,
    "activity_level": 3,
    "age": 25,
    "recomended_calories": 0,
    "recomended_proteins": 0,
    "recomended_carbs": 0,
    "recomended_fats": 0,
    "percent_proteins": 0.4,
    "percent_carbs": 0.4,
    "percent_fats": 0.2
}


res = Account(models.connect())
res.add_account(info)
#res.update_field("Fiona", "weight", 58)
# print(info)
#print(res.match_user_password("Fiona", "11da3cu7"))
