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
                proteins=food_info["proteins"],
                carbs=food_info["carbs"],
                fats=food_info["fats"]
            )
        self.session.add(food)
        self.session.commit()

#preizchislqvane 
    def update_field(self, food_name, field, value):
        food = self.session.query(models.Food).filter_by(
            name=food_name.lower()).first()
        setattr(food, field, value)
        self.session.commit()       

info = {
    "name" : "butter",
    "quantity" : 100,
    "calories" : 578,
    "proteins" : 29.1,
    "carbs" : 11.8,
    "fats" : 46.1
}        

res = Food(models.connect())
#res.add_food(info)
res.update_field("SEEDS butter", "proteins", 22)