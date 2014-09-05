from sqlalchemy.orm import sessionmaker 
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

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
            proteins_g=food_info["proteins_g"],
            carbs_g=food_info["carbs_g"],
            fats_g=food_info["fats_g"]
        )
        self.session.add(food)
        try:
            self.session.commit()
        except (SQLAlchemyError):
            self.session.rollback()

    
    def update_field(self, food_name, field, value):
        try:
            food = self.session.query(food_db).filter_by(
                name=food_name).one()
        except (NoResultFound):
            self.session.rollback()
        else:
            setattr(food, field, value)
            self.session.commit()

    def remove_by_name(self, food_name):
        try:
            row = self.session.query(food_db). \
                filter(food_db.name == food_name). \
                delete(synchronize_session='fetch')
            self.session.commit()
        except (NoResultFound):
            self.session.rollback()

    def get(self, name):
        try:
            food = self.session.query(food_db).filter_by(
                name=name).one()
        except (NoResultFound):
            self.session.rollback()
        else:
            return food


info = {
    "name": "peanut butter",
    "quantity": 100,
    "calories": 578,
    "proteins_g": 29.1,
    "carbs_g": 11.8,
    "fats_g": 46.1
}


res = Food(models.connect())
