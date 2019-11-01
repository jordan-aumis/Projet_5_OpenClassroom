import mysql.connector
import classes
import requests

MY_DATABASE = mysql.connector.connect(
    user="jordan", password="Bluechicken0", host="localhost", database="openfoodfact")

MY_CURSOR = MY_DATABASE.cursor(buffered=True)

def show_id_name(cursor):
    for num, name in cursor.fetchall():
            print(num, ":", name)

def show_product(cursor):
    for name, nutriscore, description in cursor.fetchall():
        print("name:", name)
        print("description:", description)
        print("nutriscore:", nutriscore)

def fill_category(cursor):
    new_name = []
    Url_page = "http://fr.openfoodfacts.org/categories&json=1"
    request_page = requests.get(Url_page)
    category_json = request_page.json()
    tags_json = category_json.get('tags')
    name_cat = []
    count = 2
    for n in tags_json:
        name_cat.append(n.get('name'))
    while count < 13:
        for name in name_cat:
            new_name.append(name.replace("'", ""))
        cursor.execute("INSERT INTO Category (name)\
            VALUES ('{}')".format(new_name[count]))
        count += 1
    return new_name

def fill_data_prod(cursor, cat):
    count_cat = 0
    while count_cat < 10:
        count_prod = 0
        url_product = "http://fr.openfoodfacts.org/categorie/{}/1.json"\
            .format(cat[count_cat + 2])
        product_req = requests.get(url_product)
        products = product_req.json()
        products_json = products.get('products')
        product_name = []
        nutrition_score = []
        ingredients = []
        for prod in products_json:
            product_name.append(prod.get('product_name_fr'))
            ingredients.append(prod.get('ingredients_text_fr'))
            nutrition_score.append(prod.get('nutrition_grade_fr'))
        new_product_name = []
        new_nutrition_score = []
        new_ingredients = []
        for prod in product_name:
            if prod == None:
                prod = "None"
            elif prod == "":
                prod = "Empty"
            new_product_name.append(prod.replace("'", ""))
        for text in ingredients:
            if text == None:
                text = "None"
            elif text == "":
                text = "None"
            new_ingredients.append(text.replace("'", ""))
        for score in nutrition_score:
            if score == None:
                score = "x"
            new_nutrition_score.append(score)
        while count_prod < 10:
            cursor.execute("INSERT INTO Product (name, nutriscore, \
            description, category_id) VALUES\
            ('{}', '{}', '{}', {})".format(new_product_name[count_prod],\
                new_nutrition_score[count_prod], \
                new_ingredients[count_prod], count_cat+1))
            count_prod += 1
        count_cat += 1

def fill_sub(prod, cat, score, sub, cursor):
    cursor.execute("INSERT INTO Substitut \
    (name, nutriscore, description,\
        category_id, product_id) SELECT name, nutriscore,\
        description, category_id, {} FROM Product WHERE\
        category_id={} AND nutriscore<'{}' AND id={}".format(
            prod, cat, score, sub))
    cursor.commit()

if __name__=='__main__':
    bobo = fill_category(MY_CURSOR)
    fill_data_prod(MY_CURSOR, bobo)
    MY_DATABASE.commit()
