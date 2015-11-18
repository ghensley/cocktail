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

  safe_columns = ["name"]

  id = Column(INTEGER, primary_key=True, nullable = False)
  name = Column(VARCHAR(255), nullable = True, unique=True)
  image_location = Column(VARCHAR(255), nullable = True)

class ingredient(Base):
  __tablename__ = 'ingredients'
  __table_args__ = {'schema': SCHEMA}

  safe_columns = ["name","available","slot"]

  id = Column(INTEGER, primary_key=True, nullable = False)
  name = Column(VARCHAR(255), nullable = True, unique=True)
  available = Column(BOOLEAN, nullable = True)
  image_location = Column(VARCHAR(255), nullable = True)
  slot = Column(INTEGER, nullable = True)

class ingredient_in_cocktail(Base):
  __tablename__ = 'ingredients_in_cocktails'
  __table_args__ = {'schema': SCHEMA}

  safe_columns = ["parts","cocktail_id","ingredient_id"]

  id = Column(INTEGER, primary_key=True, nullable = False)
  parts = Column(FLOAT, nullable = False)
  cocktail_id = Column(INTEGER, ForeignKey(cocktail.id, onupdate="CASCADE", ondelete="CASCADE"), nullable = False)
  ingredient_id = Column(INTEGER, ForeignKey(ingredient.id, onupdate="CASCADE", ondelete="CASCADE"), nullable = False)

  cocktail = relationship("cocktail", backref="ingredients_in_cocktail")
  ingredient = relationship("ingredient", backref="cocktails_is_in")


