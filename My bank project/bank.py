import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql
import csv
from time import gmtime, strftime

# Database connection
conn = mysql.connect(host='localhost', user='root', password='Ilovemyfamily@143', database='banking_system')
cursor = conn.cursor()

# Create tables if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    pin VARCHAR(255),
    balance FLOAT
);
""")
conn.commit()

# Function to check if input is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Function to create a new account
def write(master, name, oc, pin):
    if is_number(name) or not is_number(oc) or not is_number(pin) or name == "":
        messagebox.showinfo("Error", "Invalid Credentials\nPlease try again.")
        master.destroy()
        return

    cursor.execute("INSERT INTO accounts (name, pin, balance) VALUES (%s, %s, %s)", (name, pin, float(oc)))
    conn.commit()
    accnt_no = cursor.lastrowid
    
    with open(f"{accnt_no}-rec.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Credit", "Debit", "Balance"])
        writer.writerow([strftime("[%Y-%m-%d] [%H:%M:%S]", gmtime()), oc, "", oc])

    messagebox.showinfo("Details", f"Your Account Number is: {accnt_no}")
    master.destroy()

# Function to credit an account
def crdt_write(master, amt, accnt):
    if not is_number(amt):
        messagebox.showinfo("Error", "Invalid Amount\nPlease try again.")
        master.destroy()
        return
    
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (accnt,))
    row = cursor.fetchone()
    if row:
        cb = row[0] + float(amt)
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (cb, accnt))
        conn.commit()
        
        with open(f"{accnt}-rec.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([strftime("[%Y-%m-%d] [%H:%M:%S]", gmtime()), amt, "", cb])

        messagebox.showinfo("Success", "Amount Credited Successfully!")
    master.destroy()

# Function to debit an account
def debit_write(master, amt, accnt):
    if not is_number(amt):
        messagebox.showinfo("Error", "Invalid Amount\nPlease try again.")
        master.destroy()
        return
    
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (accnt,))
    row = cursor.fetchone()
    if row and row[0] >= float(amt):
        cb = row[0] - float(amt)
        cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (cb, accnt))
        conn.commit()
        
        with open(f"{accnt}-rec.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([strftime("[%Y-%m-%d] [%H:%M:%S]", gmtime()), "", amt, cb])

        messagebox.showinfo("Success", "Amount Debited Successfully!")
    else:
        messagebox.showinfo("Error", "Insufficient Balance!")
    master.destroy()

# Function to check account balance
def disp_bal(accnt):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (accnt,))
    row = cursor.fetchone()
    if row:
        messagebox.showinfo("Balance", f"Your balance is: {row[0]}")

# Function to display transaction history
def disp_tr_hist(accnt):
    disp_wn = tk.Tk()
    disp_wn.geometry("900x600")
    disp_wn.title("Transaction History")
    
    try:
        with open(f"{accnt}-rec.csv", "r") as file:
            lines = file.readlines()
            for line in lines:
                tk.Message(disp_wn, text=line, width=800).pack()
    except FileNotFoundError:
        messagebox.showinfo("Error", "No transaction history found!")
    
    tk.Button(disp_wn, text="Close", command=disp_wn.destroy).pack()
    disp_wn.mainloop()

# Function to show logged-in menu
def logged_in_menu(accnt, name):
    menu = tk.Tk()
    menu.geometry("400x400")
    menu.title("Account Menu")
    
    tk.Label(menu, text=f"Welcome {name}", font=("Arial", 14)).pack()
    tk.Button(menu, text="Deposit Money", command=lambda: crdt_write(menu, 100, accnt)).pack()
    tk.Button(menu, text="Withdraw Money", command=lambda: debit_write(menu, 50, accnt)).pack()
    tk.Button(menu, text="Check Balance", command=lambda: disp_bal(accnt)).pack()
    tk.Button(menu, text="Transaction History", command=lambda: disp_tr_hist(accnt)).pack()
    tk.Button(menu, text="Logout", command=menu.destroy).pack()
    
    menu.mainloop()

# Function to check login credentials
def check_log_in(master, name, acc_num, pin):
    cursor.execute("SELECT * FROM accounts WHERE account_number = %s AND name = %s AND pin = %s", (acc_num, name, pin))
    if cursor.fetchone():
        master.destroy()
        logged_in_menu(acc_num, name)
    else:
        messagebox.showinfo("Error", "Invalid Credentials!\nTry Again.")
        master.destroy()
        Main_Menu()

# Function to open account creation form
def create_account_form():
    register_window = tk.Tk()
    register_window.geometry("400x300")
    register_window.title("Create Account")

    tk.Label(register_window, text="Enter Name:").pack()
    name_entry = tk.Entry(register_window)
    name_entry.pack()

    tk.Label(register_window, text="Enter Opening Balance:").pack()
    balance_entry = tk.Entry(register_window)
    balance_entry.pack()

    tk.Label(register_window, text="Enter 4-digit PIN:").pack()
    pin_entry = tk.Entry(register_window, show="*")
    pin_entry.pack()

    tk.Button(register_window, text="Create Account", 
              command=lambda: write(register_window, name_entry.get(), balance_entry.get(), pin_entry.get())).pack()

    register_window.mainloop()

# Function to open login form
def login_form():
    login_window = tk.Tk()
    login_window.geometry("400x250")
    login_window.title("Login")

    tk.Label(login_window, text="Enter Account Number:").pack()
    acc_entry = tk.Entry(login_window)
    acc_entry.pack()

    tk.Label(login_window, text="Enter Name:").pack()
    name_entry = tk.Entry(login_window)
    name_entry.pack()

    tk.Label(login_window, text="Enter PIN:").pack()
    pin_entry = tk.Entry(login_window, show="*")
    pin_entry.pack()

    tk.Button(login_window, text="Login", 
              command=lambda: check_log_in(login_window, name_entry.get(), acc_entry.get(), pin_entry.get())).pack()

    login_window.mainloop()

# Main Menu of the banking system
def Main_Menu():
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Banking System")

    tk.Label(root, text="Welcome to the Banking System", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Create New Account", command=create_account_form).pack(pady=10)
    tk.Button(root, text="Login", command=login_form).pack(pady=10)

    root.mainloop()

# Start the program
Main_Menu()
