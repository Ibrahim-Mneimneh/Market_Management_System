-- Create Schema
create schema MMS;

-- Create the Employee table
CREATE TABLE Employee (
EmpId INT PRIMARY KEY auto_increment,
Firstname VARCHAR(30) NOT NULL,
Lastname VARCHAR(30) NOT NULL,
Salary DECIMAL(10,2) NOT NULL,
PhoneNumber VARCHAR(20) NOT NULL,
managerId INT,
FOREIGN KEY (Managerid) REFERENCES Employee(Empid)
);
ALTER TABLE Employee AUTO_INCREMENT=20230000;

-- Create the Promocode table
create table Promocode (
Promocode varchar(20) primary key unique,
Discount integer not null,
constraint check (Discount < 50 and Discount > 0)
);

-- Create the Order table
CREATE TABLE Orders (
OrderId INT PRIMARY KEY NOT NULL auto_increment,
Date DATE NOT NULL,
Price DECIMAL(10,2),
isOnline BOOLEAN,
PaymentMethod VARCHAR(20),
EmpId INT NOT NULL,
PromoCode varchar(20) unique,
FOREIGN KEY (EmpId) REFERENCES Employee(EmpId),
FOREIGN KEY (PromoCode) REFERENCES Promocode(Promocode),
constraint check (Price > 0)
);

-- Create the Item table
CREATE TABLE Item (
Barcode INT PRIMARY KEY,
Name VARCHAR(50) NOT NULL,
Price DECIMAL(10,2) NOT NULL,
leftAmount int Not NULL,
constraint check (leftAmount >= 0),
constraint check (Price > 0)
);

-- Relation between Item and order
create Table Item_Order(
OrderId INT,
Barcode INT,
Quantity INT not null,
primary key(OrderId,Barcode),
foreign key(OrderId) references Orders(OrderId),
foreign key(Barcode) references Item(Barcode),
constraint check (Quantity > 0)
);

-- Create the Supplier table
CREATE TABLE Supplier (
  SupplierId INT PRIMARY KEY not null,
  Name VARCHAR(30) NOT NULL,
  phoneNumber varchar(20) NOT NULL
);

create table Item_Supplier(
	barcode INT NOT NULL,
    supplierId INT NOT NULL,
    price decimal(10,2) NOT NULL,
    supplyAmount INT NOT NULL,
    date DATE not null,
    FOREIGN KEY (barcode) REFERENCES Item(barcode),
    FOREIGN KEY (supplierId) REFERENCES Supplier(supplierId),
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
    FOREIGN KEY (empId) REFERENCES Employee(Empid)
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

insert into Employee (Firstname, Lastname, Salary, PhoneNumber) values ("Hadi", "Al Mubasher", 1000.0, "03454123");
select EmpId from Employee where PhoneNumber = "76707309";
INSERT INTO Account VALUES ("hadim", "sueuksegishag748493", "h@gmail.com", True, (select EmpId from Employee where PhoneNumber = "03454123"));
select * from Employee;
select * from Account;