CREATE DATABASE money;
USE money;
CREATE TABLE user
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT
);
CREATE TABLE category
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name TEXT NOT NULL,
    user_id INT(11) NOT NULL,
    type INT(11) NOT NULL,
    CONSTRAINT category_user_id_fk FOREIGN KEY (user_id) REFERENCES user (id)
);
CREATE INDEX category_user_id_fk ON category (user_id);
CREATE TABLE operation
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    amount BIGINT(20) NOT NULL,
    date DATE,
    description TEXT,
    id_cat INT(11) NOT NULL,
    id_user INT(11) NOT NULL,
    CONSTRAINT operation_category_id_fk FOREIGN KEY (id_cat) REFERENCES category (id),
    CONSTRAINT operation_user_id_fk FOREIGN KEY (id_user) REFERENCES user (id)
);
CREATE INDEX operation_category_id_fk ON operation (id_cat);
CREATE INDEX operation_user_id_fk ON operation (id_user);
