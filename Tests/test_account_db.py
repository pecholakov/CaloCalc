import unittest
import sys

sys.path.append("/home/petyo/Documents/CaloCalc/src/")
from account import Account
import models


class TestAccoundController(unittest.TestCase):

    def setUp(self):
        self.tester = Account(models.connect())
        self.account_password = Account.crypt("48da3cu7")
        self.info = {
            "name": "Fiona",
            "password": self.account_password,
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
        self.tester.add(self.info)

    def tearDown(self):
         self.tester.delete_account("Fiona", self.account_password)  

    def test_add_account(self):
        self.account_attributes = (self.tester.get_by_name("Fiona")).__dict__
        self.dict = {}
        self.dict["name"] = self.account_attributes["name"]
        self.dict["password"] = self.account_attributes["password"]
        self.dict["weight"] = self.account_attributes["weight"]
        self.dict["height"] = self.account_attributes["height"]
        self.dict["gender"] = self.account_attributes["gender"]
        self.dict["activity_level"] = self.account_attributes["activity_level"]
        self.dict["age"] = self.account_attributes["age"]
        self.dict["recomended_calories"] = self.account_attributes[
            "recomended_calories"]
        self.dict["recomended_proteins"] = self.account_attributes[
            "recomended_proteins"]
        self.dict["recomended_carbs"] = self.account_attributes[
            "recomended_carbs"]
        self.dict["recomended_fats"] = self.account_attributes[
            "recomended_fats"]
        self.dict["percent_proteins"] = self.account_attributes[
            "percent_proteins"]
        self.dict["percent_carbs"] = self.account_attributes["percent_carbs"]
        self.dict["percent_fats"] = self.account_attributes["percent_fats"]

        self.assertEqual(self.info, self.dict)
        self.tester.delete_account(self.dict["name"], self.dict["password"])

    def test_add_same_account_twice(self):
        self.assertIsNone(self.tester.add(self.info))

    def test_get_account_by_name(self):
        self.assertEqual("Fiona", (self.tester.get_by_name("Fiona")).name)

    def test_update_name(self):
        self.tester.update_field(
            (self.tester.get_by_name("Fiona")).id, "name", "Sophie")
        self.assertEqual("Sophie", (self.tester.get_by_name("Sophie")).name)
        self.tester.delete_account("Sophie", self.account_password)

    def test_update_pass(self):
        self.tester.update_field(
            (self.tester.get_by_name("Fiona")).id, "password", "49qw5")
        self.assertEqual("49qw5", (self.tester.get_by_name("Fiona")).password)
        self.tester.delete_account("Fiona", "49qw5")

    def test_update_weight(self):
        self.attribute = "weight"
        self.new_value = 50
        self.account_attributes = (
            self.tester.get_by_name("Fiona")).__dict__.copy()
        self.account_attributes[self.attribute] = self.new_value
        self.tester.__calculate_nutrition__(self.account_attributes)
        self.tester.update_field((self.tester.get_by_name("Fiona")).id,
                                 self.attribute, self.new_value)

        self.assertEqual(self.new_value,
                         getattr(self.tester.get_by_name("Fiona"),
                                 self.attribute))
        self.assertEqual(self.account_attributes["recomended_calories"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_calories)
        self.assertEqual(self.account_attributes["recomended_proteins"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_proteins)
        self.assertEqual(self.account_attributes["recomended_carbs"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_carbs)
        self.assertEqual(self.account_attributes["recomended_fats"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_fats)

    def test_update_height(self):
        self.attribute = "height"
        self.new_value = 60
        self.account_attributes = (
            self.tester.get_by_name("Fiona")).__dict__.copy()
        self.account_attributes[self.attribute] = self.new_value
        self.tester.__calculate_nutrition__(self.account_attributes)
        self.tester.update_field((self.tester.get_by_name("Fiona")).id,
                                 self.attribute, self.new_value)

        self.assertEqual(self.new_value,
                         getattr(self.tester.get_by_name("Fiona"),
                                 self.attribute))
        self.assertEqual(self.account_attributes["recomended_calories"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_calories)
        self.assertEqual(self.account_attributes["recomended_proteins"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_proteins)
        self.assertEqual(self.account_attributes["recomended_carbs"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_carbs)
        self.assertEqual(self.account_attributes["recomended_fats"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_fats)

    def test_update_gender(self):
        self.attribute = "gender"
        self.new_value = 'M'
        self.account_attributes = (
            self.tester.get_by_name("Fiona")).__dict__.copy()
        self.account_attributes[self.attribute] = self.new_value
        self.tester.__calculate_nutrition__(self.account_attributes)
        self.tester.update_field((self.tester.get_by_name("Fiona")).id,
                                 self.attribute, self.new_value)

        self.assertEqual(self.new_value,
                         getattr(self.tester.get_by_name("Fiona"),
                                 self.attribute))
        self.assertEqual(self.account_attributes["recomended_calories"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_calories)
        self.assertEqual(self.account_attributes["recomended_proteins"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_proteins)
        self.assertEqual(self.account_attributes["recomended_carbs"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_carbs)
        self.assertEqual(self.account_attributes["recomended_fats"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_fats)

    def test_update_activity_level(self):
        self.attribute = "activity_level"
        self.new_value = 5
        self.account_attributes = (
            self.tester.get_by_name("Fiona")).__dict__.copy()
        self.account_attributes[self.attribute] = self.new_value
        self.tester.__calculate_nutrition__(self.account_attributes)
        self.tester.update_field((self.tester.get_by_name("Fiona")).id,
                                 self.attribute, self.new_value)

        self.assertEqual(self.new_value,
                         getattr(self.tester.get_by_name("Fiona"),
                                 self.attribute))
        self.assertEqual(self.account_attributes["recomended_calories"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_calories)
        self.assertEqual(self.account_attributes["recomended_proteins"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_proteins)
        self.assertEqual(self.account_attributes["recomended_carbs"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_carbs)
        self.assertEqual(self.account_attributes["recomended_fats"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_fats)

    def test_update_age(self):
        self.attribute = "age"
        self.new_value = 60
        self.account_attributes = (
            self.tester.get_by_name("Fiona")).__dict__.copy()
        self.account_attributes[self.attribute] = self.new_value
        self.tester.__calculate_nutrition__(self.account_attributes)
        self.tester.update_field((self.tester.get_by_name("Fiona")).id,
                                 self.attribute, self.new_value)

        self.assertEqual(self.new_value,
                         getattr(self.tester.get_by_name("Fiona"),
                                 self.attribute))
        self.assertEqual(self.account_attributes["recomended_calories"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_calories)
        self.assertEqual(self.account_attributes["recomended_proteins"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_proteins)
        self.assertEqual(self.account_attributes["recomended_carbs"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_carbs)
        self.assertEqual(self.account_attributes["recomended_fats"],
                         (self.tester.get_by_name("Fiona")).
                         recomended_fats)

    def test_get_accout_by_id(self):
        self.assertEqual((self.tester.get_by_name("Fiona")),
                         self.tester.get(1))

    def test_delete_account(self):
        self.tester.delete_account("Fiona", self.account_password)
        self.assertIsNone(self.tester.get_by_name("Fiona"))

    def test_calculate_recomended_calories(self):
        self.assertEqual(2187, self.info["recomended_calories"])

    def test_calculate_recomended_proteins(self):
        self.assertEqual(874, self.info["recomended_proteins"])

    def test_calculate_recomended_carbs(self):
        self.assertEqual(874, self.info["recomended_carbs"])

    def test_calculate_recomended_fats(self):
        self.assertEqual(437, self.info["recomended_fats"])

    def test_match_user_password_true(self):
        self.assertTrue(
            self.tester.match_user_password(models.connect(),
                                            "Fiona",
                                            self.account_password))

    def test_match_user_password_false(self):
        self.assertFalse(
            self.tester.match_user_password(models.connect(),
                                            "Fiona",
                                            "wrong_password"))     

if __name__ == '__main__':
    unittest.main()
