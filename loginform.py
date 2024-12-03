from tkinter import *
from tkinter import messagebox

from dashboard import create_window  # Import the function for admin dashboard (not run until called)
from billingpage import employee_billingPage
from employees import connect_database  # Import the function to connect to the database

def check_login(employee_id, password, login_window):
    """
    Function to check login credentials against the database.
    """
    # Connect to the database
    cursor, connection = connect_database()

    if not cursor or not connection:  # Check if the connection was successful
        messagebox.showerror('Error', 'Database connection failed')
        return

    try:
        # Use the inventory_system database
        cursor.execute('USE inventory_system')

        # Query to fetch usertype based on employee_id and password
        cursor.execute('SELECT usertype FROM employee_data WHERE empid=%s AND password=%s', (employee_id, password))
        result = cursor.fetchone()

        if result:  # If a result is found (matching employee ID and password)
            usertype = result[0]  # Get the usertype (Admin or Employee)

            if usertype == 'Admin':  # If usertype is Admin
                login_window.destroy()  # Close login window
                create_window()  # Call the admin dashboard
            elif usertype == 'Employee':  # If usertype is Employee
                login_window.destroy()  # Close login window
                employee_billingPage()  # Placeholder for employee dashboard (to be implemented later)
            else:
                messagebox.showerror('Error', 'Invalid UserType')  # Invalid usertype
        else:
            messagebox.showerror('Error', 'Invalid Employee ID or Password')  # Invalid credentials

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')  # Show error message if any exception occurs
    finally:
        cursor.close()  # Close the cursor after use
        connection.close()  # Close the database connection

def toggle_password_visibility(password_entry, eye_button):
    """
    Toggle the visibility of the password in the password entry field.
    """
    if password_entry.cget("show") == "*":
        password_entry.config(show="")  # Show the password
        eye_button.config(image=eye_open_img)  # Update button image to open eye
    else:
        password_entry.config(show="*")  # Hide the password
        eye_button.config(image=eye_closed_img)  # Update button image to closed eye

def login_form():
    """
    Create and display the login form window.
    """
    # Initialize the login window
    login_window = Tk()
    login_window.title("Login")
    login_window.resizable(False, False)  # Disable window resizing

    # Set window size
    window_width = 600
    window_height = 400

    # Get screen width and height
    screen_width = login_window.winfo_screenwidth()
    screen_height = login_window.winfo_screenheight()

    # Calculate position to center the window
    x_position = int((screen_width - window_width) / 2)
    y_position = int((screen_height - window_height) / 2)

    # Set the window size and position it in the center
    login_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    login_window.config(bg="white")

    # Title label for the login window
    title_label = Label(login_window, text="Inventory Management System", font=("Helvetica", 24, "bold"), bg="#0F4D7D", fg="white")
    title_label.pack(pady=10, fill='x')

    # Create a frame to contain the left image and the form on the right side
    frame = Frame(login_window, bg="white")
    frame.pack(padx=20, pady=20)

    # Left side: Load and display an image (if available)
    try:
        img = PhotoImage(file="assets/login.png")  # Use your image path here
        image_label = Label(frame, image=img, bg="white")
        image_label.grid(row=0, column=0, padx=10, pady=10)
        image_label.image = img  # Store reference to prevent garbage collection
        login_window.img_reference = img  # Store reference in login_window
    except Exception as e:
        print(f"Error loading image: {e}")  # Print error if the image fails to load

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
    eye_open_img = PhotoImage(file="assets/open_eye.png")  # Open eye image
    eye_closed_img = PhotoImage(file="assets/close_eye.png")  # Closed eye image

    eye_button = Button(form_frame, image=eye_closed_img, bg="white", bd=0, command=lambda: toggle_password_visibility(password_entry, eye_button))
    eye_button.grid(row=4, column=1, padx=5)

    # Store image references in the window to prevent garbage collection
    login_window.eye_open_img = eye_open_img
    login_window.eye_closed_img = eye_closed_img

    # Login button to submit credentials
    login_button = Button(form_frame, text="Login", font=("Helvetica", 14), bg="#0F4D7D", fg="white", width=20,
                          command=lambda: check_login(employee_id_entry.get(), password_entry.get(), login_window))
    login_button.grid(row=5, column=0, pady=20, sticky='w')

    # Run the login window
    login_window.mainloop()

# Start the login form when the script is run
if __name__ == "__main__":
    login_form()
