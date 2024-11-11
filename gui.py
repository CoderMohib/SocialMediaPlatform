import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()

    # You can replace this with your database check logic
    if username == "admin" and password == "admin":
        messagebox.showinfo("Login Success", "Welcome to the Social Media Platform!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

# Create the main window
root = tk.Tk()
root.title("Social Media Platform - Login")

# Create labels and entry fields
label_username = tk.Label(root, text="Username")
label_username.grid(row=0, column=0)

entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1)

label_password = tk.Label(root, text="Password")
label_password.grid(row=1, column=0)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1)

# Create login button
login_button = tk.Button(root, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2)

# Run the application
root.mainloop()
