from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
import time
import re
import json  # To serialize cart items for saving in sales_data

# Import from other Python files
from employees import connect_database


# Function to update the subtitle with the current date and time
def update(subtitleLabel):
    """Updates the subtitle label with the current time and date."""
    date_time = time.strftime('%I:%M:%S %p on %A, %B %d, %Y')
    subtitleLabel.config(text=f'Employee Dashboard - Billing Section\t\t\t {date_time}')
    subtitleLabel.after(1000, lambda: update(subtitleLabel))


# GUI Helper Functions

def center_window(window, width=1270, height=800):
    """Centers the window on the screen with the given width and height."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))
    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")


def create_title(window):
    """Creates and places the title label in the window."""
    try:
        bg_image = PhotoImage(file='assets/inventory.png')
    except Exception as e:
        messagebox.showerror("Image Load Error", f"Error loading title image: {e}")
        bg_image = None

    title_label = Label(window, image=bg_image, compound=LEFT, text='\t   Inventory Management System',
                        font=('Helvetica', 32, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
    title_label.grid(row=0, column=0, columnspan=3, sticky='we')

    if bg_image:
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


def create_subtitle(window):
    """Creates and places the subtitle (Date & Time) on the window."""
    subtitle_label = Label(window, text='', font=('Helvetica', 12),
                           bg='#4d636d', fg='white')
    subtitle_label.grid(row=1, column=0, columnspan=3, sticky='we')
    update(subtitle_label)


def fetch_product_data():
    """Fetch product data from the 'product_data' table in the database."""
    # Establishing connection to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return []

    try:
        cursor.execute('USE inventory_system')  # If using MySQL, select the database
        # Query to fetch product data
        query = "SELECT id, name, price, quantity, status FROM product_data"
        cursor.execute(query)
        product_data = cursor.fetchall()  # Fetch all rows
    except Exception as e:
        # Show error using messagebox instead of printing to console
        messagebox.showerror("Data Fetch Error", f"Error fetching product data: {e}")
        product_data = []
    finally:
        cursor.close()
        connection.close()

    return product_data


def product_treeview_with_label(window):
    """Creates and places a Treeview widget for displaying product information with an integrated 'All Products' label."""
    global product_treeview_widget  # Declare as global to access in refresh_product_treeview
    # Parent frame for the label and treeview
    treeview_parent_frame = Frame(window, bg='white', bd=3, relief=RIDGE)
    treeview_parent_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

    # Label for 'All Products'
    all_products_label = Label(treeview_parent_frame, text='All Products', font=('Helvetica', 16, 'bold'),
                               bg='#0f4d7d', fg='white')
    all_products_label.pack(fill='x')

    # Frame for Treeview and Scrollbars
    treeview_frame = Frame(treeview_parent_frame, bg='white')
    treeview_frame.pack(fill=BOTH, expand=1)

    # Scrollbars for Treeview
    Scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    Scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    product_treeview_widget = ttk.Treeview(treeview_frame,
                                columns=('id', 'name', 'price', 'quantity', 'status'),
                                show='headings', yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)

    # Configure scrollbars
    Scrolly.pack(side=RIGHT, fill=Y)
    Scrollx.pack(side=BOTTOM, fill=X)
    Scrolly.config(command=product_treeview_widget.yview)
    Scrollx.config(command=product_treeview_widget.xview)

    # Treeview columns and headings
    product_treeview_widget.heading('id', text='Id')
    product_treeview_widget.heading('name', text='Product Name')
    product_treeview_widget.heading('price', text='Price')
    product_treeview_widget.heading('quantity', text='Quantity')
    product_treeview_widget.heading('status', text='Status')

    product_treeview_widget.column('id', width=35, anchor='center')
    product_treeview_widget.column('name', width=150, anchor='w')
    product_treeview_widget.column('price', width=80, anchor='e')
    product_treeview_widget.column('quantity', width=100, anchor='center')
    product_treeview_widget.column('status', width=100, anchor='center')

    # Fetch product data from the database
    product_data = fetch_product_data()

    # Insert data into the Treeview
    for product in product_data:
        product_treeview_widget.insert('', 'end', values=product)

    product_treeview_widget.pack(fill=BOTH, expand=1)

    return product_treeview_widget


def create_customer_and_cart_frame(window, bill_text):
    """Creates and places the 'Customer Details' and 'Cart' frames side by side."""
    # Parent frame to hold Customer Details and Cart side by side
    customer_cart_frame = Frame(window, bg='white', bd=3, relief=RIDGE)
    customer_cart_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

    # Create Customer Details frame inside 'customer_cart_frame'
    customer_details_frame = Frame(customer_cart_frame, bg='#f4f4f4', bd=3, relief=RIDGE)
    customer_details_frame.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    # Configure grid columns to allow the label to expand fully
    customer_details_frame.grid_columnconfigure(0, weight=1)
    customer_details_frame.grid_columnconfigure(1, weight=1)

    # Label for 'Customer Details'
    customer_details_label = Label(customer_details_frame, text='Customer Details', font=('Helvetica', 16, 'bold'),
                                   bg='#0f4d7d', fg='white')
    customer_details_label.grid(row=0, column=0, columnspan=2, sticky='we')

    # Customer name entry
    customer_name_label = Label(customer_details_frame, text="Customer Name", font=('Helvetica', 12), bg='#f4f4f4')
    customer_name_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')

    customer_name_entry = Entry(customer_details_frame, font=('Helvetica', 12), width=20)
    customer_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # Customer contact number entry
    customer_contact_label = Label(customer_details_frame, text="Contact No.", font=('Helvetica', 12), bg='#f4f4f4')
    customer_contact_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')

    customer_contact_entry = Entry(customer_details_frame, font=('Helvetica', 12), width=20)
    customer_contact_entry.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    # Create Cart frame inside 'customer_cart_frame'
    cart_frame = Frame(customer_cart_frame, bg='#f4f4f4', bd=3, relief=RIDGE)
    cart_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

    # Label for 'Cart'
    cart_label = Label(cart_frame, text='Cart', font=('Helvetica', 16, 'bold'),
                       bg='#0f4d7d', fg='white')
    cart_label.pack(side=TOP, fill=X)

    # Treeview for Cart
    cart_tree_frame = Frame(cart_frame, bg='white')
    cart_tree_frame.pack(fill=BOTH, expand=1)

    cart_scrollx = Scrollbar(cart_tree_frame, orient=HORIZONTAL)
    cart_scrolly = Scrollbar(cart_tree_frame, orient=VERTICAL)

    cart_treeview = ttk.Treeview(cart_tree_frame,
                                 columns=('id', 'name', 'price', 'quantity', 'total'),
                                 show='headings',
                                 yscrollcommand=cart_scrolly.set,
                                 xscrollcommand=cart_scrollx.set)

    cart_scrolly.pack(side=RIGHT, fill=Y)
    cart_scrollx.pack(side=BOTTOM, fill=X)
    cart_scrolly.config(command=cart_treeview.yview)
    cart_scrollx.config(command=cart_treeview.xview)

    # Define headings
    cart_treeview.heading('id', text='Id')
    cart_treeview.heading('name', text='Product Name')
    cart_treeview.heading('price', text='Price')
    cart_treeview.heading('quantity', text='Quantity')
    cart_treeview.heading('total', text='Total')

    # Define column widths
    cart_treeview.column('id', width=35, anchor='center')
    cart_treeview.column('name', width=150, anchor='w')
    cart_treeview.column('price', width=80, anchor='e')
    cart_treeview.column('quantity', width=80, anchor='center')
    cart_treeview.column('total', width=80, anchor='e')

    cart_treeview.pack(fill=BOTH, expand=1)

    # Bind double-click to edit quantity
    cart_treeview.bind('<Double-1>', lambda event: edit_quantity(event, cart_treeview))

    # Create the Generate Bill button below the Cart frame
    generate_bill_button = Button(customer_cart_frame, text='Generate Bill', font=('Helvetica', 15, 'bold'),
                                  fg='white', bg='#0f4d7d', bd=0, relief='flat',
                                  command=lambda: generate_bill(window, (customer_name_entry, customer_contact_entry), cart_treeview, bill_text))
    generate_bill_button.grid(row=2, column=0, pady=10)

    return customer_name_entry, customer_contact_entry, cart_treeview


def create_bill_display_frame(window):
    """Creates and places the 'Generated Bill' frame."""
    bill_display_frame = Frame(window, bg='white', bd=3, relief=RIDGE)
    bill_display_frame.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

    # Configure grid weights for fixed sizing
    window.grid_columnconfigure(2, weight=1, minsize=250)  # Generated Bill
    bill_display_frame.grid_rowconfigure(1, weight=1)
    bill_display_frame.grid_columnconfigure(0, weight=1)

    # Label for 'Generated Bill'
    bill_label = Label(bill_display_frame, text='Generated Bill', font=('Helvetica', 16, 'bold'),
                      bg='#0f4d7d', fg='white')
    bill_label.grid(row=0, column=0, sticky='we')

    # Text widget to display the bill
    bill_text = Text(bill_display_frame, font=('Helvetica', 12))
    bill_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    bill_text.config(state=DISABLED)

    return bill_text


def edit_quantity(event, cart_treeview):
    """Allows the user to edit the quantity of a selected cart item."""
    selected_item = cart_treeview.focus()
    if not selected_item:
        return

    # Get current quantity
    try:
        current_quantity = int(cart_treeview.item(selected_item)['values'][3])
    except (IndexError, ValueError):
        messagebox.showerror("Error", "Invalid quantity value.")
        return

    # Prompt user to enter new quantity
    new_quantity = simpledialog.askinteger("Update Quantity", "Enter new quantity:",
                                           initialvalue=current_quantity, minvalue=1)
    if new_quantity is None:
        return  # User cancelled

    # Update quantity and total
    try:
        price = float(cart_treeview.item(selected_item)['values'][2])
    except (IndexError, ValueError):
        messagebox.showerror("Error", "Invalid price value.")
        return

    total = price * new_quantity
    cart_treeview.item(selected_item, values=(
        cart_treeview.item(selected_item)['values'][0],
        cart_treeview.item(selected_item)['values'][1],
        f"{price:.2f}",
        new_quantity,
        f"{total:.2f}"
    ))


def add_to_cart(event, product_tree, cart_tree):
    """Adds the selected product to the cart."""
    selected_item = product_tree.focus()
    if not selected_item:
        return

    product = product_tree.item(selected_item)['values']
    if not product:
        return

    try:
        product_id = product[0]
        name = product[1]
        price = float(product[2])
    except (IndexError, ValueError):
        messagebox.showerror("Error", "Invalid product data.")
        return

    # Check if the product is already in the cart
    for child in cart_tree.get_children():
        cart_item = cart_tree.item(child)['values']
        if cart_item and cart_item[0] == product_id:
            # If exists, increment quantity
            try:
                current_quantity = int(cart_item[3])
            except (IndexError, ValueError):
                current_quantity = 1
            new_quantity = current_quantity + 1
            new_total = price * new_quantity
            cart_tree.item(child, values=(
                product_id,
                name,
                f"{price:.2f}",
                new_quantity,
                f"{new_total:.2f}"
            ))
            return

    # If not in cart, add as new item with quantity 1
    total = price * 1
    cart_tree.insert('', 'end', values=(
        product_id,
        name,
        f"{price:.2f}",
        1,
        f"{total:.2f}"
    ))


def generate_bill(window, customer_entries, cart_tree, bill_text):
    """Generates the bill using customer details and cart information."""
    customer_name = customer_entries[0].get().strip()
    customer_contact = customer_entries[1].get().strip()

    # Contact validation: 11 digits, starts with "01", third digit 3-9, other 8 can be any digit
    if not re.fullmatch(r"01[3-9]\d{8}", customer_contact):
        messagebox.showerror('Error', 'Invalid contact number!')
        return

    if not customer_name or not customer_contact:
        messagebox.showerror("Input Error", "Please enter customer name and contact number.")
        return

    cart_items = cart_tree.get_children()
    if not cart_items:
        messagebox.showerror("Cart Empty", "Please add products to the cart before generating a bill.")
        return

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return

    try:
        cursor.execute('USE inventory_system')  # Select the database

        # First, check stock availability
        for item in cart_items:
            values = cart_tree.item(item)['values']
            try:
                product_id = values[0]
                purchased_qty = int(values[3])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid cart item data.")
                connection.close()
                return

            # Fetch current stock
            cursor.execute("SELECT quantity FROM product_data WHERE id = %s", (product_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", f"Product ID {product_id} not found in database.")
                connection.close()
                return

            current_stock = result[0]
            if current_stock < purchased_qty:
                messagebox.showerror("Stock Error", f"Not enough stock for product ID {product_id}. Available: {current_stock}, Requested: {purchased_qty}")
                connection.close()
                return

        # If all items have sufficient stock, proceed to update quantities
        for item in cart_items:
            values = cart_tree.item(item)['values']
            try:
                product_id = values[0]
                purchased_qty = int(values[3])
            except (IndexError, ValueError):
                messagebox.showerror("Error", "Invalid cart item data.")
                connection.close()
                return

            # Update stock
            cursor.execute("UPDATE product_data SET quantity = quantity - %s WHERE id = %s", (purchased_qty, product_id))

        # Commit the stock updates
        connection.commit()

        # Now, generate the bill content
        bill_content = f"*** Inventory Management System ***\n\n"
        bill_content += f"Customer Name: {customer_name}\n"
        bill_content += f"Contact No.: {customer_contact}\n"
        bill_content += f"Date & Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        bill_content += f"{'Id':<5}{'Product':<20}{'Price':<10}{'Qty':<10}{'Total':<10}\n"
        bill_content += "-" * 55 + "\n"

        grand_total = 0
        bill_items = []
        for item in cart_items:
            values = cart_tree.item(item)['values']
            try:
                id_ = values[0]
                product = values[1]
                price = float(values[2])
                qty = int(values[3])
                total = float(values[4])
                bill_content += f"{id_:<5}{product:<20}{price:<10.2f}{qty:<10}{total:<10.2f}\n"
                grand_total += total

                # Prepare item data for saving
                bill_items.append({
                    'id': id_,
                    'product': product,
                    'price': price,
                    'quantity': qty,
                    'total': total
                })
            except (IndexError, ValueError):
                continue  # Skip invalid entries

        bill_content += "-" * 55 + "\n"
        bill_content += f"{'':<35}Grand Total: {grand_total:.2f}\n"

        # Display the bill in the Bill Display Frame
        bill_text.config(state=NORMAL)
        bill_text.delete('1.0', END)
        bill_text.insert(END, bill_content)
        bill_text.config(state=DISABLED)

        # Now, save the bill to the 'sales_data' table
        # Assuming 'sales_data' table has columns: id, customer_name, contact_no, date_time, total, items
        # 'items' can be stored as a JSON string

        try:
            items_json = json.dumps(bill_items)
            current_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(
                "INSERT INTO sales_data (customer_name, contact_no, date_time, total, items) VALUES (%s, %s, %s, %s, %s)",
                (customer_name, customer_contact, current_datetime, grand_total, items_json)
            )
            connection.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"Error saving bill to sales_data: {e}")
            # Optionally, you might want to rollback stock updates if saving bill fails
            # cursor.execute("ROLLBACK")
            connection.close()
            return

        # Refresh the product_treeview to reflect updated quantities
        refresh_product_treeview()

        # Optionally, clear the cart after generating the bill
        for item in cart_items:
            cart_tree.delete(item)

        messagebox.showinfo("Success", "Bill generated successfully and saved to sales_data.")

    finally:
        cursor.close()
        connection.close()


def create_bill_display_frame(window):
    """Creates and places the 'Generated Bill' frame."""
    bill_display_frame = Frame(window, bg='white', bd=3, relief=RIDGE)
    bill_display_frame.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

    # Configure grid weights for fixed sizing
    window.grid_columnconfigure(2, weight=1, minsize=250)  # Generated Bill
    bill_display_frame.grid_rowconfigure(1, weight=1)
    bill_display_frame.grid_columnconfigure(0, weight=1)

    # Label for 'Generated Bill'
    bill_label = Label(bill_display_frame, text='Generated Bill', font=('Helvetica', 16, 'bold'),
                      bg='#0f4d7d', fg='white')
    bill_label.grid(row=0, column=0, sticky='we')

    # Text widget to display the bill
    bill_text = Text(bill_display_frame, font=('Helvetica', 12))
    bill_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    bill_text.config(state=DISABLED)

    return bill_text


def refresh_product_treeview():
    """Refreshes the All Products Treeview to reflect updated product data."""
    # Re-fetch product data
    product_data = fetch_product_data()

    # Refresh the Treeview by deleting all existing items and inserting updated data
    try:
        product_treeview_widget.delete(*product_treeview_widget.get_children())
        for product in product_data:
            product_treeview_widget.insert('', 'end', values=product)
    except NameError:
        # If the Treeview widget is not defined yet
        pass


def employee_billing_page():
    """Creates and runs the billing page window."""
    window = Tk()
    window.title('Billing Page')

    window.config(bg='white')

    # Set window size and center it
    center_window(window, width=1270, height=800)

    # Configure grid weights for fixed sizing
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(0, weight=1, minsize=385)  # All Products
    window.grid_columnconfigure(1, weight=1, minsize=480)  # Customer Details & Cart
    window.grid_columnconfigure(2, weight=1, minsize=250)  # Generated Bill

    # Create the billing page UI
    create_title(window)            # Create and place the title
    create_exit_button(window)      # Create and place the exit button
    create_subtitle(window)         # Create and update the subtitle

    product_tree = product_treeview_with_label(window)     # Create and place the Treeview for product details

    # Create the Generated Bill display frame
    bill_text = create_bill_display_frame(window)

    # Create Customer Details and Cart frames, passing bill_text
    customer_name_entry, customer_contact_entry, cart_treeview = create_customer_and_cart_frame(window, bill_text)

    # Bind the product Treeview double-click to add to cart
    product_tree.bind('<Double-1>', lambda event: add_to_cart(event, product_tree, cart_treeview))

    # Run the Tkinter event loop
    window.mainloop()

"""
# Running the main window
if __name__ == "__main__":
    employee_billing_page()
"""
