-- Create Schema
create schema MMS;
USE MMS;

-- Create the Employee table
CREATE TABLE Employee (
EmpId INT PRIMARY KEY auto_increment,
Firstname VARCHAR(30) NOT NULL,
Lastname VARCHAR(30) NOT NULL,
Salary DECIMAL(10,2) NOT NULL,
PhoneNumber VARCHAR(20) NOT NULL,
managerId INT DEFAULT 20230000,
FOREIGN KEY (Managerid) REFERENCES Employee(Empid) on delete set null
);
ALTER TABLE Employee AUTO_INCREMENT=20230000;

-- Create the Promocode table
create table Promocode (
Promocode varchar(20) primary key,
Discount integer not null,
constraint check (Discount < 50 and Discount > 0)
);

-- Create the Order table
CREATE TABLE Orders (
  OrderId INT PRIMARY KEY NOT NULL auto_increment,
  Date DATE NOT NULL,
  Price DECIMAL(10,2),
  isOnline BOOLEAN,
  EmpId INT,
  PromoCode varchar(20) unique,
  FOREIGN KEY (EmpId) REFERENCES Employee(EmpId) on delete set null,
  FOREIGN KEY (PromoCode) REFERENCES PromoCode(PromoCode) on delete set null,
  constraint check (Price > 0)
);
-- Create the Item table
CREATE TABLE Item (
Barcode bigint PRIMARY KEY,
Name VARCHAR(50) NOT NULL,
Price DECIMAL(10,2) NOT NULL,
leftAmount int Not NULL,
constraint check (leftAmount >= 0),
constraint check (Price > 0)
);

-- Relation between Item and order
create Table Item_Order(
OrderId INT,
barcode bigint,
quantity INT not null,
primary key(orderId,barcode),
foreign key(orderId) references orders(orderId),
foreign key(barcode) references Item(barcode),
constraint check (quantity > 0)
);

-- Create the Supplier table
CREATE TABLE Supplier (
  SupplierId INT PRIMARY KEY not null auto_increment,
  Name VARCHAR(255) NOT NULL,
  phoneNumber varchar(20) NOT NULL unique
);
ALTER TABLE Supplier AUTO_INCREMENT=100;

create table Item_Supplier(
    barcode bigint NOT NULL,
    supplierId INT NOT NULL,
    price decimal(10,2) NOT NULL,
    supplyAmount INT NOT NULL,
    date DATE not null,
    FOREIGN KEY (barcode) REFERENCES Item(barcode),
    FOREIGN KEY (supplierId) REFERENCES Supplier(supplierId) on delete cascade,
    primary key(barcode,supplierId, date),
    constraint check (price > 0),
    constraint check (supplyAmount > 0)
);

create table Account (
    username varchar(30) primary key unique,
    password varchar(64),
    email varchar(255),
    isMan boolean,
    empId INT not null unique,
    FOREIGN KEY (empId) REFERENCES Employee(Empid) on delete cascade
);


CREATE TABLE Customer (
  CustomerId INT NOT NULL AUTO_INCREMENT,
  Firstname VARCHAR(20) not null,
  Lastname VARCHAR(20) not null,
  PhoneNumber VARCHAR(20) not null,
  Address VARCHAR(100) not null,
  orderid int unique not null,
  foreign key (orderid) references Orders(Orderid) on delete cascade,
  PRIMARY KEY (CustomerId, orderid)
);

insert into Employee (Firstname, Lastname, Salary, PhoneNumber, managerId) values ("Hadi", "Al Mubasher", 1000.0, "03454123",null);
INSERT INTO Account VALUES ("hadim", "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "h.mubasher@bau.edu.lb", True, (select EmpId from Employee where PhoneNumber = "03454123"));

select * from Employee;
select * from Account;


insert into Supplier (Name, phoneNumber) values ("SHARAFELDINE FOR GENERAL TRADE","03316762");
insert into Supplier (Name, phoneNumber) values ("HAJJAR FOODS SAL","08500053");
insert into Supplier (Name, phoneNumber) values ("Modern Markets Distribution Sal","03028377");
insert into Supplier (Name, phoneNumber) values ("Akiki Brothers","76444327");

insert into Item values (745178984232, "Halawa with Chocolate 800g",2.5,30);
insert into Item values (745240328773, "Date Jam 400g",1,30);
insert into Item values (745240328766, "Pear Jam 400g",0.99,10);
insert into Item values (745240328797, "Strawberry Jam 400g",0.99,0);
insert into Item values (744998767385, "Labneh 500g", 3.5, 20);
insert into Item values (744839211470, "Kishk 400g", 4.99, 15);
insert into Item values (744516786642, "Zaatar Mix 200g", 2.49, 25);
insert into Item values (745014729392, "Dried Figs 250g", 4.99, 20);
insert into Item values (745283940274, "Pickled Turnips 1kg", 6.99, 10);
insert into Item values (745361907753, "Lebanese Coffee 200g", 7.99, 5);
insert into Item values (745523316972, "Halawa with Pistachios 500g", 5.5, 15);
insert into Item values (744706142144, "Sumac 100g", 1.99, 30);
insert into Item values (744968916720, "Pomegranate Molasses 500ml", 3.99, 20);
insert into Item values (745078101509, "Kibbeh Mix 1kg", 10.99, 5);

insert into Item_Supplier (barcode, supplierId, price, supplyAmount, date) values (745178984232,101,2,30,'2023-04-22');

select * from Item;
select * from Item_Supplier;
select * from Supplier;
select * from Account;
