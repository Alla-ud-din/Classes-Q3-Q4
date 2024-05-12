# from fastapi import FastAPI, Depends, HTTPException
## FastAPI
This is the main framework used to build the API.  
## Depends, HTTPException
These are used for dependency injection and handling errors in the API.  
Dependency injection (DI) is a programming technique for providing an object with the dependencies it needs to function, rather than having the object create them itself.  
[Dependency Injection (DI) Design pattern](https://www.geeksforgeeks.org/dependency-injectiondi-design-pattern/).  

# from sqlmodel import SQLModel, Field, create_engine, Session, select  
## SQLModel  
* This python library helps define models representing database tables.  
* SQLModel acts as a bridge between your Python application and a relational database like PostgreSQL or MySQL.  
* You create classes in Python that inherit from SQLModel to define your data models. These classes represent the structure of your tables.  
* SQLModel provides functions for performing common database operations through your Python models:
    * Creating new database objects (inserting data)
    * Updating existing objects
    * Deleting objects
    * Fetching data from the database  
## create_engine, Session, select  
These functions are used to create a database engine, manage database sessions, and write SQL queries.  
# from typing import Annotated
## Annotated   
This is used for type hints with dependencies.  
# from contextlib import asynccontextmanager  
## asynccontextmanager  
This helps create asynchronous context managers.

# PostgreSQL
PostgreSQL is a powerful, open source object-relational database system that uses and extends the SQL language combined with many features that safely store and scale the most complicated data workloads.  
## Open Source:   
source code is publicly accessible, allowing anyone to inspect, modify, and contribute to its development.  
## object-relational database:   
PostgreSQL bridges the gap between object-oriented programming languages like Python and relational databases.  

Replacing "postgresql" with "postgresql+psycopg" achieves two things:  
* It clarifies that you're connecting to a PostgreSQL database.  
* It explicitly specifies psycopg as the driver to be used for connection and communication.    

## Psycopg (PostgreSQL Driver):
psycopg is a popular Python library that acts as a driver for connecting to PostgreSQL databases.  
It allows SQLAlchemy to communicate effectively with PostgreSQL by translating Python objects and queries into appropriate PostgreSQL commands.  
SQLAlchemy is designed to work with various relational databases like PostgreSQL, MySQL, SQLite, and more. You can use the same core functionalities with different database systems by using the appropriate driver. 


