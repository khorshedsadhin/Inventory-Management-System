from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import json
from datetime import datetime, timedelta

# Import from other Python files
from employees import connect_database

# Function to calculate weekly and monthly sales
def calculate_sales_totals():
    """Calculates weekly and monthly sales totals from the sales_data table."""
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return 0, 0

    weekly_total = 0
    monthly_total = 0

    try:
        cursor.execute('USE inventory_system')  # Select the database

        # Calculate weekly sales (last 7 days)
        one_week_ago = datetime.now() - timedelta(days=7)
        cursor.execute("""
            SELECT SUM(total) FROM sales_data
            WHERE date_time >= %s
        """, (one_week_ago,))
        result = cursor.fetchone()
        weekly_total = result[0] if result[0] else 0

        # Calculate monthly sales (last 30 days)
        one_month_ago = datetime.now() - timedelta(days=30)
        cursor.execute("""
            SELECT SUM(total) FROM sales_data
            WHERE date_time >= %s
        """, (one_month_ago,))
        result = cursor.fetchone()
        monthly_total = result[0] if result[0] else 0

    except Exception as e:
        messagebox.showerror("Data Fetch Error", f"Error calculating sales totals: {e}")
    finally:
        cursor.close()
        connection.close()

    return weekly_total, monthly_total

# Function to fetch sales data based on a filter
def fetch_sales(filter_type='all'):
    """
    Fetches sales records from the sales_data table based on the filter.

    Args:
        filter_type (str): 'weekly', 'monthly', or 'all'.

    Returns:
        list: List of sales tuples.
    """
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return []

    sales = []
    try:
        cursor.execute('USE inventory_system')  # Select the database

        if filter_type == 'weekly':
            start_date = datetime.now() - timedelta(days=7)
            cursor.execute("""
                SELECT id, customer_name, contact_no, date_time, total
                FROM sales_data
                WHERE date_time >= %s
                ORDER BY date_time DESC
            """, (start_date,))
        elif filter_type == 'monthly':
            start_date = datetime.now() - timedelta(days=30)
            cursor.execute("""
                SELECT id, customer_name, contact_no, date_time, total
                FROM sales_data
                WHERE date_time >= %s
                ORDER BY date_time DESC
            """, (start_date,))
        else:  # 'all'
            cursor.execute("""
                SELECT id, customer_name, contact_no, date_time, total
                FROM sales_data
                ORDER BY date_time DESC
            """)

        sales = cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Data Fetch Error", f"Error fetching sales data: {e}")
    finally:
        cursor.close()
        connection.close()

    return sales

# Function to open the billing page with selected sale details
def open_billing_page(sale_id):
    """Opens the billing page populated with the selected sale's details."""
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror("Database Connection Error", "Failed to connect to the database.")
        return

    try:
        cursor.execute('USE inventory_system')  # Select the database
        cursor.execute("""
            SELECT customer_name, contact_no, date_time, total, items
            FROM sales_data
            WHERE id = %s
        """, (sale_id,))
        sale = cursor.fetchone()
        if not sale:
            messagebox.showerror("Error", f"No sale found with ID {sale_id}.")
            return

        customer_name, contact_no, date_time, total, items_json = sale
        items = json.loads(items_json)

        # Create a new window for the billing page
        billing_window = Toplevel()
        billing_window.title(f"Bill #{sale_id}")
        billing_window.geometry("600x500")
        billing_window.config(bg='white')

        # Billing Page Header
        header_label = Label(billing_window, text="Billing Details", font=('Helvetica', 20, 'bold'), bg='white')
        header_label.pack(pady=10)

        # Customer Details
        customer_frame = Frame(billing_window, bg='white')
        customer_frame.pack(pady=5)

        Label(customer_frame, text=f"Customer Name: {customer_name}", font=('Helvetica', 14), bg='white').pack(anchor='w')
        Label(customer_frame, text=f"Contact No.: {contact_no}", font=('Helvetica', 14), bg='white').pack(anchor='w')
        Label(customer_frame, text=f"Date & Time: {date_time.strftime('%Y-%m-%d %H:%M:%S')}", font=('Helvetica', 14), bg='white').pack(anchor='w')

        # Items Treeview
        items_frame = Frame(billing_window, bg='white')
        items_frame.pack(pady=10, fill=BOTH, expand=True)

        columns = ('id', 'name', 'price', 'quantity', 'total')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings')
        for col in columns:
            items_tree.heading(col, text=col.capitalize())
            items_tree.column(col, anchor='center', width=100)
        items_tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Populate items
        for item in items:
            items_tree.insert('', 'end', values=(
                item['id'],
                item['product'],
                f"{item['price']:.2f}",
                item['quantity'],
                f"{item['total']:.2f}"
            ))

        # Scrollbars for items_tree
        items_scrollx = Scrollbar(items_frame, orient=HORIZONTAL, command=items_tree.xview)
        items_scrolly = Scrollbar(items_frame, orient=VERTICAL, command=items_tree.yview)
        items_tree.configure(xscrollcommand=items_scrollx.set, yscrollcommand=items_scrolly.set)
        items_scrollx.pack(side=BOTTOM, fill=X)
        items_scrolly.pack(side=RIGHT, fill=Y)

        # Total Amount
        total_label = Label(billing_window, text=f"Grand Total: {total:.2f}", font=('Helvetica', 16, 'bold'), bg='white')
        total_label.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Error opening billing page: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to create the Sales Form
def sales_form(window):
    """
    Creates and displays the sales management form within the main application window.

    Args:
        window (Tk): The main application window.
    """
    global back_image_sales  # Declare back_image_sales as a global variable to prevent garbage collection

    # Create the main frame for the sales form
    sales_frame = Frame(window, width=1070, height=567, bg='white')
    sales_frame.place(x=200, y=100)

    # Heading label for the sales section
    heading_label = Label(sales_frame, text='Sales Management', font=('Helvetica', 16, 'bold'), bg='#0F4D7D', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)  # relwidth=1 ensures the label spans the width of the frame

    # Back button to exit the sales form
    back_image_sales = PhotoImage(file='assets/back.png')  # Load back button image
    back_button_sales = Button(sales_frame, image=back_image_sales, bd=0, cursor='hand2', bg='white',
                               command=lambda: sales_frame.place_forget())
    back_button_sales.place(x=10, y=30)  # Position the back button

    # ------ Sales Summaries Frame ------ #
    summaries_frame = Frame(sales_frame, bg='white')
    summaries_frame.place(x=30, y=100, width=500, height=100)

    # Weekly Sales
    weekly_label = Label(summaries_frame, text='Weekly Sales:', font=('Helvetica', 14, 'bold'), bg='white')
    weekly_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    weekly_total, monthly_total = calculate_sales_totals()
    weekly_total_label = Label(summaries_frame, text=f"{weekly_total:.2f}", font=('Helvetica', 14), bg='white', fg='green')
    weekly_total_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    # Monthly Sales
    monthly_label = Label(summaries_frame, text='Monthly Sales:', font=('Helvetica', 14, 'bold'), bg='white')
    monthly_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    monthly_total_label = Label(summaries_frame, text=f"{monthly_total:.2f}", font=('Helvetica', 14), bg='white', fg='green')
    monthly_total_label.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    # ------ Filter Options Frame ------ #
    filter_frame = Frame(sales_frame, bg='white')
    filter_frame.place(x=550, y=100, width=500, height=50)

    filter_label = Label(filter_frame, text='Filter Sales:', font=('Helvetica', 14, 'bold'), bg='white')
    filter_label.pack(side=LEFT, padx=10)

    # Variable to hold the selected filter option
    filter_var = StringVar(value='all')

    # Radio buttons for filter options
    all_radio = Radiobutton(filter_frame, text='All', variable=filter_var, value='all',
                           font=('Helvetica', 12), bg='white',
                           command=lambda: update_sales_treeview(sales_tree, filter_var.get()))
    all_radio.pack(side=LEFT, padx=10)

    weekly_radio = Radiobutton(filter_frame, text='Weekly', variable=filter_var, value='weekly',
                               font=('Helvetica', 12), bg='white',
                               command=lambda: update_sales_treeview(sales_tree, filter_var.get()))
    weekly_radio.pack(side=LEFT, padx=10)

    monthly_radio = Radiobutton(filter_frame, text='Monthly', variable=filter_var, value='monthly',
                                font=('Helvetica', 12), bg='white',
                                command=lambda: update_sales_treeview(sales_tree, filter_var.get()))
    monthly_radio.pack(side=LEFT, padx=10)

    # ------ Sales Records Table ------ #
    records_frame = Frame(sales_frame, bg='white')
    records_frame.place(x=30, y=220, width=1020, height=300)

    # Scrollbars for Treeview
    sales_scrollx = Scrollbar(records_frame, orient=HORIZONTAL)
    sales_scrolly = Scrollbar(records_frame, orient=VERTICAL)

    # Treeview widget to display the sales records
    sales_tree = ttk.Treeview(
        records_frame,
        columns=('id', 'customer_name', 'contact_no', 'date_time', 'total'),
        show='headings',
        yscrollcommand=sales_scrolly.set,
        xscrollcommand=sales_scrollx.set
    )

    # Configure scrollbars
    sales_tree.configure(xscrollcommand=sales_scrollx.set, yscrollcommand=sales_scrolly.set)
    sales_scrollx.config(command=sales_tree.xview)
    sales_scrolly.config(command=sales_tree.yview)

    # Define column headings
    sales_tree.heading('id', text='Sale ID')
    sales_tree.heading('customer_name', text='Customer Name')
    sales_tree.heading('contact_no', text='Contact No.')
    sales_tree.heading('date_time', text='Date & Time')
    sales_tree.heading('total', text='Total Amount')

    # Define column widths
    sales_tree.column('id', width=80, anchor='center')
    sales_tree.column('customer_name', width=200, anchor='w')
    sales_tree.column('contact_no', width=120, anchor='center')
    sales_tree.column('date_time', width=180, anchor='center')
    sales_tree.column('total', width=120, anchor='e')

    # Grid layout for Treeview and Scrollbars
    sales_tree.grid(row=0, column=0, sticky='nsew')
    sales_scrollx.grid(row=1, column=0, sticky='we')
    sales_scrolly.grid(row=0, column=1, sticky='ns')

    # Configure grid weights to make Treeview expandable
    records_frame.grid_rowconfigure(0, weight=1)
    records_frame.grid_columnconfigure(0, weight=1)

    # Populate treeview with all sales data initially
    all_sales = fetch_sales('all')
    for sale in all_sales:
        sale_id, customer_name, contact_no, date_time, total = sale
        formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        sales_tree.insert('', 'end', values=(
            sale_id,
            customer_name,
            contact_no,
            formatted_date,
            f"{total:.2f}"
        ))

    # Bind treeview row selection to open billing page
    sales_tree.bind('<Double-1>', lambda event: on_sale_select(event, sales_tree))

    return sales_frame

# Function to update the sales Treeview based on filter
def update_sales_treeview(treeview, filter_type):
    """
    Updates the Treeview with sales data based on the selected filter.

    Args:
        treeview (ttk.Treeview): The Treeview widget to update.
        filter_type (str): 'weekly', 'monthly', or 'all'.
    """
    # Clear existing data
    for item in treeview.get_children():
        treeview.delete(item)

    # Fetch new data based on filter
    sales = fetch_sales(filter_type)

    # Insert new data into Treeview
    for sale in sales:
        sale_id, customer_name, contact_no, date_time, total = sale
        formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
        treeview.insert('', 'end', values=(
            sale_id,
            customer_name,
            contact_no,
            formatted_date,
            f"{total:.2f}"
        ))

# Event handler for selecting a sale record
def on_sale_select(event, treeview):
    """Handles the event when a sale record is double-clicked to open the billing page."""
    selected_item = treeview.focus()
    if not selected_item:
        return

    sale_values = treeview.item(selected_item, 'values')
    if not sale_values:
        return

    sale_id = sale_values[0]
    open_billing_page(sale_id)

# Function to create the Sales Form button in the main window
def add_sales_form_button(window):
    """Adds a button to the main window to open the sales form."""
    sales_form_btn = Button(window, text='Manage Sales', font=('Helvetica', 14, 'bold'),
                            bg='#0F4D7D', fg='white', cursor='hand2',
                            command=open_sales_form)
    sales_form_btn.place(x=50, y=50)  # Adjust the position as needed

# Ensure that the Sales Form is accessible from your main application
def open_sales_form():
    """Function to open the sales form."""
    sales_form_window = Toplevel()
    sales_form_window.title('Sales Management')
    sales_form_window.geometry("1200x700")  # Adjust the size as needed
    sales_form_window.config(bg='white')

    sales_form(sales_form_window)
