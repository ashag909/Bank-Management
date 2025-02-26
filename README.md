# Bank-Management
Banking Management System

Overview

The Banking Management System is a GUI-based application built using Python, Tkinter, and MySQL. This system allows users to create accounts, deposit and withdraw money, check balances, and view transaction history. It provides a simple yet efficient banking solution with database integration for secure and persistent storage of user information.

Features

Account Creation: Users can create a new bank account with a name, PIN, and initial deposit.

Deposit Money: Users can add money to their account.

Withdraw Money: Users can withdraw money, ensuring balance availability.

Balance Inquiry: Users can check their account balance.

Transaction History: Users can view their past transactions stored in CSV files.

Secure Login: Users must log in with their account number, name, and PIN.

Graphical User Interface (GUI): Built using Tkinter for an intuitive user experience.

Technologies Used

Programming Language: Python

GUI Framework: Tkinter

Database: MySQL

CSV Handling: Transaction records are stored in CSV files for easy access.

Installation

Prerequisites

Ensure you have the following installed on your system:

Python 3.x

MySQL Server

pip (Python package manager)

Setup Instructions

Clone the Repository

git clone https://github.com/ashag909/banking-management-system.git
cd banking-management-system

Install Required Dependencies

pip install mysql-connector-python

Setup MySQL Database

Open MySQL and create a database:

CREATE DATABASE banking_system;

Update database credentials in the script if necessary:

conn = mysql.connector.connect(host='localhost', user='root', password='your_password', database='banking_system')

Run the script to create the necessary tables automatically.

Run the Application

python GUI-BankSystem.py

Usage

Launch the program and navigate through the GUI.

Register a new bank account.

Log in using your account details.

Perform transactions like deposit, withdrawal, balance inquiry, and view transaction history.

Screenshots



Future Enhancements

Add email notifications for transactions.

Implement multi-user support.

Improve security measures with encrypted PIN storage.

Contributing

Feel free to contribute by submitting pull requests or reporting issues.

License

This project is open-source and available under the MIT License.

Developed by Asha Rani Gouda 🚀
