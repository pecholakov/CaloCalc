from sqlalchemy.orm import sessionmaker

import models
from models import Food as food_db


class Food:

    def __init__(self, session):
        self.session = session

    def add(self, food_info):
        food = food_db(
            name=food_info["name"].lower(),
            quantity=food_info["quantity"],
            calories=food_info["calories"],
            proteins_g=food_info["proteins"],
            carbs_g=food_info["carbs"],
            fats_g=food_info["fats"]
        )
        self.session.add(food)
        self.session.commit()

    def update_field(self, food_name, field, value):
        food = self.session.query(food_db).filter_by(
            name=food_name.lower()).first()
        setattr(food, field, value)
        self.session.commit()

# TODO: check lower()
    def get(self, name):
        try:
            food = self.session.query(food_db).filter_by(
                name=name).one()
        except (NoResultFound):
            self.session.rollback()
        else:
            return food        

info = {
    "name": "SEEDS butter",
    "quantity": 100,
    "calories": 578,
    "proteins_g": 29.1,
    "carbs_g": 11.8,
    "fats_g": 46.1
}


res = Food(models.connect())
# res.add_food(info)
#res.update_field("SEEDS butter", "proteins_g", 22)
