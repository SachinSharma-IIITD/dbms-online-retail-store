SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP DATABASE IF EXISTS hawwkstore;
CREATE DATABASE hawwkstore;
USE hawwkstore;

CREATE TABLE admin_team (
    id TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (id)
);

CREATE TABLE employee (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    admin_id TINYINT UNSIGNED NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    gender ENUM('male', 'female') DEFAULT 'male',
    phone CHAR(10) NOT NULL,
    address VARCHAR(100) NOT NULL,
    INDEX (admin_id),
    INDEX (first_name, last_name),
    INDEX (gender),
    CONSTRAINT fk_empl_to_admin_team FOREIGN KEY (admin_id) REFERENCES admin_team(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE manages (
    table_name VARCHAR(100) NOT NULL,
    admin_id TINYINT UNSIGNED NOT NULL,
    PRIMARY KEY (table_name, admin_id),
    CONSTRAINT fk_manages_to_admin_team FOREIGN KEY (admin_id) REFERENCES admin_team(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE category (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    cat_id SMALLINT UNSIGNED NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    qty SMALLINT UNSIGNED,
    specs VARCHAR(300),
    INDEX (brand),
    INDEX (name),
    INDEX (cat_id),
    CONSTRAINT fk_product_to_cat_id FOREIGN KEY (cat_id) REFERENCES category(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE seller (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    office_no VARCHAR(100) NOT NULL,
    locality VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    phone CHAR(10),
    INDEX (name)
);

CREATE TABLE map_sellers (
    seller_id SMALLINT UNSIGNED NOT NULL,
    product_id SMALLINT UNSIGNED NOT NULL,
    qty SMALLINT UNSIGNED,
    PRIMARY KEY (seller_id, product_id),
    CONSTRAINT fk_map_seller_to_seller_id FOREIGN KEY (seller_id) REFERENCES seller(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_map_seller_to_product_id FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE customers (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    gender ENUM('male', 'female') DEFAULT 'male',
    house_no VARCHAR(100) NOT NULL,
    locality VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    INDEX (first_name, last_name),
    INDEX (gender),
    INDEX (state, city)
);

CREATE TABLE customer_phone (
    id SMALLINT UNSIGNED NOT NULL,
    phone CHAR(10) NOT NULL,
    PRIMARY KEY (id, phone),
    CONSTRAINT fk_customer_phone_to_customer FOREIGN KEY (id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE cart (
    customer_id SMALLINT UNSIGNED NOT NULL,
    product_id SMALLINT UNSIGNED NOT NULL,
    qty SMALLINT UNSIGNED,
    PRIMARY KEY (customer_id, product_id),
    CONSTRAINT fk_cart_to_customer_id FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_cart_to_product_id FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE orders (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    price DECIMAL(8,2) UNSIGNED NOT NULL,
    date_of_order date,
    date_of_delivery date,
    mode_of_payment ENUM('cash', 'upi', 'debit card', 'credit card', 'net banking') DEFAULT 'cash',
    INDEX (date_of_order),
    INDEX (date_of_delivery),
    INDEX (mode_of_payment)
);

CREATE TABLE active_orders (
    id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
    raw_price DECIMAL(7,2) UNSIGNED NOT NULL,
    status ENUM('ordered', 'ready', 'out for delivery') DEFAULT 'ordered',
    INDEX (status),
    CONSTRAINT fk_active_orders_to_orders FOREIGN KEY (id) REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE verify_orders (
    order_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
    pin SMALLINT UNSIGNED NOT NULL,
    CONSTRAINT fk_verify_orders_to_orders FOREIGN KEY (order_id) REFERENCES active_orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE map_active_orders (
    order_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
    customer_id SMALLINT UNSIGNED NOT NULL,
    INDEX (customer_id),
    CONSTRAINT fk_map_active_orders_to_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_map_active_orders_to_active_orders FOREIGN KEY (order_id) REFERENCES active_orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE map_prev_orders (
    customer_id SMALLINT UNSIGNED NOT NULL,
    order_id SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (customer_id, order_id),
    CONSTRAINT fk_map_prev_orders_to_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_map_prev_orders_to_orders FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE order_item (
    product_id SMALLINT UNSIGNED NOT NULL,
    order_id SMALLINT UNSIGNED NOT NULL,
    qty SMALLINT UNSIGNED NOT NULL,
    PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_order_item_to_product FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_order_item_to_orders FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE warehouse (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone CHAR(10) NOT NULL,
    plot_no VARCHAR(100) NOT NULL,
    locality VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    INDEX (name),
    INDEX (state, city)
);

CREATE TABLE delivery_man (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    warehouse_id SMALLINT UNSIGNED NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone CHAR(10) NOT NULL,
    status ENUM('busy', 'available') DEFAULT 'available',
    INDEX (warehouse_id),
    INDEX (first_name, last_name),
    INDEX (status),
    CONSTRAINT fk_del_man_to_orders FOREIGN KEY (warehouse_id) REFERENCES warehouse(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE offers (
    order_id SMALLINT UNSIGNED NOT NULL,
    discount SMALLINT UNSIGNED DEFAULT 0,
    PRIMARY KEY (order_id, discount),
    CONSTRAINT fk_offer_to_orders FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE map_delivery (
    order_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY,
    warehouse_id SMALLINT UNSIGNED NOT NULL,
    del_man_id SMALLINT UNSIGNED NOT NULL,
    INDEX (warehouse_id),
    INDEX (del_man_id),
    CONSTRAINT fk_map_delivery_to_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouse(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_map_delivery_to_orders FOREIGN KEY (order_id) REFERENCES active_orders(id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_map_delivery_to_del_man FOREIGN KEY (del_man_id) REFERENCES delivery_man(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE payment (
    order_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    customer_id SMALLINT UNSIGNED NOT NULL,
    date_of_payment date,
    INDEX (customer_id),
    INDEX (date_of_payment),
    CONSTRAINT fk_payment_to_prev_orders FOREIGN KEY (order_id) REFERENCES map_prev_orders(order_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_payment_to_customers FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE ON UPDATE CASCADE
);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;