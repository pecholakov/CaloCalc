import unittest
import sys

sys.path.append("/home/petyo/Documents/CaloCalc/src//")
from account import Account
import models

class TestAccoundController(unittest.TestCase):

    def setUp(self):
        self.tester = Account(models.connect())
        self.info = {
            "name": "Fiona",
            "password": Account.crypt("48da3cu7"),
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

    def test_add_account(self):
        self.tester.add(self.info)
        self.account_atributes = (self.tester.get_by_name("Fiona")).__dict__
        self.dict = {}
        self.dict["name"] = self.account_atributes["name"]
        self.dict["password"] = self.account_atributes["password"]
        self.dict["weight"] = self.account_atributes["weight"]
        self.dict["height"] = self.account_atributes["height"]
        self.dict["gender"] = self.account_atributes["gender"]
        self.dict["activity_level"] = self.account_atributes["activity_level"]
        self.dict["age"] = self.account_atributes["age"]
        self.dict["recomended_calories"] = self.account_atributes["recomended_calories"]
        self.dict["recomended_proteins"] = self.account_atributes["recomended_proteins"]
        self.dict["recomended_carbs"] = self.account_atributes["recomended_carbs"]
        self.dict["recomended_fats"] = self.account_atributes["recomended_fats"]
        self.dict["percent_proteins"] = self.account_atributes["percent_proteins"]
        self.dict["percent_carbs"] = self.account_atributes["percent_carbs"]
        self.dict["percent_fats"] = self.account_atributes["percent_fats"]

        self.assertEqual(self.info, self.dict)
        self.tester.delete_account(self.dict["name"], self.dict["password"])

    def test_get_account_by_name(self):
        self.tester.add(self.info)
        self.assertEqual("Fiona", (self.tester.get_by_name("Fiona")).name)

if __name__ == '__main__':
    unittest.main()
