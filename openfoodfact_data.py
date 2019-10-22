import requests
import mysql.connector

# class Dbopenfoodfact:

#   def __init__(self, name, host, user, passwd):
#     self.connect = mysql.connector.connect(user=user, password=pwd, host=host, database=name)

Url_page = "http://fr.openfoodfacts.org/categories&json=1"
request_page = requests.get(Url_page)
category_json = request_page.json()
tags_json = category_json.get('tags')
name_cat = []
for n in tags_json:
  name_cat.append(n.get('name'))

my_database = mysql.connector.connect(user="jordan", password="Bluechicken0", host="localhost", database="openfoodfact")

my_cursor = my_database.cursor()

count = 0
new_name = []
while count < 10:
  for name in name_cat:
    new_name.append(name.replace("'", ""))
    

  sql_formula_cat = ("INSERT INTO Category (name) VALUES ('{}')".format(new_name[count]))
  my_cursor.execute(sql_formula_cat)
  count += 1

my_database.commit()

count = 0

url_product = "http://fr.openfoodfacts.org/categorie/{}/1.json".format(name_cat[count])

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
sql_formula_cat_id = ("SELECT id FROM Category WHERE name='{}'".format(new_name[count]))
my_cursor.execute(sql_formula_cat_id)
cat_id = my_cursor.fetchone()[0]
print(new_product_name)
print(new_nutrition_score[count])
print(new_ingredients[count])
print(cat_id)

while count < 10:
  sql_formula_prod = ("INSERT INTO Product (name, nutriscore, description, category_id) VALUES ('{}', '{}', '{}', {})".format(new_product_name[count], new_nutrition_score[count], new_ingredients[count], cat_id))
  my_cursor.execute(sql_formula_prod)
  count += 1

my_database.commit()
print(url_product)
