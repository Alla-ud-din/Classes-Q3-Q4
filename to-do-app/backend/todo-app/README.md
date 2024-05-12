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

