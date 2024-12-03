from tkinter import *
from tkinter import messagebox
import time

# Import from other Python files
from employees import connect_database


# Function to update the subtitle with the current date and time
def update(subtitleLabel):
    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Employee Dashboard - Billing Section\t\t\t {date_time}')
    subtitleLabel.after(1000, lambda: update(subtitleLabel))


# GUI Helper Functions

# Function to center the window on the screen
def center_window(window, width=1270, height=668):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (width / 2))
    y_cordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")


# Function to create and place the title of the window
def create_title(window):
    # Load the image and keep a reference to it
    bg_image = PhotoImage(file='assets/inventory.png')

    titleLabel = Label(window, image=bg_image, compound=LEFT, text='\t   Inventory Management System',
                       font=('Helvetica', 32, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
    titleLabel.place(x=0, y=0, relwidth=1)

    # Store the image reference in the window to prevent it from being garbage collected
    window.bg_image = bg_image

    return bg_image

def create_exit_button(window):
    """Creates and places the logout button."""
    logoutButton = Button(window, text='Exit', font=('Helvetica', 15, 'bold'), fg='white', bg='#0f4d7d', bd=0, relief='flat',
                          command=lambda: confirm_exit(window))
    logoutButton.place(x=1190, y=16)

def confirm_exit(window):
    """Shows a confirmation message box before closing the application."""
    response = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
    if response:  # If the user clicked "Yes"
        window.destroy()  # Close the window

# Function to create and place the subtitle of the window (Date & Time)
def create_subtitle(window):
    subtitleLabel = Label(window, text='Date: 08-07-2024\t\t Time: 12:36:17 pm', font=('Helvetica', 12),
                          bg='#4d636d', fg='white')
    subtitleLabel.place(x=0, y=70, relwidth=1)
    update(subtitleLabel)


# Main Billing Page Creation Function
def create_billing_page(window):
    create_title(window)      # Create the title of the window
    create_exit_button(window)
    create_subtitle(window)   # Create and update the subtitle (Date & Time)
    # Additional functionality can be added here as needed


# The function to create and run the billing page window
def employee_billingPage():
    window = Tk()
    window.title('Billing Page')
    window.resizable(0, 0)  # Disable window resizing
    window.config(bg='white')

    # Center the window on the screen
    center_window(window)

    # Create the billing page UI
    create_billing_page(window)

    # Run the Tkinter event loop
    window.mainloop()


# Running the main window
if __name__ == "__main__":
    employee_billingPage()
