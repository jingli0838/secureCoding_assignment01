import sqlite3
import hashlib
import os

# Database setup (Unsafe: No authentication, No encryption)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
conn.commit()

def register(username, password):
    """Registers a new user (Vulnerable)"""
    # Vulnerability 1: Storing passwords in plaintext (No hashing or salting)
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    print("User registered successfully!")

def login(username, password):
    """Login function (Vulnerable)"""
    # Vulnerability 2: SQL Injection vulnerability (Direct user input in query)
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = cursor.fetchone()
    
    if user:
        print("Login successful!")
    else:
        print("Invalid credentials!")

def delete_user(username):
    """Deletes a user (Vulnerable)"""
    # Vulnerability 3: Lack of authentication for user deletion
    cursor.execute(f"DELETE FROM users WHERE username = '{username}'")
    conn.commit()
    print(f"User {username} deleted.")

def reset_password(username, new_password):
    """Reset password function (Vulnerable)"""
    # Vulnerability 4: No authentication before resetting password
    cursor.execute(f"UPDATE users SET password = '{new_password}' WHERE username = '{username}'")
    conn.commit()
    print("Password reset successful!")

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Delete User\n4. Reset Password\n5. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == "3":
            username = input("Enter username to delete: ")
            delete_user(username)
        elif choice == "4":
            username = input("Enter username: ")
            new_password = input("Enter new password: ")
            reset_password(username, new_password)
        elif choice == "5":
            # Vulnerability 5: Resource leak (Database connection never closed properly)
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
