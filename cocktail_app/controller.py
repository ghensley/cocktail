from flask import g, Blueprint, render_template, current_app, request, redirect, url_for
from cocktail_app import app
import dao

@app.route('/')
def index():
  db = current_app.config["cocktail.db"]
  with dao.dao_session(db()) as dbo:
    cocktail_list = []
    cocktails = dbo.cocktails()
    for cocktail in cocktails:
      cocktail_info = {}
      cocktail_info["name"] = cocktail.name
      cocktail_info["id"] = cocktail.id
      cocktail_info["available"] = True
      ingredients_in_cocktail = cocktail.ingredients_in_cocktail
      cocktail_info["ingredients"] = []
      for ingredient_in_cocktail in ingredients_in_cocktail:
        ingredient_info = {}
        ingredient_info["name"] = ingredient_in_cocktail.ingredient.name
        if (ingredient_in_cocktail.ingredient.available is None or ingredient_in_cocktail.ingredient.available == False):
          cocktail_info["available"] = False
        ingredient_info["parts"] = ingredient_in_cocktail.parts
        cocktail_info["ingredients"].append(ingredient_info)
      cocktail_list.append(cocktail_info)
    return render_template('index.html', cocktails=cocktail_list)

@app.route('/ingredients', methods=['GET','POST'])
def ingredients():
  db = current_app.config["cocktail.db"]
  if request.method == 'GET':
    with dao.dao_session(db()) as dbo:
      return render_template('ingredients.html', dbo.ingredients()) 

@app.route('/create_cocktail', methods=['GET','POST'])
def create_cocktail():
  if request.method == 'GET':
    return render_template('create_cocktail.html')
  db = current_app.config["cocktail.db"]
  with dao.dao_session(db()) as dbo:
    dbo.create_cocktail(request.form)
    return redirect(url_for('index'))

@app.route('/create_ingredient', methods=['GET','POST'])
def create_ingredient():
  if request.method == 'GET':
    return render_template('create_ingredient.html')
  db = current_app.config["cocktail.db"]
  with dao.dao_session(db()) as dbo:
    dbo.create_ingredient(request.form)
    return redirect(url_for('index'))
 
@app.route('/add_ingredient_to_cocktail/<int:id>', methods=['GET','POST'])
def add_ingredient_to_cocktail(id):
  db = current_app.config["cocktail.db"]
  if request.method == 'GET':
    with dao.dao_session(db()) as dbo:
      return render_template('add_ingredient_to_cocktail.html', ingredients = dbo.ingredients(), cocktail_id = id)
  with dao.dao_session(db()) as dbo:
    dbo.add_ingredient_to_cocktail(request.form)
    return redirect(url_for('index'))  
