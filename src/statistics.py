from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import models
#import account, consumed_food

class Statistics:

    def __init__(self, session):
        self.session = session

    def add(self, account_id):
        pass  

# take consumedFood from current account /query/
#populate dict with info for the statistics by the account and its tied consumedFood    
    def  take_account_info(self, account_id):
        user = self.session.query(models.Account).filter_by(
            id=account_id).all()

        return user

    def take_consumed_food_info(self, account_id):
        user = self.session.query(models.ConsumedFood).filter_by(
            account_id=account_id).all()
        for food in user:
            print(food, "\n")         

pes = Statistics(models.connect())
print(pes.take_account_info(1))        