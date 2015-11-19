from flask import flash, g, Blueprint, render_template, current_app, request, redirect, url_for
from cocktail_app import app
import dao
import thread
import time

GPIO_DICT = {}
mark = {}
GPIO_DICT[1] = 11
GPIO_DICT[2] = 10
GPIO_DICT[3] = 24
GPIO_DICT[4] = 18
GPIO_DICT[5] = 8
GPIO_DICT[6] = 25
GPIO_DICT[7] = 7

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
  with dao.dao_session(db()) as dbo:
    if request.method == 'POST':
      ingredients = dbo.ingredients()
      checked = []
      slot = {}
      for e in request.form:
        f = e.split("_")
        if f[0] == "checked":
          checked.append(int(f[1]))
        elif f[0] == "slot":
          if request.form[e]!="None":
            print request.form[e]
            slot[int(f[1])] = int(request.form[e])
      
      print slot 
      print checked
      for ingredient in ingredients:
        if ingredient.id in checked:
          dbo.edit_ingredient(ingredient.id, {"available":True})
        else:
          dbo.edit_ingredient(ingredient.id, {"available":False})
        if ingredient.id in slot:
          dbo.edit_ingredient(ingredient.id, {"slot": slot[ingredient.id]})
        else:
          dbo.edit_ingredient(ingredient.id, {"slot": None})
      
      
    return render_template('ingredients.html', ingredients=dbo.ingredients())

def pour(slot, length_of_pour, pre_wait):
  time.sleep(pre_wait)
  gpio = GPIO_DICT[slot]
  try:
    f= open ('/sys/class/gpio/unexport','w')
    f.write(str(gpio))
    f.close()
  except IOError as e:
    print "Probably already closed"
  #Export pin number
  f= open ('/sys/class/gpio/export','w')
  f.write(str(gpio))
  f.close()
  #Define Pin Direction as Output for LED

  path = '/sys/class/gpio/gpio' + str(gpio) + '/direction'
  f = open (path,'w')
  f.write('out')
  f.close()
  path = '/sys/class/gpio/gpio' + str(gpio) + '/value'
  f = open (path,'w')
  f.write('1')
  mark[slot] = time.time()
  f.close()
  print "Open " + str(gpio) + " for " + str(length_of_pour)
  time.sleep(length_of_pour)
  f = open (path,'w')
  f.write('0')
  print time.time() - mark[slot]
  f.close()
  print "Closing " + str(gpio) 
  #GPIO export
  f = open ('/sys/class/gpio/unexport','w')
  f.write(str(gpio))
  f.close()
@app.route('/make_cocktail/<int:id>')
def make_cocktail(id):
  total_pour_time = 6.0
  longest_pour = 0.0
  db = current_app.config["cocktail.db"]
  with dao.dao_session(db()) as dbo:
    cocktail = dbo.cocktail(id)
    total_parts = 0
    for ingredients_in_cocktail in cocktail.ingredients_in_cocktail:
      if ingredients_in_cocktail.ingredient.slot is None:
        flash("Cocktail cannot be made. Ingredients are missing.")
        return redirect(url_for('index'))
      total_parts = total_parts + ingredients_in_cocktail.parts
    flash('Cocktail poured!')
    for ingredients_in_cocktail in cocktail.ingredients_in_cocktail:
      pour_time = (ingredients_in_cocktail.parts/total_parts)*total_pour_time
      if (pour_time > longest_pour):
        longest_pour = pour_time
      thread.start_new_thread(pour, (ingredients_in_cocktail.ingredient.slot, pour_time,0.0))
    thread.start_new_thread(pour, (GPIO_DICT[7], total_pour_time + 1.0,longest_pour))
    return redirect(url_for('index'))

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
    return redirect(url_for('add_ingredient_to_cocktail', id=id))  
