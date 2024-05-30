# from fastapi import FastAPI, Depends, HTTPException
## FastAPI
This is the main framework used to build the API.  
## Depends, HTTPException
These are used for dependency injection and handling errors in the API.  
Dependency injection (DI) is a programming technique for providing an object with the dependencies it needs to function, rather than having the object create them itself.  
[Dependency Injection (DI) Design pattern](https://www.geeksforgeeks.org/dependency-injectiondi-design-pattern/).  

# from sqlmodel import SQLModel, Field, create_engine, Session, select  
## SQLModel  
* Creater of SQLModel and FastAPI is same. So functionality of both is highly compatible.
* SQLModel is a Python library built on top of SQLAlchemy that simplifies interacting with relational databases. It offers a more Pythonic and streamlined approach compared to using SQLAlchemy directly.  
* It is an ORM based on SQLAlchemy.
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

psycopg (PostgreSQL Driver) is a python provide driver to translate python code into PostgreSQL (SQL) language 

SQLAlchemy is a powerful ORM,  It acts as a bridge between your object-oriented Python code and the underlying database.  
SQLAlchemy is designed to work with various relational databases like PostgreSQL, MySQL, SQLite, and more. You can use the same core functionalities with different database systems by using the appropriate driver.  
psycopg is a popular Python library that acts as a driver for connecting to PostgreSQL databases.  
It allows SQLAlchemy to communicate effectively with PostgreSQL by translating Python objects and queries into appropriate PostgreSQL commands.  

# engine = create_engine(connection_string, connect_args={'sslmode':'require'}, pool_recycle=300, pool_size=10, echo=True)

* connect_args={'sslmode':'require'}   

SSL (Secure Sockets Layer) encrypts communication between your application and the database server  

* pool_recycle=300  

It specifies the time (in seconds) after which unused connections within the pool are recycled.  

* pool_size=10  

It specifies the initial number of connections that will be established in the connection pool. By default pool size in SQLAlchemy is 5.  

* echo=True  

Setting echo=True as an argument to create_engine enables detailed logging of database interactions. This means SQLAlchemy will print information to your console

# SQLModel.metadata.create_all(engine)  

* SQLModel.metadata:  

This line references an attribute called metadata that belongs to the SQLModel class in the SQLModel library.
metadata is an instance of the MetaData class from SQLAlchemy, which acts as a registry for all the database tables defined using SQLModel in your application.  

* What Does metadata Do?

As you define models (classes) in your application that inherit from SQLModel, these models represent your database tables.
When you create a model instance, SQLModel automatically registers it with the metadata object. This registration process essentially tracks the structure and relationships between your models (tables).  

* create_all(engine):  
The .create_all(engine) method is called on the metadata object. This method, provided by SQLAlchemy, iterates through all the registered models (tables) within the metadata and attempts to create them in the database specified by the engine argument.  


* def get_session():  
*    with Session(engine) as session:   
*        yield session   

## with Session(engine) as session::

* This line utilizes a context manager to create a session object and manage its lifecycle.
    * Session(engine): This part creates a new session object using SQLModel's Session class. This engine manages the connection pool and interacts with the database server.  
    * as session: This assigns the created session object to the variable named session within the indented block. The session object will be used to interact with the database.  

## yield session:

* The yield keyword within the context manager pauses the execution of the function at this point.
* When you call get_session() in your application code, the function creates a session using Session(engine), assigns it to session, and then pauses its execution using yield session.
* This essentially "yields" control back to the calling code, providing access to the created session within the context of the with block.  



# To generate random key (SECRET_KEY)  
python -c "import secrets; print(secrets.token_hex(32))"
