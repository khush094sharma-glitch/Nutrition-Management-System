import tkinter as tk
from tkinter import ttk, messagebox
import csv
import random
import matplotlib.pyplot as plt
from datetime import datetime
import mysql.connector

# --- Database Connector ---
def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="database_password",
        database="nutrition_db"
    )

# --- App Setup ---
root = tk.Tk()
root.title("Nutri Tracker")
root.geometry("1100x700+0+0")
root.configure(bg="mint cream")
root.resizable(False, False)

# --- Global Variables ---
latest_food = None
latest_values = []

# --- Register/Login Frame ---
tk.Label(root, text="Name:").place(x=20, y=20)
entry_name = tk.Entry(root, width=30)
entry_name.place(x=80, y=20)

tk.Label(root, text="Email:").place(x=400, y=20)
entry_email = tk.Entry(root, width=30)
entry_email.place(x=460, y=20)

tk.Label(root, text="Password:").place(x=800, y=20)
entry_password = tk.Entry(root, width=30, show="*")
entry_password.place(x=880, y=20)

def register_user():
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    password = entry_password.get().strip()

    if not (name and email and password):
        messagebox.showwarning("Missing Info", "Fill all fields.")
        return

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showinfo("Info", "User already exists. Continue with existing account.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

tk.Button(root, text="LOGIN", command=register_user, bg="green", fg="white", font=("Arial", 12)).place(x=0, y=60, width=1100, height=30)

# --- Quote Display ---
def load_quote():
    try:
        with open("MOTIVATIONAL_QUOTES.csv", "r", encoding="utf-8") as file:
            quotes = [row[0] for row in csv.reader(file)]
            return random.choice(quotes)
    except:
        return "Stay Healthy, Stay Strong!"

tk.Label(root, text=load_quote(), wraplength=800, justify="center", bg="light cyan",
         font=("Georgia", 12, "italic"), fg="maroon", relief="groove").place(relx=0.5, y=100, anchor="n")

# --- Nutrition Data Frame ---
frame_nutrition = tk.LabelFrame(root, text="Nutrition Info",labelanchor="n", font=("Arial", 15),width=500, height=400)
frame_nutrition.place(x=45, y=160)

tk.Label(frame_nutrition, text="Your Name:").place(x=20, y=20)
entry_nutri_name = tk.Entry(frame_nutrition, width=40)
entry_nutri_name.place(x=150, y=20)

tk.Label(frame_nutrition, text="Food Name:").place(x=20, y=70)
entry_food = tk.Entry(frame_nutrition, width=40)
entry_food.place(x=150, y=70)

tk.Label(frame_nutrition, text="Quantity:").place(x=20, y=120)
combo_qty = ttk.Combobox(frame_nutrition, values=["50 g", "100 g", "150 g", "200 g"], width=37)
combo_qty.place(x=150, y=120)
combo_qty.set("100 g")

def get_food_info():
    try:
        with open("NUTRITION_DATA.csv", "r") as file:
            for row in csv.reader(file):
                if row[0].strip().lower() == entry_food.get().strip().lower():
                    return row[0], list(map(float, row[1:]))
    except:
        return None, None

def show_nutrition_chart():
    global latest_food, latest_values
    food, values = get_food_info()
    if food and values:
        latest_food = food
        latest_values = values
        plt.figure(figsize=(5, 4))
        plt.pie(values, labels=["Calories", "Carbs", "Fats", "Protein", "Sugar"],
                colors=["tomato", "gold", "blue", "orange", "yellow"],
                autopct="%1.1f%%")
        plt.title(f"{food.title()} Nutrition")
        plt.show()
    else:
        messagebox.showinfo("Not Found", "Food not found in dataset.")

def save_nutrition():
    if not latest_food or not latest_values:
        messagebox.showwarning("Search Required", "Please search for food first.")
        return
    name = entry_nutri_name.get().strip()
    if not name:
        messagebox.showwarning("Missing Info", "Enter your name.")
        return
    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO food_nutrition_data 
            (name, food_name, calories, carbs, fat, protein, sugar, date_logged)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, latest_food, *latest_values, datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "Nutrition data saved.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Save failed: {e}")

tk.Button(frame_nutrition, text="SEARCH",activebackground="yellow" ,command=show_nutrition_chart).place(x=150, y=250, width=200)
tk.Button(frame_nutrition, text="SAVE", command=save_nutrition, bg="green", fg="white").place(x=0, y=353, width=500)

# --- Food Plan Frame ---
frame_plan = tk.LabelFrame(root, text="Food Plan", font=("Arial", 15),labelanchor="n", width=450, height=400)
frame_plan.place(x=600, y=160)

tk.Label(root, text="Name:").place(x=650, y=220)
entry_plan_name = tk.Entry(root, width=30)
entry_plan_name.place(x=750, y=220)

tk.Label(root, text="Breakfast:").place(x=650, y=260)
entry_breakfast = tk.Entry(root, width=30)
entry_breakfast.place(x=750, y=260)

tk.Label(root, text="Lunch:").place(x=650, y=300)
entry_lunch = tk.Entry(root, width=30)
entry_lunch.place(x=750, y=300)

tk.Label(root, text="Dinner:").place(x=650, y=340)
entry_dinner = tk.Entry(root, width=30)
entry_dinner.place(x=750, y=340)

tk.Label(root, text="Snacks:").place(x=650, y=380)
entry_snacks = tk.Entry(root, width=30)
entry_snacks.place(x=750, y=380)

tk.Label(root,text="    👩‍⚕️    \n~DIETICIEN~\n7219422648", bg="light yellow",fg="brown").place(x=970,y=175)
tk.Button(root,text="DONE", font=("Arial",12),activebackground="yellow").place(x=800,y=450)

def save_plan():
    name = entry_plan_name.get().strip()
    breakfast = entry_breakfast.get().strip()
    lunch = entry_lunch.get().strip()
    dinner = entry_dinner.get().strip()
    snacks = entry_snacks.get().strip()

    if not all([name, breakfast, lunch, dinner, snacks]):
        messagebox.showwarning("Missing Info", "All fields are required.")
        return

    try:
        conn = connect_database()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO food_plan (name, breakfast, lunch, dinner, snacks, date_logged)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, breakfast, lunch, dinner, snacks, datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Saved", "Food plan saved.")
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Save failed: {e}")

tk.Button(frame_plan, text="SAVE PLAN", command=save_plan, bg="green", fg="white").place(x=0, y=353, width=450)

# --- Logout / Exit ---
def logout_user():
    name = entry_nutri_name.get().strip()
    if not name:
        messagebox.showwarning("Missing Info", "Enter name to logout.")
        return
    confirm = messagebox.askyesno("Confirm Logout", f"Delete all data for '{name}'?")
    if confirm:
        try:
            conn = connect_database()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE name = %s", (name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Logged Out", "All user data deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Logout failed: {e}")

tk.Button(root, text="LOGOUT", bg="red", fg="white", font=("Arial", 12),width=20 ,command=logout_user).place(x=130, y=620)
tk.Button(root, text="STAY", bg="green", fg="white",font=("Arial",12),width=20 , activebackground="yellow").place(x=450, y=620)
tk.Button(root, text="EXIT", bg="red", fg="white", font=("Arial", 12),width=20 , command=root.destroy).place(x=750, y=620)

root.mainloop()






