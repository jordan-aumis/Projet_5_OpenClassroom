import mysql.connector
import requests

def fill_data_category():
  Url_page = "http://fr.openfoodfacts.org/categories&json=1"
  request_page = requests.get(Url_page)
  category_json = request_page.json()
  tags_json = category_json.get('tags')
  name_cat = []
  for n in tags_json:
    name_cat.append(n.get('name'))
    count = 0
    new_name = []
  while count < 10:
    for name in name_cat:
      new_name.append(name.replace("'", "")) 
    sql_formula_cat = ("INSERT INTO Category (name) VALUES ('{}')".format(new_name[count]))
    my_cursor.execute(sql_formula_cat)
    count += 1
    my_database.commit()

def fill_data_prod(NameCat, CatId):
  count = 0
  url_product = "http://fr.openfoodfacts.org/categorie/{}/1.json".format(NameCat)
  product_req = requests.get(url_product)
  products = product_req.json()
  products_json = products.get('products')
  product_name = []
  nutrition_score = []
  ingredients = []
  for p in products_json:
    product_name.append(p.get('product_name_fr'))
    ingredients.append(p.get('ingredients_text_fr'))
    nutrition_score.append(p.get('nutrition_grade_fr'))
  new_product_name = []
  new_nutrition_score = []
  new_ingredients = []
  for prod in product_name:
    if prod == None:
      prod = "None"
    elif prod == "":
      prod ="Empty"
    new_product_name.append(prod.replace("'", ""))
  for text in ingredients:
    if text == None:
      text = "None"
    elif text == "":
      text="None"
    new_ingredients.append(text.replace("'", ""))
  for score in nutrition_score:
    if score == None:
      score = "x"
    new_nutrition_score.append(score)
  while count < 10:
    sql_formula_prod = ("INSERT INTO Product (name, nutriscore, description, category_id) VALUES ('{}', '{}', '{}', {})".format(new_product_name[count], new_nutrition_score[count], new_ingredients[count], CatId))
    my_cursor.execute(sql_formula_prod)
    count += 1
    my_database.commit()

my_database = mysql.connector.connect(user="jordan", password="Bluechicken0", host="localhost", database="openfoodfact")

my_cursor = my_database.cursor()

is_on = True

def show_data(cursor):
  for show in cursor.fetchall():
    print(show)



fill_data_category()
print("|**********************************************************************************************|")
print("|*                                                                                            *|")
print("|*                   Bienvenue sur l'application pur beurre                                   *|")
print("|*                                                                                            *|")
print("|**********************************************************************************************|")
print("")
print("Pour lancer une recherche tapez: 1 ")
print("Pour voir l'historique des enregistrements tapez: 2")
print("Pour quitter l'application tapez: 0")
print(" ")
while is_on:
  choice = input()

  if choice == "1":
    print("| Choisissez une category en tapant son id                                                  |")
    print("| Pour quitter l'application tapez: 0                                                           |")
    print(" ")
    sql_formula_show = "SELECT * FROM Category"
    my_cursor.execute(sql_formula_show)
    show_data(my_cursor)
    new_choice = input("Quel catégorie choisissez vous ?")
    if new_choice == "0":
      is_on = False
    val = int(new_choice)
    my_cursor.execute("SELECT name FROM Category WHERE id={}".format(val))
    cat_name = my_cursor.fetchone()
    print("vous avez choisi la category {}".format(cat_name))
    print("Veuillez choisir un produit en tapant son id")
    fill_data_prod(cat_name, val)
    my_cursor.execute("SELECT id, name FROM Product WHERE category_id={}".format(val))
    show_data(my_cursor)
    choice_prod = input("quel est votre produit ?")
    val_prod = int(choice_prod)
    my_cursor.execute("SELECT * FROM Product WHERE id={}".format(val_prod))
    product = my_cursor.fetchone()
    print("Voici le produit choisit :")
    print(product)
    input()
    my_cursor.execute("SELECT nutriscore FROM Product WHERE id={}".format(val_prod))
    nutriscore_prod = my_cursor.fetchone()
    my_cursor.execute("SELECT * FROM Product WHERE category_id={} AND nutriscore<'{}'".format(val, nutriscore_prod[0]))
    print("Voici les substituts proposé par rapport au point de nutrition")
    print(" ")
    print("entrez le numero de la ligne afin d'enregistrer votre substitut pour le revoir dans l'historique")
    show_data(my_cursor)
    save_sub = int(input())
    my_cursor.execute("SELECT * FROM Product WHERE category_id={} AND nutriscore<'{}' AND id={}".format(val, nutriscore_prod[0], save_sub))
    show_data(my_cursor)
    if save_sub == '0':
      is_on = False
    my_cursor.execute("INSERT INTO Substitut (name, nutriscore, description, category_id, product_id) SELECT name, nutriscore, description, category_id, id FROM Product WHERE category_id={} AND nutriscore<'{}' AND id={}".format(val, nutriscore_prod[0], save_sub))
  elif choice == "2":
    print("voici l'historique.")
    my_cursor.execute("SELECT * FROM Substitut")
    show_data(my_cursor)
  elif choice == "0":
    print("Bye bye et à bientôt sur pur beurre !")
    is_on = False
  else:
    print("je n'ai pas compris vôtre choix")