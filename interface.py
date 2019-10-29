import mysql.connector
import requests
import classes

def interface():
    my_database = mysql.connector.connect(user="jordan", password="Bluechicken0", host="localhost", database="openfoodfact")

    my_cursor = my_database.cursor(buffered=True)

    is_on = True

    def show_id_name(cursor):
        for num, name in cursor.fetchall():
            print(num,":",name)
    
    def show_product(cursor):
        for name, nutriscore, description in cursor.fetchall():
            print("name:", name)
            print("description:", description)
            print("nutriscore:", nutriscore)

    category = classes.Category(my_cursor)
    my_database.commit()
    classes.Product.fill_data_prod(my_cursor)
    my_database.commit()
    while is_on:
        print("|**********************************************************************************************|")
        print("|*                                                                                            *|")
        print("|*                   Bienvenue sur l'application pur beurre                                   *|")
        print("|*                                                                                            *|")
        print("|**********************************************************************************************|")
        print("Cette application à pour but de Chercher un produit et de le substitué par un autre produit avec un meilleur score nutritionelle.")
        print("entrez le numero correspondant :")
        print("1: Nouvelle recherche,     2: Substitut enregistré,     0: Quitter")
        print("")
        choice = input()
        print(" ")
        if choice == "1":
            print("Choisissez une catégorie:")
            print("0: Quitter")
            print(" ")
            my_cursor.execute("SELECT * FROM Category")
            show_id_name(my_cursor)
            print("")
            new_choice = input()
            int_new_choice = int(new_choice)
            print(" ")
            if new_choice == "0":
                is_on = False
        #     val = int(new_choice)
            my_cursor.execute("SELECT name FROM Category WHERE id={}".format(int_new_choice))
            cat_name = my_cursor.fetchone()[0]
            print("Choisissez votre produit pour la categorie '{}':".format(cat_name))
            my_cursor.execute("SELECT id, name FROM Product WHERE category_id={}".format(int_new_choice))
            show_id_name(my_cursor)
            print("")
            choice_prod = input()
            int_choice_prod = int(choice_prod)
        #     val_prod = int(choice_prod)
            my_cursor.execute("SELECT name, nutriscore, description FROM Product WHERE id={}".format(int_choice_prod))
        #     product = my_cursor.fetchone()
            print("Voici les données du produits choisit :")
            show_product(my_cursor)
            print("")
            input("appuyez sur entrée")
            print("Choisissez le substitut proposé par rapport au point de nutrition")
            my_cursor.execute("SELECT nutriscore FROM Product WHERE id={}".format(int_choice_prod))
            nutriscore_prod = my_cursor.fetchone()
            my_cursor.execute("SELECT id, name FROM Product WHERE category_id={} AND nutriscore<'{}'".format(int_new_choice, nutriscore_prod[0]))
        #     print(" ")
        #     print("entrez le numero de la ligne afin d'enregistrer votre substitut pour le revoir dans l'historique")
        #     show_data(my_cursor)
        #     save_sub = int(input())
            # my_cursor.execute("SELECT * FROM Product WHERE category_id={} AND nutriscore<'{}'".format(int_new_choice, nutriscore_prod[0], save_sub))
            show_id_name(my_cursor)
            sub_choice = input()
            int_sub_choice = int(sub_choice)
            print("Voici les données du substitut choisi :")
            my_cursor.execute("SELECT name, nutriscore, description FROM Product WHERE id={}".format(int_sub_choice))
            show_product(my_cursor)
            input("Appuyez sur entrée pour enregistrer.")
            my_cursor.execute("INSERT INTO Substitut (name, nutriscore, description, category_id, product_id) SELECT name, nutriscore, description, category_id, {} FROM Product WHERE category_id={} AND nutriscore<'{}' AND id={}".format(int_choice_prod, int_new_choice, nutriscore_prod[0], int_sub_choice))
            my_database.commit()
        elif choice == "2":
            print("voici l'historique des recherches, entrez le numero pour voir les details")
            my_cursor.execute("SELECT id, name FROM Substitut")
            show_id_name(my_cursor)
            detail_sub = input()
            int_detail_sub = int(detail_sub)
            my_cursor.execute("SELECT product_id FROM Substitut WHERE id={}".format(int_detail_sub))
            prod_id = my_cursor.fetchone()[0]
            print(prod_id)
            print("Vous avez substitué:")
            my_cursor.execute("SELECT name, nutriscore, description FROM Product WHERE id={}".format(prod_id))
            show_product(my_cursor)
            print("par:")
            my_cursor.execute("SELECT name, nutriscore, description FROM Substitut WHERE id={}".format(int_detail_sub))
            show_product(my_cursor)
            input("Appuyez sur entré")

        elif choice == "0":
            print("Bye bye et à bientôt sur pur beurre !")
            is_on = False
        else:
            print("je n'ai pas compris vôtre choix")
interface()