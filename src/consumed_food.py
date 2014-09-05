from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

import models
from models import ConsumedFood as consumed_food_db


class ConsumedFood:

    def __init__(self, session):
        self.session = session

    def add(self, account_id, multiplier, food_info):
        consumed_food = consumed_food_db(
            account_id=account_id,
            multiplier_quantity=multiplier,
            name=food_info["name"],
            quantity=food_info["quantity"] * multiplier,
            calories=int(food_info["calories"] * multiplier),
            proteins_g=round(food_info["proteins"] * multiplier, 2),
            carbs_g=round(food_info["carbs"] * multiplier, 2),
            fats_g=round(food_info["fats"] * multiplier, 2)
        )
        self.session.add(consumed_food)
        self.session.commit()

    def get_statistics(self, account_id):
        self.food_statistics = {}
        self.food_statistics["consumed_calories"] = \
            self.get_consumed_calories(account_id)
        self.food_statistics["consumed_proteins"] = \
            self.get_consumed_protein_calories(account_id)
        self.food_statistics["consumed_carbs"] = \
            self.get_consumed_carbs_calories(account_id)
        self.food_statistics["consumed_fats"] = \
            self.get_consumed_fats_calories(account_id)

        return self.food_statistics

    def remove_record_by_id(self, food_id):
        try:
            res = self.session.query(consumed_food_db). \
                filter(consumed_food_db.id == food_id). \
                delete(synchronize_session='fetch')
            self.session.commit()
        except (NoResultFound):
            self.session.rollback()

    def get_consumed_food(self, account_id):
        consumed_food = self.session.query(consumed_food_db).filter_by(
            account_id=account_id).all()
        return consumed_food

    def get_consumed_calories(self, account_id):
        consumed_calories = self.session.query(
            func.sum(consumed_food_db.calories).label("total_calories")). \
            filter(account_id == account_id).one()
        return int(consumed_calories.total_calories)

    def get_consumed_protein_calories(self, account_id):
        consumed_proteins = self.session.query(
            func.sum(consumed_food_db.proteins_g).label("protein_grams")).\
            filter(account_id == account_id).one()
        return int(consumed_proteins.protein_grams * 4)

    def get_consumed_carbs_calories(self, account_id):
        consumed_carbs = self.session.query(
            func.sum(consumed_food_db.carbs_g).label("carbs_grams")). \
            filter(account_id == account_id).one()
        return int(consumed_carbs.carbs_grams * 4)

    def get_consumed_fats_calories(self, account_id):
        consumed_fats = self.session.query(
            func.sum(consumed_food_db.fats_g).label("fats_grams")). \
            filter(account_id == account_id).one()
        return int(consumed_fats.fats_grams * 9)

info = {
    "name": "potatoes",
    "quantity": 100,
    "calories": 478,
    "proteins": 24,
    "carbs": 55.2,
    "fats": 41
}

res = ConsumedFood(models.connect())
