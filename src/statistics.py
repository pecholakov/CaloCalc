from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import models
import account, consumed_food

class Statistics:

    def __init__(self, session):
        self.session = session

    def add(self, account_id):
        pass  

# take consumedFood from current account /query/
#populate dict with info for the statistics by the account and its tied consumedFood    
    def  take_account_info(self, account_id):
        qry = self.session.query(models.Account, models.ConsumedFood)
        qry = qry.filter(models.Account.id==models.ConsumedFood.account_id).all()
        print(qry[0].Account.password)

    def take_consumed_food_info(self, account_id):
        pass         

res = Statistics(models.connect())
res.take_account_info(1)        