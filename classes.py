import mysql.connector
import requests


class Category:
    new_name = []
    Url_page = "http://fr.openfoodfacts.org/categories&json=1"
    request_page = requests.get(Url_page)
    category_json = request_page.json()
    tags_json = category_json.get('tags')
    name_cat = []
    count = 2
    for n in tags_json:
        name_cat.append(n.get('name'))
    def __init__(self, cursor):
        while self.count < 13:
            for name in self.name_cat:
                self.new_name.append(name.replace("'", "")) 
            cursor.execute("INSERT INTO Category (name) VALUES ('{}')".format(self.new_name[self.count]))
            self.count += 1

class Product:
    def fill_data_prod(cursor):
        count_cat = 0
        while count_cat < 10:
            count_prod = 0
            url_product = "http://fr.openfoodfacts.org/categorie/{}/1.json".format(Category.new_name[count_cat + 2])
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
            while count_prod < 10:
                cursor.execute("INSERT INTO Product (name, nutriscore, description, category_id) VALUES ('{}', '{}', '{}', {})".format(new_product_name[count_prod], new_nutrition_score[count_prod], new_ingredients[count_prod], count_cat+1))
                count_prod += 1
            count_cat += 1
