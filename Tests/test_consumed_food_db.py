import unittest
import sys

sys.path.append("/home/petyo/Documents/CaloCalc/src/")
from consumed_food import ConsumedFood
from account import Account
import models


class TestConsumedFoodController(unittest.TestCase):

    def setUp(self):
        self.account_info = {
            "name": "Fiona",
            "password": "some_password",
            "gender": 'F',
            "weight": 56,
            "height": 176,
            "activity_level": 3,
            "age": 23,
            "recomended_calories": 0,
            "recomended_proteins": 0,
            "recomended_carbs": 0,
            "recomended_fats": 0,
            "percent_proteins": 0.4,
            "percent_carbs": 0.4,
            "percent_fats": 0.2
        }
        self.tester_account = Account(models.connect())
        self.tester_account.add(self.account_info)
        self.account = self.tester_account.get_by_name("Fiona")
        self.tester = ConsumedFood(models.connect())
        self.multiplier = 3.5

        self.info = {
            "name": "peanut butter",
            "quantity": 100,
            "calories": 578,
            "proteins_g": 29.1,
            "carbs_g": 11.8,
            "fats_g": 46.1
        }

    def tearDown(self):
        self.tester_account.delete_account("Fiona", "some_password")
        self.tester.remove_record_by_id(1)

    def test_add_food_to_database(self):
        self.tester.add(self.account.id, self.multiplier, self.info)
        self.food_atributes = (self.tester.get_consumed_food(self.account.id))[0].__dict__
        self.dict = {}
        self.dict["name"] = self.food_atributes["name"]
        self.dict["quantity"] = self.food_atributes["quantity"]
        self.dict["calories"] = self.food_atributes["calories"]
        self.dict["proteins_g"] = self.food_atributes["proteins_g"]
        self.dict["carbs_g"] = self.food_atributes["carbs_g"]
        self.dict["fats_g"] = self.food_atributes["fats_g"]
        # self.assertEqual(self)
        # self.assertEqual(self.info, self.dict)
        self.tester.remove_record_by_id(1)

if __name__ == '__main__':
    unittest.main()
