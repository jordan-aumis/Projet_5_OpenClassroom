DROP TABLE IF EXISTS Substitut;
DROP TABLE IF EXISTS Product;
DROP TABLE IF EXISTS Category;

CREATE TABLE Category (
id smallint(3) unsigned NOT NULL AUTO_INCREMENT,
name varchar(200) CHARACTER SET utf8 NOT NULL,
PRIMARY KEY (id)
) ENGINE=InnoDB;

CREATE TABLE Product (
id smallint(3) unsigned NOT NULL AUTO_INCREMENT,
name varchar(200) CHARACTER SET utf8,
nutriscore char(1) CHARACTER SET utf8,
description varchar(4000) CHARACTER SET utf8,
category_id smallint(3) unsigned NOT NULL,
PRIMARY KEY (id),
CONSTRAINT fk_id_category
 FOREIGN KEY (category_id)
REFERENCES Category(id)
) ENGINE=InnoDB;

CREATE TABLE Substitut (
id smallint(3) unsigned NOT NULL AUTO_INCREMENT,
name varchar(50) CHARACTER SET utf8,
nutriscore char(1) CHARACTER SET utf8,
description varchar(4000) CHARACTER SET utf8,
category_id smallint(3) unsigned NOT NULL,
product_id smallint(3) unsigned NOT NULL,
PRIMARY KEY (id),
 FOREIGN KEY (product_id)
REFERENCES Product(id),
FOREIGN KEY (category_id)
REFERENCES Category(id)
) ENGINE=InnoDB;