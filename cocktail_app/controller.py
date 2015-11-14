from flask import g, Blueprint, render_template, current_app, request, redirect, url_for
from cocktail_app import app

@app.route('/')
def index:
  return render_template('index.html')
