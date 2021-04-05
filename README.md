##Prerequisites

Install MySql Server : sudo apt-get install mysql-server

CREATE DATABASE flaskapp;

USE flaskapp;

CREATE TABLE image_labels(image varchar(200), label varchar(100));


#Dependencies

Check Requirements.txt


To run the app:


python app.py "path to Image Directory"


The labels will be stored in the database created. 
