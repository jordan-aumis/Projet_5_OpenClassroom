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

bobo = interface_sub("1", 3)
print(bobo)