from sqlalchemy.orm import sessionmaker
from Crypto.Hash import SHA256
from sqlalchemy.orm.attributes import instance_state
from sqlalchemy.orm import object_session
from sqlalchemy.orm.util import has_identity

import models
import consumed_food, statistics


class Account:

    def __init__(self, session):
        self.session = session

    def add_account(self, account_info):
        self.__calculate_nutrition__(account_info)
        account = models.Account(
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
        user = self.session.query(models.Account).filter_by(
            name=user_name).first()
        setattr(user, field, value)
        # print(user.__dict__, "@@@@@@@@@@@@@@@")
        # print("############################")
        user_info = user.__dict__
        self.__calculate_nutrition__(user_info)
        #print(dir(user))
        user.recomended_calories = user_info["recomended_calories"]
        # setattr(user, "recomended_calories",
        # user.__dict__["recomended_calories"])
        self.session.add(user)
        self.session.commit()

        

# Harris–Benedict equations revised by Roza and Shizgal
    def __calculate_recomended_calories__(self, account_info):
        if (account_info["gender"] == 'M'):
            self.BMR = 88.362 + (13.397 * account_info["weight"]) + \
                (4.799 * account_info["height"]) - (5.677 * account_info["age"])

        if (account_info["gender"] == 'F'):
            self.BMR = 447.593 + (9.247 * account_info["weight"]) + \
                (3.098 * account_info["height"]) - (4.330 * account_info["age"])

        if (account_info["activity_level"] == 1):
            self.calories = self.BMR * 1.2
        elif (account_info["activity_level"] == 2):
            self.calories = self.BMR * 1.375
        elif (account_info["activity_level"] == 3):
            self.calories = self.BMR * 1.55
        elif (account_info["activity_level"] == 4):
            self.calories = self.BMR * 1.725
        elif (account_info["activity_level"] == 5):
            self.calories = self.BMR * 1.9
        account_info["recomended_calories"] = int(self.calories)

    def __calculate_recomended_proteins__(self, account_info):
       account_info["recomended_proteins"] = account_info["recomended_calories"] * \
            account_info["percent_proteins"]

    def __calculate_recomended_carbs__(self, account_info):
        account_info["recomended_carbs"] = account_info["recomended_calories"] * \
            account_info["percent_carbs"]

    def __calculate_recomended_fats__(self, account_info):
        account_info["recomended_fats"] = account_info["recomended_calories"] * \
            account_info["percent_fats"]

    def __calculate_nutrition__(self, account_info):
        self.__calculate_recomended_calories__(account_info)
        self.__calculate_recomended_proteins__(account_info)
        self.__calculate_recomended_carbs__(account_info)
        self.__calculate_recomended_fats__(account_info)

    @classmethod
    def __crypt__(cls, password):
        cls.pw_bytes = password.encode('utf-8')
        return SHA256.new(cls.pw_bytes).hexdigest()

    # def check_password(self, given_pass, password_hash):
    #     return SHA256.new(given_pass).hexdigest() == password_hash

    def match_user_password(self, user, password):
        for row in self.session.query(models.Account).filter_by(name=user):
            return row.password == self.__crypt__(password)

        
        
        


info = {
    "name" : "Fiona",
    "password" : Account.__crypt__("11da3cu7"),
    "gender" : 'F',
    "weight" : 51,
    "height" : 173,
    "activity_level" : 4,
    "age" : 23,
    "recomended_calories" : 0,
    "recomended_proteins" : 0,
    "recomended_carbs" : 0,
    "recomended_fats" : 0,
    "percent_proteins" : 0.4,
    "percent_carbs" : 0.4,
    "percent_fats" : 0.2
}


res = Account(models.connect())
# res.add_account(info)
res.update_field("Fiona", "weight", 56)
# print(info)
# Account.add_account()
# print(res.update_field("Borisious", "age",  28))
