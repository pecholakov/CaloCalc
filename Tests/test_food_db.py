import unittest
import sys

sys.path.append("/home/petyo/Documents/CaloCalc/src//")
from food import Food
import models


class TestFoodController(unittest.TestCase):

    def setup(self):
        pass

    def test_quantity_is_added_correctly(self):
        food_controller = Food(models.connect())
        info = {
            "name": "seeds butter",
            "quantity": 100,
            "calories": 578,
            "proteins_g": 29.1,
            "carbs_g": 11.8,
            "fats_g": 46.1
        }
        food_controller.add(info)
        self.assertEqual(info["name"], (food_controller.get("seeds butter")).name)



if __name__ == '__main__':
    unittest.main()
