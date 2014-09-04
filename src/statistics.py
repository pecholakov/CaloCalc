import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func

import clock_sync
import models
from models import Statistics as statistics_db
from account import Account  
from consumed_food import ConsumedFood
from prettytable import PrettyTable



class Statistics:

    def __init__(self, session):
        self.session = session

    def add(self, account_id):
        user = Account(self.session)
        user_info = user.get(account_id)

        consumed = ConsumedFood(self.session)
        consumed_food_info = consumed.get_statistics(account_id)

#TODO: try-except block
    def get(self, account_id):
        statistics = self.session.query(statistics_db).filter_by(
                account_id=account_id).all() 
        return statistics          
 
 #TODO: functionality       
    def generate_stastics_file(self, account_id):
        statistic_rows = []
        table = self.get(account_id)
        column_titles = ["Date", "Recomended calories", "Consumed calories",
                "Recomended proteins", "Consumed proteins",
                "Recomended carbs", "Consumed carbs",
                "Recomended fats", "Consumed fats"]    


# TODO: modify date
        today = datetime.date.today()
        statistics = statistics_db(
            account_id=account_id,
            date=today,
            recomended_calories=user_info.recomended_calories,
            recomended_proteins=user_info.recomended_proteins,
            recomended_carbs=user_info.recomended_carbs,
            recomended_fats=user_info.recomended_fats,
            consumed_calories=consumed_food_info["consumed_calories"],
            consumed_proteins=consumed_food_info["consumed_proteins"],
            consumed_carbs=consumed_food_info["consumed_carbs"],
            consumed_fats=consumed_food_info["consumed_fats"]
            )
        self.session.add(statistics)
        self.session.commit()    

pes = Statistics(models.connect())
#pes.add(3)
print(pes.generate_stastics_file(3))
# print(pes.take_account_info(1))
