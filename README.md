# Movie Search System

## Description

Console application for searching movies in the Sakila database.

The project uses:

- MySQL for movie data storage
- MongoDB for storing search history
- Python
- PyMySQL
- PyMongo

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

├── ui.py

├── mysql_client.py

├── mongo_client.py

├── sql_queries.py

├── errors.py

├── logger_sakila.py

├── settings.py

├── .env

└── README.md

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