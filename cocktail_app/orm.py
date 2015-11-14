from sqlalchemy import Column, ForeignKeyConstraint, Index, PrimaryKeyConstraint, text
from sqlalchemy.dialects.mysql import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import TypeDecorator
from sqlalchemy import types
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import ForeignKey, Table
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy_utils import *

Base = declarative_base()
SCHEMA = 'cocktail'

class cocktail(Base):
  __tablename__ = 'cocktails'
  __table_args__ = {'schema': SCHEMA}

  id = Column(INTEGER, primary_key=True, nullable = False)
  name = Column(VARCHAR(255), nullable = True)
  image_location = Column(VARCHAR(255), nullable = True)

class ingredient_in_cocktail(Base):
  __tablename__ = 'ingredients_in_cocktails'
  __table_args__ = {'schema': SCHEMA}
  id = Column(INTEGER, primary_key=True, nullable = False)
  parts = Column(FLOAT, nullable = False)
  cocktail_id = Column(Integer, ForeignKey('cocktail.id'))
  ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
  
  cocktails = relationship("cocktail", backref=backref('ingredient_in_cocktail', order_by=id))
  ingredients = relationship("ingredient", backref=backref('ingredient_in_cocktail', order_by=id))

class ingredient(Base):
  __tablename__ = 'ingredients'
  __table_args__ = {'schema': SCHEMA}

  id = Column(INTEGER, primary_key=True, nullable = False)
  name = Column(VARCHAR(255), nullable = True)
  image_location = Column(VARCHAR(255), nullable = True)
