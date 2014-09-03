from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

import models


class ConsumedFood:

    def __init__(self, session):
        self.session = session

    def add_consumed_food(self, account_id, multiplier, food_info):
        consumed_food = models.ConsumedFood(
            account_id=account_id,
            multiplier_quantity=multiplier,
            name=food_info["name"],
            quantity=food_info["quantity"] * multiplier,
            calories=food_info["calories"] * multiplier,
            proteins_g=food_info["proteins"] * multiplier,
            carbs_g=food_info["carbs"] * multiplier,
            fats_g=food_info["fats"] * multiplier
        )
        self.session.add(consumed_food)
        self.session.commit()

# TODO: lower() check where to add
    def remove_consumed_food(self, food_name):
        try:
            res = self.session.query(models.ConsumedFood). \
                filter(models.ConsumedFood.name == food_name). \
                delete(synchronize_session='fetch')
            self.session.commit()
        except (NoResultFound):
            self.session.rollback()
    
    def remove_consumed_food_by_id(self, food_id):
        try:
            res = self.session.query(models.ConsumedFood). \
                filter(models.ConsumedFood.id == food_id). \
                delete(synchronize_session='fetch')
            self.session.commit()
        except (NoResultFound):
            self.session.rollback()       

    def give_consumed_food(self, account_id):
        consumed_food = self.session.query(models.ConsumedFood).filter_by(
            account_id=account_id).all()
        return consumed_food

    def give_consumed_calories(self, account_id):
        consumed_calories = self.session.query(
            func.sum(models.ConsumedFood.calories).label("total_calories")). \
            filter(account_id == account_id).one()
        return int(consumed_calories.total_calories)

    def give_consumed_protein_calories(self, account_id):
        consumed_proteins = self.session.query(
            func.sum(models.ConsumedFood.proteins_g).label("protein_grams")).\
            filter(account_id == account_id).one()
        return int(consumed_proteins.protein_grams * 4)  

    def give_consumed_carbs_calories(self, account_id):
        consumed_carbs = self.session.query(
            func.sum(models.ConsumedFood.carbs_g).label("carbs_grams")). \
            filter(account_id == account_id).one()
        return int(consumed_carbs.carbs_grams * 4)

    def give_consumed_fats_calories(self, account_id):
        consumed_fats = self.session.query(
            func.sum(models.ConsumedFood.fats_g).label("fats_grams")). \
            filter(account_id == account_id).one()
        return int(consumed_fats.fats_grams * 9)                   

info = {
    "name": "peanut butter",
    "quantity": 100,
    "calories": 578,
    "proteins": 24,
    "carbs": 51.4,
    "fats": 41
}

res = ConsumedFood(models.connect())
#res.add_consumed_food(1, 4.2, info)
#res.remove_consumed_food_by_id(4)
#print(res.remove_consumed_food("peanut butter"))
