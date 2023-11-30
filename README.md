# MyBooks Library Management System

##Overview
MyBooks is a Python-based library management system designed to manage book records using a MySQL database. This application provides a user-friendly interface for adding, updating, deleting, and viewing book records.

##Features
Add Book: Insert new book details into the database.
View Records: Display all book records from the database.
Update Record: Modify existing book details.
Delete Record: Remove book records from the database.
Clear Screen: Reset the display area.
Exit Application: Close the application.

##Installation and Setup
Prerequisites
Python 3.11
MySQL Server

##Setting up the MySQL Database
Install MySQL Server and set up a database named mybooks.
Create a table named books with appropriate fields (e.g., id, title, author, isbn, ratings).

##Configuring the Application
Update the mysql_config.py file with your MySQL server details:
python
dbConfig = {
    'user': 'yourusername',
    'password': 'yourpassword',
    'host': 'localhost',
    'database': 'mybooks'
}


##Running the Application
To run the application, execute the mybooks.py script:
bash
python mybooks.py

##Usage
Upon launching, the application presents a GUI where you can interact with the database by adding, updating, viewing, and deleting book records.
