# Movie Search System

## Description

Console application for searching movies in the Sakila database.

## Technologies Used

The project uses the following technologies and libraries:

- Python 3.13
  - Main programming language used to implement the application logic.

- MySQL
  - Relational database management system used for storing movie data from the Sakila database.

- MongoDB
  - NoSQL document-oriented database used for storing search history and search statistics.

- PyMySQL
  - Python client library used to connect to MySQL and execute SQL queries.

- PyMongo
  - Official MongoDB driver for Python used to insert, retrieve and aggregate search history data.

- python-dotenv
  - Loads environment variables from the `.env` file, allowing sensitive configuration values to be stored outside the source code.

- dnspython
  - DNS toolkit used internally by MongoDB drivers and network-related operations. Provides DNS resolution support for MongoDB connections.


## Features

- Search movies by keyword
- Search movies by category
- Search movies by year range
- Search movies by category and year
- View last searches
- View top searches
- Error handling and logging

## Project Structure

project/

├── main.py  
Application entry point. Starts the interactive menu system.

├── ui.py  
User interface module. Contains menu navigation, movie search handlers, pagination logic, and search history display.

├── mysql_client.py  
MySQL database client. Handles connections, query execution, and movie search operations in the Sakila database.  

├── mongo_client.py
MongoDB client. Stores search history and provides statistics for recent and popular searches.  

├── sql_queries.py  
Collection of SQL queries used by the application. Separates SQL code from business logic.

├── errors.py  
Custom exceptions and input validation functions for categories, years, and search parameters.  

├── logger_sakila.py  
Logging and centralized error handling module. Provides a decorator for exception handling and logging.  

├── settings.py
Application configuration module. Loads environment variables and database settings.  

├── .env
Environment variables file containing database credentials and connection settings.  

└── README.md
Project documentation, installation instructions, and usage guide.




## Installation

Install dependencies:

```bash```
```pip install pymysql pymongo python-dotenv```

## Environment Variables
Create .env file:  
DB_HOST=your_host  
DB_USER=your_username  
DB_PASSWORD=your_password  

MONGO_URI=your_link  
MONGO_DATABASE=your_db  
MONGO_COLLECTION=your_collection  

## Run
```bash ```
```python main.py```

Author
V_NMad