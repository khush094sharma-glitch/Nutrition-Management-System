import mysql.connector

#CONNECT TO MYSQL & CREATE DATABASE
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my!dogs$eats9bones"
)
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Nutrition_Database;")
cursor.execute("USE Nutrition_Database")

#CREATE TABLE FOR USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
)""")

#CREATE TABLE FOR CHALLENGES
cursor.execute("""
CREATE TABLE IF NOT EXISTS challenges(
    challenge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    challenge_name VARCHAR(255),
    status ENUM('pending','done'),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)   
)""")

# CREATE TABLE FOR REWARDS
cursor.execute("""
CREATE TABLE IF NOT EXISTS rewards(
    reward_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    reward_name VARCHAR(255),
    status ENUM('pending','claimed'),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)""")

# CREATE TABLE FOR FOOD LOG
cursor.execute("""
CREATE TABLE IF NOT EXISTS food_log(
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_name VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)  
)""")

#CREATE TABLE FOR NUTRITION DATA
cursor.execute("""
CREATE TABLE IF NOT EXISTS nutrition_data(
    nutrition_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    food_name VARCHAR(255),
    calories FLOAT,
    protein FLOAT,
    carbohydrate FLOAT,
    fats FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)""")

conn.commit()
cursor.close()
conn.close()
print("Database & Tables Created Succesfully!")















