import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('faults.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS faults (
                            id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            last_name TEXT,
                            gender TEXT,
                            contact_number TEXT,
                            date_of_reporting TEXT,
                            unit_number TEXT,
                            apartment_name TEXT,
                            fault TEXT
                            )''')
        self.conn.commit()

    def insert_fault(self, first_name, last_name, gender, contact_number, unit_number, apartment_name, fault):
        try:
            date_of_reporting = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('''INSERT INTO faults (first_name, last_name, gender, contact_number, date_of_reporting, unit_number, apartment_name, fault) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (first_name, last_name, gender, contact_number, date_of_reporting, unit_number, apartment_name, fault))
            self.conn.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False

    def list_faults(self):
        self.cursor.execute("SELECT * FROM faults")
        return self.cursor.fetchall()

    def __del__(self):
        self.conn.close()

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Fault Logging System")

        self.db = Database()

        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_number_var = tk.StringVar()
        self.unit_number_var = tk.StringVar()
        self.apartment_name_var = tk.StringVar()
        self.fault_var = tk.StringVar()

        tk.Label(root, text="First Name:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.first_name_var).grid(row=0, column=1)
        tk.Label(root, text="Last Name:").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.last_name_var).grid(row=1, column=1)
        tk.Label(root, text="Gender:").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.gender_var).grid(row=2, column=1)
        tk.Label(root, text="Contact Number:").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.contact_number_var).grid(row=3, column=1)
        tk.Label(root, text="Unit Number:").grid(row=4, column=0)
        tk.Entry(root, textvariable=self.unit_number_var).grid(row=4, column=1)
        tk.Label(root, text="Apartment Name:").grid(row=5, column=0)
        tk.Entry(root, textvariable=self.apartment_name_var).grid(row=5, column=1)
        tk.Label(root, text="Fault:").grid(row=6, column=0)
        tk.Entry(root, textvariable=self.fault_var).grid(row=6, column=1)

        tk.Button(root, text="Submit", command=self.submit_fault).grid(row=7, column=1)
        tk.Button(root, text="List Faults", command=self.list_faults).grid(row=8, column=1)

    def submit_fault(self):
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        gender = self.gender_var.get()
        contact_number = self.contact_number_var.get()
        unit_number = self.unit_number_var.get()
        apartment_name = self.apartment_name_var.get()
        fault = self.fault_var.get()

        if not first_name or not last_name or not gender or not contact_number or not unit_number or not apartment_name or not fault:
            messagebox.showerror("Error", "All fields are required.")
            return

        if len(contact_number) != 10 or not contact_number.isdigit():
            messagebox.showerror("Error", "Invalid contact number.")
            return

        if not unit_number.isdigit():
            messagebox.showerror("Error", "Unit number must be a number.")
            return

        if self.db.insert_fault(first_name, last_name, gender, contact_number, unit_number, apartment_name, fault):
            messagebox.showinfo("Success", "Fault logged successfully.")

    def list_faults(self):
        faults = self.db.list_faults()
        if not faults:
            messagebox.showinfo("Info", "No faults logged yet.")
        else:
            fault_list_window = tk.Toplevel(self.root)
            tk.Label(fault_list_window, text="Faults Logged").pack()
            for fault in faults:
                tk.Label(fault_list_window, text=fault).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
