from tkinter import *

# import from another python file
from employees import employee_form
from supplier import supplier_form

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
    titleLabel = Label(window, image=bg_image, compound=LEFT, text='  Inventory Management System',
                       font=('times new roman', 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
    titleLabel.place(x=0, y=0, relwidth=1)
    return bg_image

def create_logout_button(window):
    """Creates and places the logout button."""
    logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='white', bg='#0f4d7d')
    logoutButton.place(x=1100, y=10)

def create_subtitle(window):
    """Creates and places the subtitle label below the title."""
    subtitleLabel = Label(window, text='Welcome Admin\t\t Date: 08-07-2024\t\t Time: 12:36:17 pm',
                          font=('times new roman', 15), bg='#4d636d', fg='white')
    subtitleLabel.place(x=0, y=70, relwidth=1)

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

    # Logo at the top
    imageLabel = Label(leftFrame, image=logoImage)
    imageLabel.pack()

    # Menu label
    menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
    menuLabel.pack(fill=X)

    # Create buttons with icons
    # without lambda this function will call automatically when the code is running (ex: without the click of employee button)
    # lambda is needed when the callback function has parameters
    create_menu_button(leftFrame, employee_icon, ' Employees', lambda: employee_form(window))
    create_menu_button(leftFrame, supplier_icon, ' Suppliers', lambda: supplier_form(window))
    create_menu_button(leftFrame, category_icon, ' Categories', show_categories)
    create_menu_button(leftFrame, products_icon, ' Products', show_products)
    create_menu_button(leftFrame, sales_icon, ' Sales', show_sales)
    create_menu_button(leftFrame, exit_icon, ' Exit', window.quit)

    # Return the images to prevent garbage collection
    return [logoImage, employee_icon, supplier_icon, category_icon, products_icon, sales_icon, exit_icon]

def create_menu_button(frame, icon, text, callback):
    """Creates a menu button inside the given frame."""
    button = Button(frame, image=icon, compound=LEFT, text=text, font=('times new roman', 20, 'bold'),
                    anchor='w', padx=10, command=callback)
    button.pack(fill=X)

def show_categories():
    print("Categories button clicked")
    # Add logic to display category-related functionality

def show_products():
    print("Products button clicked")
    # Add logic to display product-related functionality

def show_sales():
    print("Sales button clicked")
    # Add logic to display sales-related functionality


def create_stat_frame(window, x, y, bg_color, icon_path, title, count):
    """Creates a statistics frame with an icon, title, and count."""
    frame = Frame(window, bg=bg_color, bd=3, relief=RIDGE)
    frame.place(x=x, y=y, height=170, width=280)

    icon = PhotoImage(file=icon_path)
    icon_label = Label(frame, image=icon, bg=bg_color)
    icon_label.pack(pady=10)

    title_label = Label(frame, text=title, bg=bg_color, fg='white', font=('times new roman', 15, 'bold'))
    title_label.pack()

    count_label = Label(frame, text=count, bg=bg_color, fg='white', font=('times new roman', 30, 'bold'))
    count_label.pack()

    # Return the image reference to prevent garbage collection
    return icon


def create_dashboard(window):
    """Main function to create and place all the dashboard statistics frames."""
    # Create employee frame
    emp_icon = create_stat_frame(window, 400, 125, '#2C3E50', 'assets/total_emp.png', 'Total Employees', '0')

    # Create supplier frame
    sup_icon = create_stat_frame(window, 800, 125, '#8E44AD', 'assets/total_sup.png', 'Total Suppliers', '0')

    # Create categories frame
    cat_icon = create_stat_frame(window, 400, 310, '#27AE60', 'assets/total_cat.png', 'Total Categories', '0')

    # Create products frame
    prod_icon = create_stat_frame(window, 800, 310, '#2C3E50', 'assets/total_prod.png', 'Total Products', '0')

    # Create sales frame
    sales_icon = create_stat_frame(window, 600, 495, '#E74C3C', 'assets/total_sales.png', 'Total Sales', '0')

    # Return all icons to prevent garbage collection
    return [emp_icon, sup_icon, cat_icon, prod_icon, sales_icon]

def create_window():
    """Main function to create and run the window."""
    window = Tk()
    window.title('Dashboard')
    window.resizable(0, 0)  # Disable maximize button
    window.config(bg='white')

    center_window(window)  # Center the window on the screen

    # Create components
    bg_image = create_title(window)
    create_logout_button(window)
    create_subtitle(window)
    icons = create_left_menu(window)  # Store the icon images to prevent garbage collection

    # Create the dashboard frames (Total Employees, Total Suppliers, etc.)
    dashboard_icons = create_dashboard(window)

    # Run the Tkinter event loop
    window.mainloop()

# Call the main function to create the window
create_window()
