import sys
import os

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
    Enum,
    CheckConstraint,
    create_engine
)
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session,
    backref
)
from sqlalchemy.ext.declarative import declarative_base

MAX_LENGTH = 64

def connect():
    engine = create_engine('sqlite:///cc.db', echo=False)
    Session = sessionmaker(bind=engine)
    return Session()


Base = declarative_base()
engine = create_engine('sqlite:///cc.db', echo=False)
session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False))

# TODO: add constraints

"""Extend the base class

        Provides a nicer representation when a class instance is printed.
        Found on the SA wiki
"""
class Base():

    def __repr__(self):
        return "%s(%s)" % (
            (self.__class__.__name__),
            ', '.join(["%s=%r" % (key, getattr(self, key))
                       for key in sorted(self.__dict__.keys())
                       if not key.startswith('_')]))


DeclarativeBase = declarative_base(cls=Base)
metadata = DeclarativeBase.metadata

class Account(DeclarativeBase):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    name = Column(String(MAX_LENGTH), nullable=False, unique=True)
    password = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)
    gender = Column(Enum("M", "F", name="genders_enum"),
                    nullable=False)
    activity_level = Column(Integer,
                            CheckConstraint(
                                "activity_level > 0 AND activity_level <= 5"),
                            nullable=False)
    age = Column(Integer, nullable=False)
    recomended_calories = Column(Integer)
    recomended_proteins = Column(Integer)
    recomended_carbs = Column(Integer)
    recomended_fats = Column(Integer)
    percent_proteins = Column(Float,
            CheckConstraint("percent_proteins > 0 AND percent_proteins < 1"))
    percent_carbs = Column(Float,
            CheckConstraint("percent_carbs > 0 AND percent_carbs < 1"))
    percent_fats = Column(Float,
            CheckConstraint("percent_fats > 0 AND percent_fats < 1"))


class Statistics(DeclarativeBase):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    date = Column(Date, nullable=False)
    recomended_calories = Column(Integer, nullable=False)
    recomended_proteins = Column(Integer, nullable=False)
    recomended_carbs = Column(Integer, nullable=False)
    recomended_fats = Column(Integer, nullable=False)
    consumed_calories = Column(Integer)
    consumed_proteins = Column(Integer)
    consumed_carbs = Column(Integer)
    consumed_fats = Column(Integer)

    account = relationship(
        "Account", backref=backref("statistics", order_by=id))


class ConsumedFood(DeclarativeBase):
    __tablename__ = 'consumedFood'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    multiplier_quantity = Column(Float)
    name = Column(String(MAX_LENGTH), primary_key=False)
    quantity = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    proteins_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)

    account = relationship(
        "Account", backref=backref("consumedFood", order_by=id))


class Food(DeclarativeBase):
    __tablename__ = 'foodDB'
    id = Column(Integer, primary_key=True)
    name = Column(String(MAX_LENGTH), nullable=False, unique=True)
    quantity = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    proteins_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)


DeclarativeBase.metadata.create_all(engine)
