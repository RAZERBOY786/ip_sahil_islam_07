import tkinter as tk
import tkinter.messagebox
from tkinter.constants import SUNKEN
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Function to connect to the MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sahil",
            database="razerboy"
        )
        if conn.is_connected():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Connected to the database at {current_time}!")
            return conn
    except mysql.connector.Error as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tkinter.messagebox.showinfo("Error", f"Error connecting to MySQL at {error_time}: {e}")
        return None

# Functions for calculator operations
def myclick(number):
    entry.insert(tk.END, number)

def equal():
    try:
        expression = entry.get()
        result = str(eval(expression))
        entry.delete(0, tk.END)
        entry.insert(0, result)
        
        # Insert calculation into MySQL database
        cursor.execute("INSERT INTO calculations (expression, result) VALUES (%s, %s)", (expression, result))
        conn.commit()

    except Exception as e:
        tkinter.messagebox.showinfo("Error", f"Syntax Error: {e}")

def clear():
    entry.delete(0, tk.END)

# Establish a MySQL connection
conn = connect_to_database()
if conn:
    cursor = conn.cursor()

    # Create the main window
    window = tk.Tk()
    window.title('Calculator-GeeksForGeeks')
    frame = tk.Frame(master=window, bg="#856ff8", padx=20)
    frame.pack()
    entry = tk.Entry(master=frame, relief=SUNKEN, borderwidth=3, width=30)
    entry.grid(row=0, column=0, columnspan=30, ipady=20, pady=20)

    # Define buttons
    button_add = tk.Button(master=frame, text="Add", padx=15, pady=5, width=3, command=lambda: myclick('+'))
    button_add.grid(row=5, column=0, pady=2)
    button_subtract = tk.Button(master=frame, text="Sub", padx=15, pady=5, width=3, command=lambda: myclick('-'))
    button_subtract.grid(row=5, column=1, pady=2)
    button_multiply = tk.Button(master=frame, text="Multi", padx=15, pady=5, width=3, command=lambda: myclick('*'))
    button_multiply.grid(row=5, column=2, pady=2)
    button_div = tk.Button(master=frame, text="Div", padx=15, pady=5, width=3, command=lambda: myclick('/'))
    button_div.grid(row=6, column=0, pady=2)
    button_clear = tk.Button(master=frame, text="Clear", padx=15, pady=5, width=12, command=clear)
    button_clear.grid(row=6, column=1, columnspan=2, pady=2)
    button_equal = tk.Button(master=frame, text="=", padx=15, pady=5, width=20, command=equal)
    button_equal.grid(row=7, column=0, columnspan=3, pady=2)
    button_1 = tk.Button(master=frame, text='1', padx=15, pady=5, width=3, command=lambda: myclick(1))
    button_1.grid(row=1, column=0, pady=2)
    button_2 = tk.Button(master=frame, text='2', padx=15, pady=5, width=3, command=lambda: myclick(2))
    button_2.grid(row=1, column=1, pady=2)
    button_3 = tk.Button(master=frame, text='3', padx=15, pady=5, width=3, command=lambda: myclick(3))
    button_3.grid(row=1, column=2, pady=2)
    button_4 = tk.Button(master=frame, text='4', padx=15, pady=5, width=3, command=lambda: myclick(4))
    button_4.grid(row=2, column=0, pady=2)
    button_5 = tk.Button(master=frame, text='5', padx=15, pady=5, width=3, command=lambda: myclick(5))
    button_5.grid(row=2, column=1, pady=2)
    button_6 = tk.Button(master=frame, text='6', padx=15, pady=5, width=3, command=lambda: myclick(6))
    button_6.grid(row=2, column=2, pady=2)
    button_7 = tk.Button(master=frame, text='7', padx=15, pady=5, width=3, command=lambda: myclick(7))
    button_7.grid(row=3, column=0, pady=2)
    button_8 = tk.Button(master=frame, text='8', padx=15, pady=5, width=3, command=lambda: myclick(8))
    button_8.grid(row=3, column=1, pady=2)
    button_9 = tk.Button(master=frame, text='9', padx=15, pady=5, width=3, command=lambda: myclick(9))
    button_9.grid(row=3, column=2, pady=2)
    button_0 = tk.Button(master=frame, text='0', padx=15, pady=5, width=3, command=lambda: myclick(0))
    button_0.grid(row=4, column=0, pady=2)
    button_00 = tk.Button(master=frame, text='00', padx=15, pady=5, width=3, command=lambda: myclick('00'))
    button_00.grid(row=4, column=1, pady=2)
    button_o = tk.Button(master=frame, text='.', padx=15, pady=5, width=3, command=lambda: myclick('.'))
    button_o.grid(row=4, column=2, pady=2)

    window.mainloop()

    # Close the MySQL connection when done
    cursor.close()
    conn.close()
    print("Connection closed.")
