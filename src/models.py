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
    global ENGINE
    global Session

    ENGINE = create_engine('sqlite:///cc.db', echo=False)
    Session = sessionmaker(bind=ENGINE)
    return Session()


Base = declarative_base()
engine = create_engine('sqlite:///cc.db', echo=False)
session = scoped_session(
    sessionmaker(bind=engine, autocommit=False, autoflush=False))

# TODO: add constraints
# TODO: check ForeignKeys (recomended stuff)


class Account(Base):
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
    recomended_proteins = Column(Float)
    recomended_carbs = Column(Float)
    recomended_fats = Column(Float)
    percent_proteins = Column(Float,
            CheckConstraint("percent_proteins > 0 AND percent_proteins < 1"))
    percent_carbs = Column(Float,
            CheckConstraint("percent_carbs > 0 AND percent_carbs < 1"))
    percent_fats = Column(Float,
            CheckConstraint("percent_fats > 0 AND percent_fats < 1"))

    consumed_food = relationship(
        "ConsumedFood", uselist=False, backref="accounts")
    stats = relationship("Statistics", uselist=False, backref="accounts")

class ConsumedFood(Base):
    __tablename__ = 'consumbedFood'
    id = Column(Integer, primary_key=True)
    multiplier_quantity = Column(Float)
    name = Column(String(MAX_LENGTH), primary_key=False)
    quantity = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    proteins_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)

    account_id = Column(Integer, ForeignKey('accounts.id'))

class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    recomended_calories = Column(Integer, nullable=False)
    recomended_proteins = Column(Float, nullable=False)
    recomended_carbs = Column(Float, nullable=False)
    recomended_fats = Column(Float, nullable=False)
    consumed_calories = Column(Integer)
    consumed_proteins = Column(Float)
    consumed_carbs = Column(Float)
    consumed_fats = Column(Float)

    account_id = Column(Integer, ForeignKey('accounts.id'))

class Food(Base):
    __tablename__ = 'foodDB'
    id = Column(Integer, primary_key=True)
    name = Column(String(MAX_LENGTH), nullable=False, unique=True)
    quantity = Column(Float, nullable=False)
    calories = Column(Integer, nullable=False)
    proteins_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)

    # def __repr__(self):
    #     return "<Food(id='%s', name='%s', quantity='%s', calories='%s', proteins'%s', carbs = '%s', fats = '%s')>" % (
    #         self.id, self.name, self.quantity, self.calories, self.proteins, self.carbs,
    #         self.fats)

# another fields for consumed food



Base.metadata.create_all(engine)
