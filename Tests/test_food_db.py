import unittest
from food_db import FoodRecord


'''
TODO more unit tests
'''

class TestFoodRecord(unittest.TestCase):

    def setUp(self):
        self.food_record = FoodRecord('Peanut Butter', 100, 578, 29.1,
                                       11.8, 46.1)

    def test_quantity_is_added_correctly(self):
        self.assertEqual(self.food_record.name, 'Peanut Butter')



if __name__ == '__main__':
    unittest.main()



