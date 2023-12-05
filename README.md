# MyBooks Library Management System

## Overview
MyBooks is a Python-based library management system designed to manage book records using a MySQL database. This application provides a user-friendly interface for adding, updating, deleting, and viewing book records.

## Features
Add Book: Insert new book details into the database.
View Records: Display all book records from the database.
Update Record: Modify existing book details.
Delete Record: Remove book records from the database.
Clear Screen: Reset the display area.
Exit Application: Close the application.

## Technical Specifications
  - The primary language is Python3.
  - MySQL database will be used for efficient data query. 
  - For the Graphical interface, the tkinter library and the tkinter.messagebox will be used to display message boxes to the user.
  - The mysql.connector and pymysql will be used to connect the Python application to the MySQL database for CRUD (Create, Read, Update, Delete) operations.
    -pip install mysql-connector-python
    -pip install pymysql

## Setting up the MySQL Database
To set up the database, import the two MySQL dump files in the github into your MySQL server:
1. booksdump.sql
2. books_schema3.sql.sql

Create a table named books with appropriate fields (e.g., id, title, author, isbn, ratings).

## Configuring the Application
Update the mysql_config.py file with your MySQL server details:
dbConfig = {
    'user': 'yourusername',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'mybooks'
}

## Running the Application
1. Clone this repository to your local machine
2. Connect to MySQL Database with instruction listed above
3. Navigate to the project directory and execute the booksApp.py script
python3 booksApp.py

## Usage
Upon launching, the application presents a GUI where you can interact with the database by adding, updating, viewing, and deleting book records.
