# Diet_App
Diet app to help us achieve our nutritional goals.

This project is composed on 3 main parts:
  1. Web_scraper_all_recipes.ipynb -> web scraper made in Python to collects data about meals and nutritions from https://www.allrecipes.com/.
     The file is collecting data all information about meals: nutritions and ingredients needed to prepare the dish. Later we will compose the diet plan 
     based on that information.
  2. Architecture of the data base made in PostgreSQL to manage all data (informations about users, diet plans, meals information etc.) used in Diet Application.
     DATABASE_project.jpeg shows visual representation of tables and connections beetwen them. 
  3. New_user_creation.py -> Python connector to a database which is collecting information about new user and insert them into Data Base. 
      
      
STACK USED IN THE PROJECT: postgreSQL, pgAdmin4, Python, Jupyter Lab, Psycopg2, Pandas, NumPy

Work in progress:
  4. Errors and Exceptions handling for Python connector
  5. Algorithms to plan weekly diet plan.
