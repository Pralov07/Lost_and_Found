# Utility function to center a window on the screen
def center_window(win, width, height):
    win.update_idletasks()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")
from tkinter import *
from tkinter import messagebox
import subprocess
import sys
import os
import sqlite3
from db_connection import get_db_connection

# Database initialization 
def initialize_db():
    try:
        with sqlite3.connect('lost_and_found.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT,
                user_type TEXT DEFAULT 'user'
            )
            ''')
            # Add phone column if not exists (for existing DBs)
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
            except sqlite3.OperationalError:
                pass  # Column already exists
            # Add user_type column if not exists (for existing DBs)
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'user'")
            except sqlite3.OperationalError:
                pass  # Column already exists
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

initialize_db()

# User registration logic
def register_user_to_db(username, password, full_name, email, phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, full_name, email, phone, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                       (username, password, full_name, email, phone, 'user'))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


root = Tk()
root.title("Lost & Found Desktop - Login")
center_window(root, 1100, 600)
root.resizable(0, 0)

# Setting the background color
canvas = Canvas(root, width=900, height=600, highlightthickness=0)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Drawing a gradient from sky blue to navy
def get_gradient_color(i):
    # Sky blue RGB: (135, 206, 235)
    # Navy RGB: (0, 0, 128)
    # Calculate ratio based on position
    ratio = i / 599
    
    # Interpolate between sky blue and navy
    r = int(135 - (135 * ratio))
    g = int(206 - (206 * ratio))
    b = int(235 - (107 * ratio))  # 235 to 128
    
    return f'#{r:02x}{g:02x}{b:02x}'

root.update_idletasks()  # Ensure geometry is updated
window_width = root.winfo_width()


for i in range(600):  # window height
    color = get_gradient_color(i)
    canvas.create_line(0, i, window_width, i, fill=color)


# Global variable for register window
register_window = None

# Function to open admin control panel
def open_admin_panel():
    try:
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        admin_panel_path = os.path.join(current_dir, "admin_page.py")
        
        # Clear login fields for security
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        root.destroy()
        subprocess.run([sys.executable, admin_panel_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open admin page: {str(e)}")
        root.deiconify()
        
def open_user_page():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        user_page_path = os.path.join(current_dir, "user_page.py")
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        root.destroy()
        subprocess.run([sys.executable, user_page_path])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open user page: {str(e)}")
        root.deiconify() 

# Function to handle login
def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_type FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user[0]  # user_type
    return None
def handle_login():
    username = username_entry.get().strip()
    password = password_entry.get()
    
    # Basic validation
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password!")
        return
    
    user_type = authenticate_user(username, password)
    if user_type:
        messagebox.showinfo("Success", f"Welcome back, {username}!")
        if user_type == 'admin':
            open_admin_panel()
        else:
            open_user_page()
    else:
        messagebox.showerror("Error", "Invalid username or password!")
        password_entry.delete(0, END)  

# function for registering a new user
def register_user():
    global register_window
    if register_window is not None and register_window.winfo_exists():
        register_window.lift()
        return

    register_window = Toplevel()
    register_window.title("User Registration")
    center_window(register_window, 1100, 600)
    register_window.resizable(0, 0)
    register_window.grab_set()  
    register_window.transient(root)  

    # Create canvas for gradient background
    reg_canvas = Canvas(register_window, width=1100, height=600, highlightthickness=0,)
    reg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    

    def get_gradient_color_reg(i):
        # Sky blue RGB: (135, 206, 235)
        # Navy RGB: (0, 0, 128)
        
        ratio = i / 599
        
        # Interpolate between sky blue and navy
        r = int(135 - (135 * ratio))
        g = int(206 - (206 * ratio))
        b = int(235 - (107 * ratio))  
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    
    
    for i in range(600):  # window height
        color = get_gradient_color_reg(i)
        reg_canvas.create_line(0, i, 1100, i, fill=color)
   

    def on_closing():
        global register_window
        register_window.destroy()
        register_window = None

    register_window.protocol("WM_DELETE_WINDOW", on_closing)

    
    
    lbl_registration = Label(register_window, text="User Registration", font=("Impact", 30), fg="white", bg=get_gradient_color_reg(70))
    reg_canvas.create_window(550, 70, window=lbl_registration, anchor="center")

    # Username
    lbl_username = Label(register_window, text="Username:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(120))
    reg_canvas.create_window(400, 120, window=lbl_username, anchor="center")
    username_entry_reg = Entry(register_window, width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 120, window=username_entry_reg, anchor="center")

    # Full Name
    lbl_full_name = Label(register_window, text="Full Name:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(160))
    reg_canvas.create_window(400, 160, window=lbl_full_name, anchor="center")
    full_name_entry = Entry(register_window, width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 160, window=full_name_entry, anchor="center")

    # Email
    lbl_email = Label(register_window, text="Email:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(210))
    reg_canvas.create_window(400, 210, window=lbl_email, anchor="center")
    email_entry = Entry(register_window, width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 210, window=email_entry, anchor="center")

    # Phone
    lbl_phone = Label(register_window, text="Phone:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(260))
    reg_canvas.create_window(400, 260, window=lbl_phone, anchor="center")
    phone_entry = Entry(register_window, width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 260, window=phone_entry, anchor="center")

    # Password
    lbl_password = Label(register_window, text="Password:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(310))
    reg_canvas.create_window(400, 310, window=lbl_password, anchor="center")
    password_entry_reg = Entry(register_window, show="*", width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 310, window=password_entry_reg, anchor="center")

    # Confirm Password
    lbl_confirm_password = Label(register_window, text="Confirm Password:", font=("Arial", 12, "bold"), fg="white", bg=get_gradient_color_reg(360))
    reg_canvas.create_window(400, 360, window=lbl_confirm_password, anchor="center")
    confirm_password_entry = Entry(register_window, show="*", width=25, font=("Arial", 11), bd=2, highlightthickness=0)
    reg_canvas.create_window(700, 360, window=confirm_password_entry, anchor="center")
   

    def handle_registration():
        username = username_entry_reg.get().strip()
        full_name = full_name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        password = password_entry_reg.get()
        confirm_password = confirm_password_entry.get()
        if not all([username, full_name, email, phone, password, confirm_password]):
            messagebox.showerror("Error", "Please fill all fields!")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return
        if not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Error", "Please enter a valid phone number (at least 10 digits)!")
            return
        result = None
        if password != confirm_password:
            result = "Passwords do not match!"
        elif len(password) < 6:
            result = "Password must be at least 6 characters!"
        elif register_user_to_db(username, password, full_name, email, phone):
            result = f"Registration successful! Welcome, {full_name}!"
        else:
            result = "Username or email already exists!"

        if result.startswith("Registration successful!"):
            messagebox.showinfo("Success", result)
            # Clear the registration fields
            username_entry_reg.delete(0, END)
            full_name_entry.delete(0, END)
            email_entry.delete(0, END)
            phone_entry.delete(0, END)
            password_entry_reg.delete(0, END)
            confirm_password_entry.delete(0, END)
            register_window.destroy()
            # After registration, just close the registration window and show the login page again
            
        else:
            messagebox.showerror("Error", result)

    # Center the buttons with original styling to match login page
    submit_button = Button(register_window, text="Register", width=12, font=("Arial", 12), bg="lightgreen", fg="black", command=handle_registration)
    reg_canvas.create_window(475, 450, window=submit_button, anchor="center")
    cancel_button = Button(register_window, text="Cancel", width=10, font=("Arial", 12), bg="lightcoral", fg="black", command=on_closing)
    reg_canvas.create_window(625, 450, window=cancel_button, anchor="center")

    
    


# Username field - properly centered
username_label = Label(root, text="Username", font=("Calibri", 14), bg=get_gradient_color(250), fg="white")
canvas.create_window(450, 265, window=username_label, anchor="center")

username_entry = Entry(root, width=27, font=("Calibri", 14) )
canvas.create_window(550, 290, window=username_entry, anchor="center")

# Password field - properly centered
password_label = Label(root, text="Password", font=("Calibri", 15), bg=get_gradient_color(300), fg="white")
canvas.create_window(450, 325, window=password_label, anchor="center")

password_entry = Entry(root, show="*", width=27, font=("Calibri", 14) )
canvas.create_window(550, 350, window=password_entry, anchor="center")

# Buttons - centered horizontally with original styling
login_btn = Button(root, text="Login", width=10, fg="white", font=("Arial", 13), bg="teal", command=handle_login)
canvas.create_window(550, 430, window=login_btn, anchor="center")

register_btn = Button(root, text="Register", width=12, fg="white", font=("Arial", 13), bg="Teal", command=register_user)
canvas.create_window(550, 480, window=register_btn, anchor="center")

#App name

app_name_text = canvas.create_text(
    550, 90,
    text="Lost & Found App",
    font=("Impact", 35, "bold"),
    fill="white",
    anchor="center"
)

app_name_text2 = canvas.create_text(
    550, 135,
    text="Reuniting people with their missing stuff.",
    font=("Rockwell", 17),
    fill="white",
    anchor="center"
)


# Center the text horizontally
app_name_text = canvas.create_text(550, 90, text="", font=("Impact", 35, "bold"), fill="white", anchor="center")
app_name_text2 = canvas.create_text(550, 135, text="", font=("Rockwell", 20), fill="white", anchor="center")
app_name_text3 = canvas.create_text(550, 170, text="", font=("Rockwell", 20), fill="white", anchor="center")


footer_text1 = canvas.create_text(
    550, 553,  # x, y position
    text="Let's Find What is Lost", 
    font=("Open Sans", 12, "bold"),
    fill="#000000",
    anchor="center"
)

footer_text2 = canvas.create_text(
    550, 570,  # x, y position (centered at bottom)
    text="Made With Love By The Flickers",
    font=("Open Sans", 10),
    fill="#000000",
    anchor="center"
)


root.mainloop()