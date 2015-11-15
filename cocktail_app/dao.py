import orm as cocktail_orm
from sqlalchemy.orm import class_mapper 
from sqlalchemy import func
from decimal import Decimal
from sqlalchemy import desc, asc
from sqlalchemy_utils import *

class dao_session:
    def __init__(self, session):
        self.session = session
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.close()
    def close(self):
        self.session.commit()
        self.session.close()
    def cocktails(self):
        query = self.session.query(cocktail_orm.cocktail).order_by("name asc")
        return query.all()
    def ingredients(self):
        query = self.session.query(cocktail_orm.ingredient).order_by("name asc")
        return query.all()
    def cocktail(self, id):
        return self.session.query(cocktail_orm.cockail).filter(cocktail_orm.cocktail.id == id).first()
    def ingredient(self, id):
        return self.session.query(cocktail_orm.ingredient).filter(cocktail_orm.ingredient.id == id).first()
    def create_ingredient(self,attrs):
        ingredient = cocktail_orm.ingredient()
        dao_session.setAttrsSafe(ingredient, attrs)
        self.session.add(ingredient)
    def edit_ingredient(self,id, attrs):
        ingredient = self.session.query(cocktail_orm.ingredient).filter(cocktail_orm.ingredient.id == id).first()
        dao_session.setAttrsSafe(ingredient, attrs)        
    def create_cocktail(self,attrs):
        cocktail = cocktail_orm.cocktail()
        dao_session.setAttrsSafe(cocktail, attrs)
        self.session.add(cocktail)
    def add_ingredient_to_cocktail(self,attrs):
        ingredient_in_cocktail = cocktail_orm.ingredient_in_cocktail()
        dao_session.setAttrsSafe(ingredient_in_cocktail, attrs)
        self.session.add(ingredient_in_cocktail) 
    @staticmethod
    def setAttrsSafe(obj, attrs):
        for key, value in attrs.iteritems():
            if key in obj.safe_columns:
                setattr(obj, key, value)

def serializeList(models, *proxies):
    return [serialize(model, *proxies) for model in models]

def serialize(model, *proxies):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict       
    output = dict((c, getattr(model, c)) for c in columns)
    for key in proxies:
        proxy = getattr(model, key)
        if hasattr(proxy, '__iter__'):
            output.update({key: list(proxy)})
        else:
            output.update({key: proxy})

    return output

import datetime
import json

class DaoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()
        elif isinstance(obj, Decimal):
            return str(obj)
        elif isinstance(obj, bus_orm.Base):
            return serialize(obj)
        else:
            return super(DaoEncoder, self).default(obj)

