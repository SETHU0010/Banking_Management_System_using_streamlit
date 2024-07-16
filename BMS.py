import streamlit as st
import mysql.connector
from mysql.connector import Error

# Database connection
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="bms"
        )
        st.success("Successfully connected to the database")
    except Error as e:
        st.error(f"The error '{e}' occurred")
    return connection

# Get all users
def get_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Add a transaction
def add_transaction(connection, user_id, type, amount):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO transactions (user_id, type, amount) VALUES (%s, %s, %s)", (user_id, type, amount))
    connection.commit()

# Update user balance
def update_balance(connection, user_id, amount, is_deposit=True):
    cursor = connection.cursor()
    if is_deposit:
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
    else:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
    connection.commit()

# Streamlit interface
def main():
    st.title("Banking Management System")
    
    # Connect to database
    connection = create_connection()

    menu = ["Create User", "View Users", "Deposit", "Withdraw"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create User":
        st.subheader("Create New User")
        name = st.text_input("Name")
        email = st.text_input("Email")
        balance = st.number_input("Initial Balance", min_value=0.0)
        if st.button("Create"):
            create_user(connection, name, email, balance)
            st.success(f"User {name} created successfully with balance {balance}")

    elif choice == "View Users":
        st.subheader("View All Users")
        users = get_users(connection)
        for user in users:
            st.write(f"ID: {user['id']}, Name: {user['name']}, Email: {user['email']}, Balance: {user['balance']}")

    elif choice == "Deposit":
        st.subheader("Deposit Money")
        user_id = st.number_input("User ID", min_value=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Deposit"):
            add_transaction(connection, user_id, 'deposit', amount)
            update_balance(connection, user_id, amount, is_deposit=True)
            st.success(f"Deposited {amount} to user ID {user_id}")

    elif choice == "Withdraw":
        st.subheader("Withdraw Money")
        user_id = st.number_input("User ID", min_value=1)
        amount = st.number_input("Amount", min_value=0.01)
        if st.button("Withdraw"):
            add_transaction(connection, user_id, 'withdrawal', amount)
            update_balance(connection, user_id, amount, is_deposit=False)
            st.success(f"Withdrew {amount} from user ID {user_id}")

if __name__ == '__main__':
    main()
