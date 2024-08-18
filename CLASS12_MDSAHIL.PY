import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sahil",
            database="razerboy"
        )
        if conn.is_connected():
            print("Connected to the database!")
            return conn
    except Error as e:
        messagebox.showinfo("Error", f"Error connecting to MySQL: {e}")
        return None

# Function to add a room
def add_room():
    room_number = entry_room_number.get()
    room_type = entry_room_type.get()
    price = entry_price.get()
    
    if room_number and room_type and price:
        try:
            cursor.execute("INSERT INTO rooms (room_number, room_type, price) VALUES (%s, %s, %s)", 
                           (room_number, room_type, price))
            conn.commit()
            messagebox.showinfo("Success", "Room added successfully!")
            clear_entries()
            view_rooms()
        except Error as e:
            messagebox.showinfo("Error", f"Failed to add room: {e}")
    else:
        messagebox.showinfo("Error", "All fields are required!")

# Function to view all rooms
def view_rooms():
    cursor.execute("SELECT room_id, room_number, room_type, availability, price FROM rooms")
    rows = cursor.fetchall()
    
    for row in tree.get_children():
        tree.delete(row)
    
    for row in rows:
        tree.insert("", "end", values=row)

# Function to clear entry fields
def clear_entries():
    entry_room_number.delete(0, tk.END)
    entry_room_type.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# Function to delete a selected room
def delete_room():
    try:
        selected_item = tree.selection()[0]
        room_id = tree.item(selected_item)['values'][0]
        
        cursor.execute("DELETE FROM rooms WHERE room_id = %s", (room_id,))
        conn.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Room deleted successfully!")
    except IndexError:
        messagebox.showinfo("Error", "No room selected for deletion.")
    except Error as e:
        messagebox.showinfo("Error", f"Failed to delete room: {e}")

# Main Window
conn = connect_to_database()
if conn:
    cursor = conn.cursor()
    
    window = tk.Tk()
    window.title("Hotel Management System")

    # Labels and Entry widgets for Room Details
    lbl_room_number = tk.Label(window, text="Room Number:")
    lbl_room_number.grid(row=0, column=0, padx=10, pady=10)

    entry_room_number = tk.Entry(window)
    entry_room_number.grid(row=0, column=1, padx=10, pady=10)

    lbl_room_type = tk.Label(window, text="Room Type:")
    lbl_room_type.grid(row=1, column=0, padx=10, pady=10)

    entry_room_type = tk.Entry(window)
    entry_room_type.grid(row=1, column=1, padx=10, pady=10)

    lbl_price = tk.Label(window, text="Price:")
    lbl_price.grid(row=2, column=0, padx=10, pady=10)

    entry_price = tk.Entry(window)
    entry_price.grid(row=2, column=1, padx=10, pady=10)

    # Buttons for Add, Delete, and View
    btn_add_room = tk.Button(window, text="Add Room", command=add_room)
    btn_add_room.grid(row=3, column=0, padx=10, pady=10)

    btn_view_rooms = tk.Button(window, text="View Rooms", command=view_rooms)
    btn_view_rooms.grid(row=3, column=1, padx=10, pady=10)

    btn_delete_room = tk.Button(window, text="Delete Room", command=delete_room)
    btn_delete_room.grid(row=4, column=0, padx=10, pady=10)

    btn_clear = tk.Button(window, text="Clear", command=clear_entries)
    btn_clear.grid(row=4, column=1, padx=10, pady=10)

    # Treeview for displaying rooms
    columns = ("Room ID", "Room Number", "Room Type", "Availability", "Price")
    tree = ttk.Treeview(window, columns=columns, show='headings')
    
    for col in columns:
        tree.heading(col, text=col)
        tree.grid(row=5, column=0, columnspan=2)

    view_rooms()

    window.mainloop()
    
    # Close the database connection
    cursor.close()
    conn.close()