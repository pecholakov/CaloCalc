from models import connect
from food import *
from account import *
from consumed_food import *
from statistics import *


class Controller:

    # after login user must be settled
    @classmethod
    def login(cls, user_name, password):
        if Account.match_user_password(cls.session, user_name, password):
            cls.session = connect()
            cls.food_record  = Food(cls.session)
            cls.account = Account(cls.session)
            cls.consumed_food = ConsumedFood(cls.session)
            cls.statistics = Statistics(cls.session)
            cls.loaded_user = cls.account.get_by_name(user_name)
            cls.logged_in = True
        else:
            # Wrong account or password!
            return None    
            
    @classmethod
    def log_out(cls):
        cls.loaded_user = None
        cls.logged_in = False
        cls.session.close()

    @classmethod
    def create_account(cls, account_info):
        cls.account.add(account_info)

    @classmethod
    def add_food(cls, food_info):
        cls.food_record.add(food_info)

    @classmethod
    def modify_food_record(cls, food_name, field, value):
        cls.food_record.update_field(food_name, field, value)

    @classmethod
    def remove_food_record(cls, food_name):
        cls.food_record.remove_by_name(food_name)

    @classmethod
    def get_food_record(cls, food_name):
        cls.food_record.get(food_name)

    @classmethod
    def update_account_info(cls, field, value):
        cls.account.update_field(cls.loaded_user.id, field, value)

    @classmethod
    def add_consumed_food(cls, multriplier, food_info):
        cls.consumed_food.add(cls.loaded_user.id, multriplier, food_info)

    @classmethod
    def get_current_consumed(cls, account_id):
        cls.consumed_food.get_statistics(cls.loaded_user.id)      
    
    @classmethod
    def remove_consumed_food_id(cls, food_id):
        cls.consumed_food.remove_record_by_id(food_id)

    @classmethod
    def save_statistics(cls):
        cls.statistics.add(cls.loaded_user.id)

    @classmethod
    def generate_statisics_file(cls, account_id):
        pass           
