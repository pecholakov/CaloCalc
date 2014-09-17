from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from Crypto.Hash import SHA256

from models import connect
from models import Account as account_db


class Account:

    def __init__(self, session):
        self.session = session

    def add(self, account_info):
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
        try:
            self.session.commit()
        except (SQLAlchemyError):
            self.session.rollback()
            return None

    def update_field(self, account_id, field, value):
        self.percents = ["percent_proteins", "percent_carbs", "percent_fats"]
        user = self.get(account_id)
        if user is not None:
            if isinstance(field, dict):
                if self.check_percents(field["percent_proteins"],
                                       field["percent_carbs"],
                                       field["percent_fats"]):
                    user.percent_proteins = field["percent_proteins"]
                    user.percent_carbs = field["percent_carbs"]
                    user.percent_fats = field["percent_fats"]
                    account_info = user.__dict__.copy()
                    self.__calculate_nutrition__(account_info)
                    user.recomended_calories = \
                        account_info["recomended_calories"]
                    user.recomended_proteins = \
                        account_info["recomended_proteins"]
                    user.recomended_carbs = account_info["recomended_carbs"]
                    user.recomended_fats = account_info["recomended_fats"]
                else:
                    return None
            else:
                setattr(user, field, value)
                account_info = user.__dict__.copy()
                self.__calculate_nutrition__(account_info)
                user.recomended_calories = account_info["recomended_calories"]
                user.recomended_proteins = account_info["recomended_proteins"]
                user.recomended_carbs = account_info["recomended_carbs"]
                user.recomended_fats = account_info["recomended_fats"]
            self.session.commit()

    def get(self, account_id):
        try:
            user = self.session.query(account_db).filter_by(
                id=account_id).one()
            return user
        except (NoResultFound):
            self.session.rollback()
            return None

    def get_by_name(self, account_name):
        try:
            user = self.session.query(account_db).filter_by(
                name=account_name).one()
            return user
        except (NoResultFound):
            self.session.rollback()
            return None

    def delete_account(self, user_name, password):
        if self.match_user_password(self.session, user_name, password):
            try:
                row = self.session.query(account_db). \
                    filter(account_db.name == user_name). \
                    delete(synchronize_session='fetch')
                self.session.commit()
            except:
                self.session.rollback()
                return None

    def __calculate_nutrition__(self, account_info):
        self.__calculate_recomended_calories(account_info)
        self.__calculate_recomended_proteins(account_info)
        self.__calculate_recomended_carbs(account_info)
        self.__calculate_recomended_fats(account_info)

# Harris–Benedict equations revised by Roza and Shizgal
    def __calculate_recomended_calories(self, account_info):
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

    def __calculate_recomended_proteins(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_proteins = account_info["percent_proteins"]

        account_info["recomended_proteins"] = int(self.recomended_calories *
                                                  self.percent_proteins)

    def __calculate_recomended_carbs(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_carbs = account_info["percent_carbs"]

        account_info["recomended_carbs"] = int(self.recomended_calories *
                                               self.percent_carbs)

    def __calculate_recomended_fats(self, account_info):
        self.recomended_calories = account_info["recomended_calories"]
        self.percent_fats = account_info["percent_fats"]

        account_info["recomended_fats"] = int(self.recomended_calories *
                                              self.percent_fats)

    @classmethod
    def crypt(cls, password):
        cls.pw_bytes = password.encode('utf-8')
        return SHA256.new(cls.pw_bytes).hexdigest()

    """ Method expects already crypted password"""
    @classmethod
    def match_user_password(cls, session, user_name, password):
        try:
            user = session.query(account_db).filter_by(name=user_name).one()
            return user.password == password
        except(NoResultFound):
            return False

    @classmethod
    def check_percents(cls, proteins, carbs, fats):
        return (proteins + carbs + fats) == 1
