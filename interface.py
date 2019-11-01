import database

def menu():
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
    print("1: Nouvelle recherche,\n2: Substitut enregistré,\n0: Quitter")
    print("")

def interface_prod(cat):
    database.MY_CURSOR.execute(
        "SELECT name FROM Category WHERE id={}".format(cat))
    cat_name = database.MY_CURSOR.fetchone()[0]
    print("Choisissez votre produit pour la categorie '{}': \
        0: Quitter".format(cat_name))
    database.MY_CURSOR.execute(
        "SELECT id, name FROM Product WHERE category_id={}".format(cat))
    database.show_id_name(database.MY_CURSOR)
    print("")

def interface_detail_prod(prod):
    database.MY_CURSOR.execute(
        "SELECT name, nutriscore, description\
                FROM Product WHERE id={}".format(prod))
    print("Voici les données du produits choisit :")
    database.show_product(database.MY_CURSOR)
    print("")
    input("appuyez sur entrée")

def interface_sub(prod, cat):
    print("Choisissez le substitut proposé par rapport au point de nutrition:   \
        0: Quitter")
    database.MY_CURSOR.execute(
        "SELECT nutriscore FROM Product WHERE id={}".format(prod))
    nutriscore_prod = database.MY_CURSOR.fetchone()
    database.MY_CURSOR.execute("SELECT id, name FROM Product\
    WHERE category_id={} AND nutriscore<'{}'".format(
        cat, nutriscore_prod[0]))
    return nutriscore_prod[0]

def interface_detail_sub(sub):
    print("Voici les données du substitut choisi :")
    database.MY_CURSOR.execute(
        "SELECT name, nutriscore, description\
        FROM Product WHERE id={}".format(sub))
    database.show_product(database.MY_CURSOR)

def history_menu():
    print(
        "voici l'historique des recherches,\
                entrez le numero pour voir les details.  0:Quitter")
    database.MY_CURSOR.execute("SELECT id, name FROM Substitut")
    database.show_id_name(database.MY_CURSOR)

def history(sub):
    database.MY_CURSOR.execute(
        "SELECT product_id FROM Substitut WHERE id={}".format(sub))
    prod_id = database.MY_CURSOR.fetchone()[0]
    print("Vous avez substitué:")
    database.MY_CURSOR.execute(
        "SELECT name, nutriscore, description FROM Product WHERE id={}".format(prod_id))
    database.show_product(database.MY_CURSOR)
    print("par:")
    database.MY_CURSOR.execute(
        "SELECT name, nutriscore,\
                description FROM Substitut WHERE id={}".format(sub))
    database.show_product(database.MY_CURSOR)
    input("Appuyez sur entrée")

def select_cat():
    print("Choisissez une catégorie:   0: Quitter")
    print(" ")
    database.MY_CURSOR.execute("SELECT * FROM Category")
    database.show_id_name(database.MY_CURSOR)
    print("")

def validate_answer():
    while True:
        try:
            val = int(input())
            return str(val)
        except ValueError:
            print("je n'ai pas compris vôtre choix")
        else:
            break

def interface():
    while True:
        menu()
        choice = input()
        print(" ")
        if choice == "1":
            select_cat()
            new_choice = validate_answer()
            if new_choice == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_new_choice = int(new_choice)
            print(" ")
            interface_prod(int_new_choice)
            # database.MY_CURSOR.execute(
            #     "SELECT name FROM Category WHERE id={}".format(int_new_choice))
            # cat_name = database.MY_CURSOR.fetchone()[0]
            # print("Choisissez votre produit pour la categorie '{}': \
            #     0: Quitter".format(cat_name))
            # database.MY_CURSOR.execute(
            #     "SELECT id, name FROM Product WHERE category_id={}".format(int_new_choice))
            # database.show_id_name(database.MY_CURSOR)
            # print("")
            choice_prod = validate_answer()
            if choice_prod == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_choice_prod = int(choice_prod)
            interface_detail_prod(int_choice_prod)
            # database.MY_CURSOR.execute(
            #     "SELECT name, nutriscore, description\
            #          FROM Product WHERE id={}".format(int_choice_prod))
            # print("Voici les données du produits choisit :")
            # database.show_product(database.MY_CURSOR)
            # print("")
            # input("appuyez sur entrée")
            score = interface_sub(int_choice_prod, int_new_choice)
            print("")
            # print("Choisissez le substitut proposé par rapport au point de nutrition:   \
            #     0: Quitter")
            # database.MY_CURSOR.execute(
            #     "SELECT nutriscore FROM Product WHERE id={}".format(int_choice_prod))
            # nutriscore_prod = database.MY_CURSOR.fetchone()
            # database.MY_CURSOR.execute("SELECT id, name FROM Product\
            # WHERE category_id={} AND nutriscore<'{}'".format(
            #     int_new_choice, nutriscore_prod[0]))
            if database.MY_CURSOR.fetchone() is None:
                print("Substitut indisponible essayez avec un autre produit")
                print("")
                input("appuyez sur entrée pour continuer")
                continue
            else:
                database.show_id_name(database.MY_CURSOR)
            sub_choice = validate_answer()
            if sub_choice == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_sub_choice = int(sub_choice)
            interface_detail_sub(int_sub_choice)
            input("Appuyez sur entrée pour enregistrer.")
            # database.MY_CURSOR.execute("INSERT INTO Substitut \
            # (name, nutriscore, description,\
            #  category_id, product_id) SELECT name, nutriscore,\
            #  description, category_id, {} FROM Product WHERE\
            #  category_id={} AND nutriscore<'{}' AND id={}".format(
            #      int_choice_prod, int_new_choice, score, int_sub_choice))
            # database.MY_DATABASE.commit()
            database.fill_sub(int_choice_prod, int_new_choice, score, int_sub_choice, database.MY_CURSOR)
        elif choice == "2":
            history_menu()
            detail_sub = validate_answer()
            if detail_sub == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_detail_sub = int(detail_sub)
            history(int_detail_sub)
            # print(
            #     "voici l'historique des recherches,\
            #          entrez le numero pour voir les details.  0:Quitter")
            # database.MY_CURSOR.execute("SELECT id, name FROM Substitut")
            # database.show_id_name(database.MY_CURSOR)
            # detail_sub = validate_answer()
            # if detail_sub == "0":
            #     print("Bye bye et à bientôt sur pur beurre !")
            #     break
            # int_detail_sub = int(detail_sub)
            # database.MY_CURSOR.execute(
            #     "SELECT product_id FROM Substitut WHERE id={}".format(int_detail_sub))
            # prod_id = database.MY_CURSOR.fetchone()[0]
            # print(prod_id)
            # print("Vous avez substitué:")
            # database.MY_CURSOR.execute(
            #     "SELECT name, nutriscore, description FROM Product WHERE id={}".format(prod_id))
            # database.show_product(database.MY_CURSOR)
            # print("par:")
            # database.MY_CURSOR.execute(
            #     "SELECT name, nutriscore,\
            #          description FROM Substitut WHERE id={}".format(int_detail_sub))
            # database.show_product(database.MY_CURSOR)
            # input("Appuyez sur entrée")
        elif choice == "0":
            print("Bye bye et à bientôt sur pur beurre !")
            break
        else:
            print("je n'ai pas compris vôtre choix")


interface()
