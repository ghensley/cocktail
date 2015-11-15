from flask import Flask
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

import cocktail_app.controller

DB_URI = "mysql://cocktail@localhost/cocktail"
db = app.config.get("cocktail.db")

if db is None:
    engine = create_engine(DB_URI)
    app.config["cocktail.db"] = sessionmaker(bind = engine)
