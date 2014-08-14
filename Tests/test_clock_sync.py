import unittest
from clock_sync import TimeSynchronization

'''
    How to make unit tests for time synchronization
'''

class TestClockSyncronization(unittest.TestCase):

    def setUp(self):
        self.time = TimeSynchronization()

    def test_year(self):
        self.res = self.time.sync_clock_ntp()

        self.assertEqual(2014, self.res.tm_year)


if __name__ == '__main__':
    unittest.main()
