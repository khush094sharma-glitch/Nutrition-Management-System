import tkinter as tk
from tkinter import messagebox
import datetime
import mysql.connector
import matplotlib.pylot as plt 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="my!dogs$eats9bones",
    database="Nutrition_Database"
)
cursor = conn.cursor()

LOGGED_IN_USER = None

# VALIDATE IF USER EXISTS
def validate_user(user_id):
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone() is not None

# AUTO RETURN PREVIOUS USER DATA
def load_user_data(user_id):
    """FETCH USER DATA AUTOMATICALLY"""
    if not validate_user(user_id):
        messagebox.showerror("Error","User does not exist!")
        return
    
    cursor.execute("SELECT food_name, calories, protein, carbohydrates, fats FROM nutrition_data WHERE user_id =%s", (user_id,))
    history = cursor.fetchall()
    history_text = "Your Nutrition Data:\n"
    for food in history:
        history_text += f"{food[0]}g - Calories:{food[1]}, Protein:{food[2]}g, Carbohydrates:{food[3]}g, Fats:{food[4]}g"
    food_history_label.config(text=history_text)
    
# USER REGISTRATION
def register():
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%S,%S,%S)",(entry_name.get(), entry_email.get(), entry_password.get()))
    conn.commit()
    messagebox.showinfo("Success:","User Registered Successfully!")

# login user
def login():
    global LOGGED_IN_USER
    cursor.execute("SELECT user_id FROM users WHERE email=%s AND password=%s", (entry_email.get(), entry_password.get()))
    user = cursor.fetchone()
    if user:
        LOGGED_IN_USER = user[0]
        messagebox.showinfo("logged in successfully!")
        load_user_data(LOGGED_IN_USER)
    else:
        messagebox.showerror("Error:Invalid Email or Password")

#LOGOUT
def logout():
    global LOGGED_IN_USER
    LOGGED_IN_USER = None
    messagebox.showinfo("Logout:","Logged out Successfully!")


def get_nutrition():
    food_items= food_entry.get().split(",")
    foods =[]
    calories = []
    for food in food_items:
        cursor.execute("SELECT calories FROM nutrition_data WHERE food_name=%s",(food.strip(),))
        result = cursor.fetchone()
        if result:
            foods.append(food.strip())
            calories.append(result[0])
        else:
            messagebox.showerror("Error",f"No data found for {food.strip()}!")
    if foods:
        plt.bar(foods,calories, color="green")
        plt.xlabel("Foods")
        plt.ylabel("Calories")
        plt.title("Nutrition Progress")
        plt.show()

# GUI SETUP
root = tk.Tk()
root.geometry("1000x800")
root.title("Nutrition Tracker")
root.configure(bg="light green")

food_history_label =tk.Label(root,text="f_h_l", bg="light green").pack()
entry_name = tk.Entry(root).pack()
entry_email = tk.Entry(root).pack()
entry_password = tk.Entry(root, show="*").pack()
food_entry = tk.Entry(root).pack()

tk.Button(root, text="Login", command=register, width=20, bg="orange").pack(pady=5)
tk.Button(root, text="challenges", command=login, width=20, bg="orange").pack(pady=5)
tk.Button(root,text="Nutrition", command=get_nutrition, width=20, color="orange").pack(pady=5)
tk.Button(root, text="logout", command=logout, width=20, color="orange").pack(pady=5)

root.mainloop()        













    