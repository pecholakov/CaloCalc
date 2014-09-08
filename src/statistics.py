import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
import tabulate

from models import connect
from models import Statistics as statistics_db
from account import Account
from consumed_food import ConsumedFood


class Statistics:

    def __init__(self, session):
        self.session = session

    def add(self, account_id):
        user = Account(self.session)
        user_info = user.get(account_id)

        consumed = ConsumedFood(self.session)
        consumed_food_info = consumed.get_statistics(account_id)
        statistics = statistics_db(
            account_id=account_id,
            date=datetime.date.today(),
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

    def get(self, account_id):
        statistics = self.session.query(statistics_db).filter_by(
            account_id=account_id).all()
        return statistics

 # TODO: add functionality
    def generate_stastics_file(self, account_id):
        statistic_rows = []
        table = self.get(account_id)

        result = []
        for entry in table:
            result.append([])
            l = [a for a in dir(entry) if not a.startswith('__') and not callable(getattr(entry,a))]
            for column in l:
                result[-1].append(column)

        column_titles = ["Date", "Recomended calories", "Consumed calories",
                         "Recomended proteins", "Consumed proteins",
                         "Recomended carbs", "Consumed carbs",
                         "Recomended fats", "Consumed fats"]
        #print(table)  
           