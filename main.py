"""THis is our main loop in order to run our programme"""
import interface
import database

def main():
    """The loop of my interface it regroups all the function above"""
    while True:
        menu = interface.Interface()
        choice = input()
        print(" ")
        if choice == "1":
            menu.select_cat()
            new_choice = menu.validate_answer(10)
            if new_choice == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_new_choice = int(new_choice)
            print(" ")
            menu.interface_prod(int_new_choice)
            choice_prod = menu.validate_answer(100)
            if choice_prod == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_choice_prod = int(choice_prod)
            menu.interface_detail_prod(int_choice_prod)
            score = menu.interface_sub(int_choice_prod, int_new_choice)
            print("")
            check = database.Data.my_cursor.fetchone()
            if check is None:
                menu.not_availlable()
                continue
            elif check is not None:
                menu.show_id_name(database.Data.my_cursor)
            sub_choice = menu.validate_answer(100)
            if sub_choice == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_sub_choice = int(sub_choice)
            menu.interface_detail_sub(int_sub_choice)
            input("Appuyez sur entrée pour enregistrer.")
            database.Data.fill_sub(int_choice_prod, int_new_choice, score,\
                int_sub_choice)
        elif choice == "2":
            menu.history_menu()
            detail_sub = menu.validate_answer(100)
            if detail_sub == "0":
                print("Bye bye et à bientôt sur pur beurre !")
                break
            int_detail_sub = int(detail_sub)
            menu.history(int_detail_sub)
        elif choice == "3":
            database.Data()
        elif choice == "0":
            print("Bye bye et à bientôt sur pur beurre !")
            break
        else:
            print("je n'ai pas compris vôtre choix")

if __name__ == '__main__':
    main()
