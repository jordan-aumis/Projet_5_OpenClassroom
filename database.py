"""This module concern our database it has all the table filling and database connector"""
import mysql.connector
import requests


class Data:
    """This class is our database for openfoodfact it has all
     the function to create all the tables and fill it"""
    my_database = mysql.connector.connect(
        user="jordan", password="Bluechicken0", host="localhost", database="openfoodfact")

    my_cursor = my_database.cursor(buffered=True)
    count_cat = 0
    count_prod = 0
    count_sub = 0
    @classmethod
    def empty_data(cls, array, new_array):
        """This replace the Empty data by a string"""
        for data_value in array:
            if data_value is None:
                data_value = "None"
            elif data_value == "":
                data_value = "Empty"
            new_array.append(data_value.replace("'", ""))

    @classmethod
    def empty_score(cls, array, new_array):
        """This replace the empty nutriscore by a 'x'"""
        for score_value in array:
            if score_value is None:
                score_value = "x"
            new_array.append(score_value)

    def create_tables(self):
        """Create all the tables and erase them if they already exist"""
        self.my_cursor.execute("DROP TABLE IF EXISTS Substitut")
        self.my_cursor.execute("DROP TABLE IF EXISTS Product")
        self.my_cursor.execute("DROP TABLE IF EXISTS Category")
        self.my_cursor.execute("CREATE TABLE Category \
            (id smallint(3) unsigned NOT NULL AUTO_INCREMENT\
                 PRIMARY KEY, name varchar(200) CHARACTER SET utf8 NOT NULL)")
        self.my_cursor.execute("CREATE TABLE Product (id smallint(3)\
             unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY, name varchar(200)\
                  CHARACTER SET utf8, nutriscore char(1) CHARACTER SET utf8, description varchar(4000) CHARACTER SET utf8, category_id smallint(3)\
                       unsigned NOT NULL, FOREIGN KEY(category_id)\
                            REFERENCES Category(id), url varchar(1000) CHARACTER SET utf8)")
        self.my_cursor.execute("CREATE TABLE Substitut (id smallint(3)\
             unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,\
                  name varchar(50) CHARACTER SET utf8, nutriscore char(1)\
                CHARACTER SET utf8,description varchar(4000)\
                    CHARACTER SET utf8, category_id smallint(3)\
                            unsigned NOT NULL, FOREIGN KEY(category_id)\
                            REFERENCES Category(id), product_id smallint(3)\
                        unsigned NOT NULL, FOREIGN KEY(product_id)\
                    REFERENCES Product(id), url varchar(1000) CHARACTER SET utf8)")


    @classmethod
    def fill_category(cls, cursor):
        """This will fill the data in the table Category of our database"""
        new_name = []
        request_page = requests.get("http://fr.openfoodfacts.org/categories&json=1")
        tags_json = request_page.json().get('tags')
        name_cat = []
        count = 2
        for name in tags_json:
            name_cat.append(name.get('name'))
        while count < 12:
            for name in name_cat:
                new_name.append(name.replace("'", ""))
            cursor.execute("INSERT INTO Category (name)\
                VALUES ('{}')".format(new_name[count]))
            count += 1
        return new_name

    def fill_data_prod(self, cursor, cat):
        """This will fill the data in the table Product of our database"""
        while self.count_cat < 10:
            self.count_prod = 0
            product_req = requests.get("http://fr.openfoodfacts.org/categorie/{}/1.json"\
                .format(cat[self.count_cat + 2]))
            products_json = product_req.json().get('products')
            product_name = []
            nutrition_score = []
            ingredients = []
            prod_url = []
            for prod in products_json:
                product_name.append(prod.get('product_name_fr'))
                ingredients.append(prod.get('ingredients_text_fr'))
                nutrition_score.append(prod.get('nutrition_grade_fr'))
                prod_url.append(prod.get('url'))
            new_product_name = []
            new_nutrition_score = []
            new_ingredients = []
            new_url = []
            self.empty_data(product_name, new_product_name)
            self.empty_data(ingredients, new_ingredients)
            self.empty_data(prod_url, new_url)
            self.empty_score(nutrition_score, new_nutrition_score)
            while self.count_prod < 10:
                cursor.execute("INSERT INTO Product (name, nutriscore, \
                description, category_id, url) VALUES\
                ('{}', '{}', '{}', {}, '{}')".format(new_product_name[self.count_prod],\
                    new_nutrition_score[self.count_prod], \
                    new_ingredients[self.count_prod], self.count_cat+1, new_url[self.count_prod]))
                self.count_prod += 1
            self.count_cat += 1

    @classmethod
    def fill_sub(cls, prod, cat, score, sub):
        """This will fill the data in the table Sustitut of our database"""
        Data.my_cursor.execute("INSERT INTO Substitut \
        (name, nutriscore, description,\
            category_id, product_id, url) SELECT name, nutriscore,\
            description, category_id, {}, url FROM Product WHERE\
            category_id={} AND nutriscore<'{}' AND id={}".format(
                prod, cat, score, sub))
        Data.count_sub += 1
        Data.my_database.commit()

    def __init__(self):
        print("Chargement en cours ...")
        self.create_tables()
        cat = self.fill_category(self.my_cursor)
        self.fill_data_prod(self.my_cursor, cat)
        self.my_database.commit()
        input("Operation réussi appuyez sur entrée")
