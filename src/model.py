import sys 
import os

from sqlalchemy import Column, ForeignKey, Integer, String, Float, Date, CheckConstraint
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

 
Base = declarative_base()
engine = create_engine('sqlite:///cc.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

MAX_LENGTH = 64

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True)
    name = Column(String(MAX_LENGTH), nullable=False)
    password = Column(String, nullable = False)

    account = relationship("Account", uselist=False, backref="users")
    
# Добавяне на ограничения
# Еквивалнтност на users.id && accounts.id 
class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key = True)
    weight = Column(Float, nullable = False)
    height = Column(Integer, nullable = False)
    waist = Column(Float, nullable = False)
    hip = Column(Float, nullable = False)
    activity_level = Column(Integer, 
        CheckConstraint("activity_level > 0 AND activity_level <= 5"), 
        nullable = False)
    age = Column(Integer, nullable = False)
    recomended_calories = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))

    consumed_food = relationship("ConsumedFood", uselist=False, backref="accounts")
    stats = relationship("Statistics", uselist=False, backref="accounts")

# TODO: Must add recomended and taken nutrition
class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key = True)
    date = Column(Date, nullable = False)
    recomended_calories = Column(Integer, nullable = False)
    consumed_calories = Column(Integer)

    account_id = Column(Integer, ForeignKey('accounts.id'))

class Food(Base):
    __tablename__ = 'foodDB'
    id = Column(Integer, primary_key = True)
    name = Column(String(MAX_LENGTH), nullable = False)
    quantity = Column(Float, nullable = False)
    calories = Column(Integer, nullable = False)
    proteins = Column(Float, nullable = False)
    carbs = Column(Float, nullable = False)
    fats = Column(Float, nullable = False)

    # def __repr__(self):
    #     return "<Food(id='%s', name='%s', quantity='%s', calories='%s', proteins'%s', carbs = '%s', fats = '%s')>" % (
    #         self.id, self.name, self.quantity, self.calories, self.proteins, self.carbs,
    #         self.fats)

class ConsumedFood(Base):
    __tablename__ = 'consumbedFood' 
    id = Column(Integer, primary_key = True)
    multiplier_quantity = Column(Float)
    name = Column(String(MAX_LENGTH), primary_key = False)
    quantity = Column(Float, nullable = False)
    calories = Column(Integer, nullable = False)
    proteins = Column(Float, nullable = False)
    carbs = Column(Float, nullable = False)
    fats = Column(Float, nullable = False)

    account_id = Column(Integer, ForeignKey('accounts.id'))


Base.metadata.create_all(engine)
