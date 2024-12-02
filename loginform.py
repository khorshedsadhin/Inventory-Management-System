from tkinter import *
from tkinter import messagebox

from dashboard import create_window  # Import the function, but it won't run until called
from employees import connect_database

def check_login(employee_id, password, login_window):
    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Database connection failed')
        return

    try:
        cursor.execute('USE inventory_system')
        # Fetch the usertype based on employee_id and password
        cursor.execute('SELECT usertype FROM employee_data WHERE empid=%s AND password=%s', (employee_id, password))
        result = cursor.fetchone()

        # Debugging: print the result
        print(f"Query result: {result}")

        if result:  # Check if there was a match
            usertype = result[0]
            print(f'UserType: {usertype}')  # Debugging statement to check the usertype
            if usertype == 'Admin':  # Changed to 'Admin' with uppercase
                # Admin user: Open admin dashboard
                login_window.destroy()  # Close login window
                create_window()  # Call admin dashboard
            elif usertype == 'Employee':  # Changed to 'Employee' with uppercase
                # Employee user: Open employee dashboard (function to be defined later)
                login_window.destroy()  # Close login window
                employee_dashboard()  # Placeholder for employee dashboard
            else:
                messagebox.showerror('Error', 'Invalid UserType')
        else:
            messagebox.showerror('Error', 'Invalid Employee ID or Password')

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
        print(f'Error: {e}')  # Debugging statement to track errors

    finally:
        cursor.close()
        connection.close()

def toggle_password_visibility(password_entry, eye_button):
    """Toggle the visibility of the password"""
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        eye_button.config(image=eye_open_img)  # Update button image to open eye
    else:
        password_entry.config(show="*")
        eye_button.config(image=eye_closed_img)  # Update button image to closed eye

def login_form():
    # Initialize the window
    login_window = Tk()
    login_window.title("Login")

    # Set window size (smaller window)
    window_width = 600  # Reduced the window width
    window_height = 400  # Reduced the window height

    # Get screen width and height
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    # Calculate position to center the window
    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)

    # Set the window size and position it in the center
    login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    login_window.config(bg="white")

    # Title label for "Inventory Management System"
    title_label = Label(login_window, text="Inventory Management System", font=("Helvetica", 24, "bold"), bg="#0F4D7D", fg="white")
    title_label.pack(pady=10, fill='x')

    # Create a frame to contain the left image and the form on the right side
    frame = Frame(login_window, bg="white")
    frame.pack(padx=20, pady=20)

    # Left side: Load and display an image using PhotoImage
    try:
        # Replace this with the correct path to your image file (png, gif supported)
        img = PhotoImage(file="assets/login.png")  # Use your image path here
        image_label = Label(frame, image=img, bg="white")
        image_label.grid(row=0, column=0, padx=10, pady=10)
        image_label.image = img  # Keep a reference to the image
    except Exception as e:
        print(f"Error loading image: {e}")

    # Right side: Create the login form (employee ID, password, and login button)
    form_frame = Frame(frame, bg="white")
    form_frame.grid(row=0, column=1, padx=20)

    # Employee ID label and entry
    employee_id_label = Label(form_frame, text="Employee ID", font=("Helvetica", 14), bg="white")
    employee_id_label.grid(row=1, column=0, pady=5)
    employee_id_entry = Entry(form_frame, font=("Helvetica", 14), width=20)
    employee_id_entry.grid(row=2, column=0, pady=5)

    # Password label and entry
    password_label = Label(form_frame, text="Password", font=("Helvetica", 14), bg="white")
    password_label.grid(row=3, column=0, pady=5)
    password_entry = Entry(form_frame, font=("Helvetica", 14), width=20, show="*")
    password_entry.grid(row=4, column=0, pady=5)

    # Eye button for password visibility toggle
    global eye_open_img, eye_closed_img
    eye_open_img = PhotoImage(file="assets/open_eye.png")  # Use the correct path for the open eye image
    eye_closed_img = PhotoImage(file="assets/close_eye.png")  # Use the correct path for the closed eye image

    eye_button = Button(form_frame, image=eye_closed_img, bg="white", bd=0, command=lambda: toggle_password_visibility(password_entry, eye_button))
    eye_button.grid(row=4, column=1, padx=5)

    # Login button
    login_button = Button(form_frame, text="Login", font=("Helvetica", 14), bg="#0F4D7D", fg="white", width=20,
                          command=lambda: check_login(employee_id_entry.get(), password_entry.get(), login_window))
    login_button.grid(row=5, column=0, pady=20, sticky='w')

    # Run the login window
    login_window.mainloop()

# Placeholder for employee dashboard function
def employee_dashboard():
    messagebox.showinfo("Info", "Employee Dashboard will be created later.")

# Start the login form
if __name__ == "__main__":
    login_form()
