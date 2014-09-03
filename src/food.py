from sqlalchemy.orm import sessionmaker

import models

class Food:

    def __init__(self, session):
        self.session = session

    def add_food(self, food_info):
        food = models.Food(
                name=food_info["name"].lower(),
                quantity=food_info["quantity"],
                calories=food_info["calories"],
                proteins_g=food_info["proteins"],
                carbs_g=food_info["carbs"],
                fats_g=food_info["fats"]
            )
        self.session.add(food)
        self.session.commit()

# izchislqvane na kaloriite
    def update_field(self, food_name, field, value):
        food = self.session.query(models.Food).filter_by(
            name=food_name.lower()).first()
        setattr(food, field, value)
        self.session.commit()       

info = {
    "name" : "SEEDS butte",
    "quantity" : 100,
    "calories" : 578,
    "proteins_g" : 29.1,
    "carbs_g" : 11.8,
    "fats_g" : 46.1
}        

#TODO: GET FOOD RECORD

res = Food(models.connect())
#res.add_food(info)
res.update_field("SEEDS butte", "proteins_g", 22)