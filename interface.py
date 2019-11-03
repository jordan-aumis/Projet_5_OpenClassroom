"""This is the module where all the interface's code is"""
import database

class Interface:
    """This is the Interface classes which regroups
    all the function for the interface to work"""

    @classmethod
    def show_id_name(cls, cursor):
        """This will show only the id and name"""
        for num, name in cursor.fetchall():
            print(num, ":", name)

    @classmethod
    def show_product(cls, cursor):
        """This will show name, nutriscore and description"""
        for name, nutriscore, description, url in cursor.fetchall():
            print("NAME:", name)
            print("DESCRIPTION:", description)
            print("NUTRISCORE:", nutriscore)
            print("URL:", url)

    @classmethod
    def menu(cls):
        """This is the interface menu where you start the app,\
            you can choose what you want to do"""
        print("|***********************************************|")
        print("|*                                             *|")
        print("|*   Bienvenue sur l'application pur beurre    *|")
        print("|*                                             *|")
        print("|***********************************************|")
        print("Cette application vous permet de substituer un produit\
    par un autre avec un meilleure nutriscore*.")
        print("")
        print("Nutricore* = le score nutritionnelle par lettre, du produit")
        print("'a' = Meilleur score")
        print("'e' = le plus mauvais")
        print("'x' = score inconu ")
        print("")
        print("entrez le numero correspondant à votre commande:")
        print("1: Nouvelle recherche\n2: Substitut enregistré")
        print("3: Mise à jour des produits")
        print("0: Quitter")
        print("")

    def select_cat(self):
        """This will show the categories you can choose from"""
        print("Choisissez une catégorie:   0: Quitter")
        print(" ")
        database.Data.my_cursor.execute("SELECT * FROM Category")
        self.show_id_name(database.Data.my_cursor)
        print("")

    def interface_prod(self, cat):
        """This will show the list of product (id and name)\
            that you can choose from which category you chose"""
        database.Data.my_cursor.execute(
            "SELECT name FROM Category WHERE id={}".format(cat))
        cat_name = database.Data.my_cursor.fetchone()[0]
        print("Choisissez votre produit pour la categorie '{}': \
            0: Quitter".format(cat_name))
        print("")
        database.Data.my_cursor.execute(
            "SELECT id, name FROM Product WHERE category_id={}".format(cat))
        self.show_id_name(database.Data.my_cursor)
        print("")

    def interface_detail_prod(self, prod):
        """This show the detail of the product you chose"""
        database.Data.my_cursor.execute(
            "SELECT name, nutriscore, description, url\
                    FROM Product WHERE id={}".format(prod))
        print("Voici les données du produits choisit :")
        print("")
        self.show_product(database.Data.my_cursor)
        print("")
        input("appuyez sur entrée")

    @classmethod
    def not_availlable(cls):
        """This is when the substitute is not availlable it will print:"""
        print("Substitut indisponible essayez avec un autre produit")
        print("")
        input("appuyez sur entrée pour continuer")

    @classmethod
    def interface_sub(cls, prod, cat):
        """This is the list of substitut availlable you can choose from the product you chose"""
        print("Choisissez le substitut proposé par rapport au point de nutrition:   0: Quitter")
        print("")
        database.Data.my_cursor.execute(
            "SELECT nutriscore FROM Product WHERE id={}".format(prod))
        nutriscore_prod = database.Data.my_cursor.fetchone()
        database.Data.my_cursor.execute("SELECT id, name FROM Product\
        WHERE category_id={} AND nutriscore<'{}'".format(
            cat, nutriscore_prod[0]))
        return nutriscore_prod[0]

    def interface_detail_sub(self, sub):
        """This show the detail of the substitut you chose"""
        print("Voici les données du substitut choisi :")
        print("")
        database.Data.my_cursor.execute(
            "SELECT name, nutriscore, description, url\
            FROM Product WHERE id={}".format(sub))
        self.show_product(database.Data.my_cursor)

    def history_menu(self):
        """This is the start of the history it will show all search"""
        print(
            "voici l'historique des recherches,\
                    entrez le numero pour voir les details.  0:Quitter")
        database.Data.my_cursor.execute("SELECT id, name FROM Substitut")
        self.show_id_name(database.Data.my_cursor)

    def history(self, sub):
        """This is the detail of all the search you have done"""
        database.Data.my_cursor.execute(
            "SELECT product_id FROM Substitut WHERE id={}".format(sub))
        prod_id = database.Data.my_cursor.fetchone()[0]
        print("Vous avez substitué:")
        print("")
        database.Data.my_cursor.execute(
            "SELECT name, nutriscore, description, url FROM Product WHERE id={}".format(prod_id))
        self.show_product(database.Data.my_cursor)
        print("")
        print("PAR:")
        print("")
        database.Data.my_cursor.execute(
            "SELECT name, nutriscore,\
                    description, url FROM Substitut WHERE id={}".format(sub))
        self.show_product(database.Data.my_cursor)
        input("Appuyez sur entrée")

    def __init__(self):
        self.menu()

    @staticmethod
    def validate_answer(number):
        """This check if the answer is an integer"""
        while True:
            val = input()
            try:
                int(val)
            except ValueError:
                print("je n'ai pas compris vôtre choix")
                continue
            if int(val) > number:
                print("Ce numero est en dehors de la liste, essayez à nouveau.")
                continue
            else:
                return str(val)
