import unittest
import sys

sys.path.append("/home/petyo/Documents/CaloCalc/src//")
from food import Food
import models


class TestFoodController(unittest.TestCase):

    def setUp(self):
        self.tester = Food(models.connect())
        self.info = {
            "name": "peanut butter",
            "quantity": 100,
            "calories": 578,
            "proteins_g": 29.1,
            "carbs_g": 11.8,
            "fats_g": 46.1
        }

    def test_food_is_added(self):
        self.tester.add(self.info)
        self.food_atributes = (self.tester.get("peanut butter")).__dict__
        self.dict = {}
        self.dict["name"] = self.food_atributes["name"]
        self.dict["quantity"] = self.food_atributes["quantity"]
        self.dict["calories"] = self.food_atributes["calories"]
        self.dict["proteins_g"] = self.food_atributes["proteins_g"]
        self.dict["carbs_g"] = self.food_atributes["carbs_g"]
        self.dict["fats_g"] = self.food_atributes["fats_g"]

        self.assertEqual(self.info, self.dict)
        self.tester.remove_by_name("peanut butter")

    def test_update_field_calories(self):
        self.tester.add(self.info)
        self.tester.update_field("peanut butter", "calories", 500)
        self.assertEqual(500, (self.tester.get("peanut butter")).__dict__["calories"])
        self.tester.remove_by_name("peanut butter")

    def test_remove_existing_food_record(self):
        self.tester.add(self.info)
        self.tester.remove_by_name("peanut butter")
        self.assertEqual(None, self.tester.get("peanut butter"))

    def test_remove_not_existing_food_record(self):
        self.assertEqual(None, self.tester.remove_by_name("peanut butter"))

    def test_get_not_existing_food_record(self):
        self.assertEqual(None, self.tester.get("peanut butter"))

    def test_get_existing_food_record(self):
        self.tester.add(self.info)
        self.assertEqual("peanut butter", (self.tester.get("peanut butter")).name)
        self.tester.remove_by_name("peanut butter")             

if __name__ == '__main__':
    unittest.main()
