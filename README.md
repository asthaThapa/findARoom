# Find a room

## About the application
"Find a room" is a light weight web application built on Flask that provides a platform for users to find and advertise rooms for rent. The application allows users to search for available rooms based on different criteria such as location, rent amount, and availability date. Users can also create a profile and advertise their own rooms for rent by providing details such as room description, rent amount, location, and availability date.

The application is designed with a simple and user-friendly interface that enables users to easily navigate and find the information they need. The application also has a messaging system that allows users to communicate with each other to arrange viewings or ask questions.

## Requirements 
* Install python 3.10.9 and import Flask
* Import SQLAlchemy
* Sqlite3

## Database Details
This application uses SQLite as its database management system. The database is located in the instance folder and is called find-a-room.db. 

If you want to create your own database, you can delete the old one and create the database schema. In order to do so, run the following command before you run the application from the root folder.

> *python dbconfig.py*

This config file creates the necessary databases for the application to use.

## How to run
After setting up the database. Run the following command from the root folder.

> *python main.py*

## UI template
The UI template has been taken in reference from [BootstrapMade](https://bootstrapmade.com/real-estate-agency-bootstrap-template/)

