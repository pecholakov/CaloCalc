CaloCalc
========

CaloCalc calculates the daily caloric intake and how many of those calories come from proteins, fats and carbohydrates. It also calculates what is the needed daily calorie intake for the user, based on information entered about its body.

Database with food
-------
In a database is stored information about the type of the food, quantity, calories, chemical composition (fats, carbohydrates and proteins). In this database the user can add new food, to modify values.

Account
-------
Every user can make his own account where will be stored statisics about him. The user must add basic information about his body when creates a new account. That includes weight, height, gender, activity level and age. 
To calculate the needed daily caloric intake, CaloCalc uses the Harris-Benedict equations. The necessary calories are separated into three groups - from fats, carbohydrates and proteins.

Statistics and synchronization
-------
CaloCalc stores statistics for the last month that can be presented in printable format. Users can check and modify consumed food till the moment of the check. 
CaloCalc synchronizes its time via NTP server and if internet connection is not available - from the current system time.

Dependencies:
-------
ntplib - https://pypi.python.org/pypi/ntplib/                                                
SQLAlchemy - https://pypi.python.org/pypi/SQLAlchemy
