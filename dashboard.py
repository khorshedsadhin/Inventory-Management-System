from tkinter import *
import time

# Import from other Python files
from employees import employee_form
from employees import connect_database
from supplier import supplier_form
from category import category_form
from products import product_form

# Global variable to track the currently displayed frame, ensuring only one frame is visible at a time
current_frame = None

def show_form(form_function, window):
    """
    Ensures only one frame is visible at a time by hiding the current frame if it exists,
    then displaying the new frame created by form_function.
    """
    global current_frame  # Access the global variable to track the currently open frame
    # Hide the current frame if one is open
    if current_frame:
        current_frame.place_forget()  # Removes the frame from view without destroying it

    # Create and display the new frame by calling the provided form function
    current_frame = form_function(window)

def initialize_database():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    # Create the database if it doesn't exist
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create the tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_data (
            empid INT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            gender VARCHAR(50),
            contact VARCHAR(30),
            education VARCHAR(30),
            address VARCHAR(100),
            doj VARCHAR(30),
            salary VARCHAR(50),
            usertype VARCHAR(50),
            password VARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(100),
            supplier VARCHAR(100),
            price DECIMAL(10,2),
            quantity INT,
            status VARCHAR(50)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice INT PRIMARY KEY,
            name VARCHAR(100),
            contact VARCHAR(15),
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_data (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            sale_id INT AUTO_INCREMENT PRIMARY KEY,
            product_id INT,
            quantity_sold INT,
            sale_date DATETIME
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

def update(subtitleLabel, stat_labels):
    """
    Updates the count labels and subtitle label periodically.
    """
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_system')

    # Fetch and update employee count
    cursor.execute('SELECT * FROM employee_data')
    emp_records = cursor.fetchall()
    stat_labels['employee'].config(text=len(emp_records))

    # Fetch and update supplier count
    cursor.execute('SELECT * FROM supplier_data')
    sup_records = cursor.fetchall()
    stat_labels['supplier'].config(text=len(sup_records))

    # Fetch and update category count
    cursor.execute('SELECT * FROM category_data')
    cat_records = cursor.fetchall()
    stat_labels['category'].config(text=len(cat_records))

    # Fetch and update product count
    cursor.execute('SELECT * FROM product_data')
    prod_records = cursor.fetchall()
    stat_labels['product'].config(text=len(prod_records))

    # Fetch and update sales count (example query; adjust as needed)
    cursor.execute('SELECT COUNT(*) FROM sales_data')
    sales_count = cursor.fetchone()[0]
    stat_labels['sales'].config(text=sales_count)

    # Update subtitle label with current date and time
    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Welcome Admin\t\t\t {date_time}')

    # Schedule the next update
    subtitleLabel.after(1000, lambda: update(subtitleLabel, stat_labels))

# GUI part
def center_window(window, width=1270, height=668):
    """Centers the window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (width/2))
    y_cordinate = int((screen_height/2) - (height/2))
    window.geometry(f"{width}x{height}+{x_cordinate}+{y_cordinate}")

def create_title(window):
    """Creates and places the title label at the top of the window."""
    bg_image = PhotoImage(file='assets/inventory.png')
    titleLabel = Label(
        window,
        image=bg_image,
        compound=LEFT,
        text='\t   Inventory Management System',
        font=('Helvetica', 32, 'bold'),
        bg='#010c48',
        fg='white',
        anchor='w',
        padx=20
    )
    titleLabel.place(x=0, y=0, relwidth=1)
    return bg_image

def create_subtitle(window, stat_labels):
    """
    Creates and places the subtitle label below the title.
    """
    subtitleLabel = Label(
        window,
        text='Welcome Admin\t\t Date: 08-07-2024\t\t Time: 12:36:17 pm',
        font=('Helvetica', 12),
        bg='#4d636d',
        fg='white'
    )
    subtitleLabel.place(x=0, y=70, relwidth=1)

    # Start updating
    update(subtitleLabel, stat_labels)

def create_left_menu(window):
    """Creates the left frame with buttons and icons."""
    leftFrame = Frame(window)
    leftFrame.place(x=0, y=102, width=200, height=555)

    # Load all images
    logoImage = PhotoImage(file='assets/logo.png')
    employee_icon = PhotoImage(file='assets/employee.png')
    supplier_icon = PhotoImage(file='assets/supplier.png')
    category_icon = PhotoImage(file='assets/category.png')
    products_icon = PhotoImage(file='assets/product.png')
    sales_icon = PhotoImage(file='assets/sales.png')
    exit_icon = PhotoImage(file='assets/exit.png')

    # Store image references in the `window` to prevent garbage collection
    window.logoImage = logoImage
    window.employee_icon = employee_icon
    window.supplier_icon = supplier_icon
    window.category_icon = category_icon
    window.products_icon = products_icon
    window.sales_icon = sales_icon
    window.exit_icon = exit_icon

    # Logo at the top
    imageLabel = Label(leftFrame, image=logoImage)
    imageLabel.pack()

    # Menu label
    menuLabel = Label(leftFrame, text='Menu', font=('Helvetica', 20, 'bold'), bg='#009688')
    menuLabel.pack(fill=X)

    # Create buttons with icons
    create_menu_button(leftFrame, employee_icon, ' Employees', lambda: show_form(employee_form, window))
    create_menu_button(leftFrame, supplier_icon, ' Suppliers', lambda: show_form(supplier_form, window))
    create_menu_button(leftFrame, category_icon, ' Categories', lambda: show_form(category_form, window))
    create_menu_button(leftFrame, products_icon, ' Products', lambda: product_form(window))
    create_menu_button(leftFrame, sales_icon, ' Sales', show_sales)
    create_menu_button(leftFrame, exit_icon, ' Exit', window.destroy)

    return [logoImage, employee_icon, supplier_icon, category_icon, products_icon, sales_icon, exit_icon]

def create_menu_button(frame, icon, text, callback):
    """Creates a menu button inside the given frame."""
    button = Button(
        frame,
        image=icon,
        compound=LEFT,
        text=text,
        font=('Helvetica', 19, 'bold'),
        anchor='w',
        padx=10,
        command=callback
    )
    button.pack(fill=X)

def show_sales():
    print("Sales button clicked")
    # Add logic to display sales-related functionality

def create_stat_frame(window, x, y, bg_color, icon_path, title):
    """
    Creates a statistics frame with an icon, title, and count.
    """
    frame = Frame(window, bg=bg_color, bd=3, relief=RIDGE)
    frame.place(x=x, y=y, height=170, width=280)

    icon = PhotoImage(file=icon_path)
    icon_label = Label(frame, image=icon, bg=bg_color)
    icon_label.pack(pady=10)

    title_label = Label(frame, text=title, bg=bg_color, fg='white', font=('Helvetica', 15, 'bold'))
    title_label.pack()

    count_label = Label(frame, text='0', bg=bg_color, fg='white', font=('Helvetica', 30, 'bold'))
    count_label.pack()

    # Return the count label and the icon reference
    return count_label, icon

def create_dashboard(window):
    """
    Main function to create and place all the dashboard statistics frames.
    """
    stat_labels = {}

    # Create employee frame
    emp_label, emp_icon = create_stat_frame(window, 400, 125, '#2C3E50', 'assets/total_emp.png', 'Total Employees')
    stat_labels['employee'] = emp_label

    # Create supplier frame
    sup_label, sup_icon = create_stat_frame(window, 800, 125, '#8E44AD', 'assets/total_sup.png', 'Total Suppliers')
    stat_labels['supplier'] = sup_label

    # Create categories frame
    cat_label, cat_icon = create_stat_frame(window, 400, 310, '#27AE60', 'assets/total_cat.png', 'Total Categories')
    stat_labels['category'] = cat_label

    # Create products frame
    prod_label, prod_icon = create_stat_frame(window, 800, 310, '#2C3E50', 'assets/total_prod.png', 'Total Products')
    stat_labels['product'] = prod_label

    # Create sales frame
    sales_label, sales_icon = create_stat_frame(window, 600, 495, '#E74C3C', 'assets/total_sales.png', 'Total Sales')
    stat_labels['sales'] = sales_label

    # Return all count labels and icons to prevent garbage collection
    return stat_labels, [emp_icon, sup_icon, cat_icon, prod_icon, sales_icon]

def create_window():
    """Main function to create and run the window."""
    window = Tk()
    window.title('Dashboard')
    window.resizable(0, 0)  # Disable maximize button
    window.config(bg='white')

    center_window(window)  # Center the window on the screen
    initialize_database()

    # Create components
    bg_image = create_title(window)
    create_left_menu(window)  # Store the icon images to prevent garbage collection

    # Create the dashboard frames and retrieve the stat_labels dictionary
    stat_labels, dashboard_icons = create_dashboard(window)

    # Create the subtitle and pass stat_labels to it
    create_subtitle(window, stat_labels)

    # Run the Tkinter event loop
    window.mainloop()
