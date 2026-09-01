import mysql.connector

#---CONNECT TO MYSQL & CREATE DATABASE---
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="database_password"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS nutrition_db;")
cursor.execute("USE nutrition_db")

#---CREATE USERS TABLE---
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    name VARCHAR(100) PRIMARY KEY,
    email VARCHAR(100),
    password VARCHAR(100)
)""")

#---CREATE FOOD_PLAN TABLE---
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_plan(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    breakfast VARCHAR(100),
    lunch VARCHAR(100),
    dinner VARCHAR(100),
    snacks VARCHAR(100),
    date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (name) REFERENCES users(name) ON DELETE CASCADE
)""")

#---CREATE NUTRITION_DATA TABLE---
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_nutrition_data(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    food_name VARCHAR(100),
    calories FLOAT,
    carbs FLOAT,
    fat FLOAT,
    protein FLOAT,
    sugar FLOAT,
    date_logged TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (name) REFERENCES users(name) ON DELETE CASCADE
)""")

conn.commit()
cursor.close()
conn.close()
print("Database & Tables Created Succesfully!")















