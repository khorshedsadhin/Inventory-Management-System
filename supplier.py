import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

# Function to initialize the database and table structure for suppliers if they do not exist
def create_database_table():
    cursor, connection = connect_database()

    # Create database if it does not exist and switch to it
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create supplier_data table with fields invoice, name, contact, and description
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice INT PRIMARY KEY,
            name VARCHAR(100),
            contact VARCHAR(15),
            description TEXT
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

# Function to delete a selected supplier entry from the database and refresh the view
def delete_supplier(invoice, treeview):
    """
    Deletes a supplier record from the database after user confirmation.

    Args:
        invoice (int): The invoice number of the supplier to be deleted.
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
    """
    # Prompt the user for confirmation before deletion
    confirm = messagebox.askyesno('Confirm Deletion', 'Do you really want to delete the selected record?')
    if not confirm:
        return  # User chose not to delete; exit the function

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Failed to connect to the database.')
        return

    try:
        # Select the inventory_system database
        cursor.execute('USE inventory_system')

        # Execute the DELETE statement with parameterized query to prevent SQL injection
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s', (invoice,))
        connection.commit()  # Commit the transaction to save changes

        # Refresh the treeview to reflect the deletion
        treeview_data(treeview)

        # Inform the user that the record has been successfully deleted
        messagebox.showinfo('Success', 'Record has been deleted successfully.')

    except Exception as e:
        # Show an error message if something goes wrong during deletion
        messagebox.showerror('Error', f'An error occurred while deleting the record: {e}')

    finally:
        # Close the database connection
        cursor.close()
        connection.close()

# Function to clear data from the input fields; optionally deselects treeview selection
def clear(invoice_entry, name_entry, contact_entry, description_text, treeview, deselect_treeview=True):
    """
    Clears the input fields and optionally deselects any selected row in the treeview.

    Args:
        invoice_entry (Entry): Entry widget for Invoice Number.
        name_entry (Entry): Entry widget for Supplier Name.
        contact_entry (Entry): Entry widget for Supplier Contact.
        description_text (Text): Text widget for Description.
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
        deselect_treeview (bool): Whether to deselect the selected row in the treeview.
    """
    # Clear all input fields
    invoice_entry.delete(0, END)
    name_entry.delete(0, END)
    contact_entry.delete(0, END)
    description_text.delete(1.0, END)

    # Deselect any selected row in the treeview if specified
    if deselect_treeview:
        treeview.selection_remove(treeview.selection())

# Function to populate input fields when a row is selected in treeview
def select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview):
    """
    Populates the input fields with data from the selected row in the treeview.

    Args:
        event: The event object.
        invoice_entry (Entry): Entry widget for Invoice Number.
        name_entry (Entry): Entry widget for Supplier Name.
        contact_entry (Entry): Entry widget for Supplier Contact.
        description_text (Text): Text widget for Description.
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
    """
    index = treeview.selection()
    if not index:
        return  # No selection

    content = treeview.item(index)
    row = content['values']

    # Clear input fields and populate with selected row data
    clear(invoice_entry, name_entry, contact_entry, description_text, treeview, deselect_treeview=False)
    invoice_entry.insert(0, row[0])
    name_entry.insert(0, row[1])

    # Ensure contact number starts with "0"
    contact_number = str(row[2])
    if not contact_number.startswith("0"):
        contact_number = "0" + contact_number

    contact_entry.insert(0, contact_number)
    description_text.insert(1.0, row[3])

# Function to retrieve and display all supplier records from the database in treeview
def treeview_data(treeview):
    """
    Retrieves all supplier records from the database and displays them in the treeview.

    Args:
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
    """
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Failed to connect to the database.')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM supplier_data')
        records = cursor.fetchall()

        # Clear existing rows and repopulate treeview with fetched records
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred while fetching data: {e}')

    finally:
        cursor.close()
        connection.close()

# Function to add a new supplier to the database; includes validation and duplication check
def add_supplier(invoice, contact, name, description, treeview):
    """
    Adds a new supplier to the database after validating inputs and checking for duplicates.

    Args:
        invoice (str): The invoice number of the supplier.
        contact (str): The contact number of the supplier.
        name (str): The name of the supplier.
        description (str): A brief description of the supplier.
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
    """
    # Validate that all fields are filled
    if not invoice or not name or not contact or not description:
        messagebox.showerror('Error', 'All fields are required.')
        return

    # Validate contact number using regex
    if not re.fullmatch(r"01[3-9]\d{8}", contact):
        messagebox.showerror('Error', 'Invalid contact number! It should start with "01" followed by a digit between 3-9 and 8 more digits.')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Failed to connect to the database.')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (invoice,))

        # Check if Invoice ID already exists in the database
        if cursor.fetchone():
            messagebox.showerror('Error', 'Invoice number already exists.')
            return

        # Insert new supplier data into supplier_data table
        cursor.execute('INSERT INTO supplier_data (invoice, name, contact, description) VALUES (%s, %s, %s, %s)',
                       (invoice, name, contact, description))
        connection.commit()
        messagebox.showinfo('Success', 'Supplier added successfully.')
        treeview_data(treeview)  # Refresh treeview to display the new supplier

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred while adding the supplier: {e}')

    finally:
        cursor.close()
        connection.close()

# Function to update an existing supplier in the database
def update_supplier(invoice, contact, name, description, treeview):
    """
    Updates an existing supplier's details in the database after validation.

    Args:
        invoice (str): The invoice number of the supplier to be updated.
        contact (str): The new contact number of the supplier.
        name (str): The new name of the supplier.
        description (str): The new description of the supplier.
        treeview (ttk.Treeview): The treeview widget displaying supplier data.
    """
    # Check if a row is selected in the treeview
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is selected for update.')
        return

    # Validate contact number using regex
    if not re.fullmatch(r"01[3-9]\d{8}", contact):
        messagebox.showerror('Error', 'Invalid contact number! It should start with "01" followed by a digit between 3-9 and 8 more digits.')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Failed to connect to the database.')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s', (invoice,))
        current_data = cursor.fetchone()
        if not current_data:
            messagebox.showerror('Error', 'Supplier not found.')
            return

        # Extract current data (excluding invoice)
        current_data = current_data[1:]
        new_data = (name, contact, description)

        # Check if any changes have been made
        if current_data == new_data:
            messagebox.showinfo('Info', 'No changes detected.')
            return

        # Update the supplier details in the database
        cursor.execute('''
            UPDATE supplier_data
            SET name = %s, contact = %s, description = %s
            WHERE invoice = %s
        ''', (name, contact, description, invoice))
        connection.commit()
        messagebox.showinfo('Success', 'Supplier details updated successfully.')
        treeview_data(treeview)  # Refresh treeview to display updated data

    except Exception as e:
        messagebox.showerror('Error', f'An error occurred while updating the supplier: {e}')

    finally:
        cursor.close()
        connection.close()

# Function to build and display the supplier management form interface
def supplier_form(window):
    """
    Creates and displays the supplier management form within the main application window.

    Args:
        window (Tk): The main application window.
    """
    create_database_table()  # Initialize database and table

    global back_image  # Declare back_image as a global variable to prevent garbage collection

    # Create the main frame for the supplier form
    supplier_frame = Frame(window, width=1070, height=567, bg='white')
    supplier_frame.place(x=200, y=100)

    # Heading label for the supplier section
    heading_label = Label(supplier_frame, text='Manage Supplier Details', font=('Helvetica', 16, 'bold'), bg='#0F4D7D', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)  # relwidth=1 ensures the label spans the width of the frame

    # Back button to exit the supplier form
    back_image = PhotoImage(file='assets/back.png')  # Load back button image
    back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command=lambda: supplier_frame.place_forget())
    back_button.place(x=10, y=30)  # Position the back button

    # Logo for supplier form
    logo = PhotoImage(file='assets/product_category.png')  # Adjust the path as needed
    logo_label = Label(supplier_frame, image=logo, bg='white')
    logo_label.place(x=30, y=100)

    # ------ Left Frame for Supplier Details Entry ------ #
    left_frame = Frame(supplier_frame, bg='white')
    left_frame.place(x=10, y=100)  # Place it inside the supplier frame

    # Invoice Number Label and Entry field
    invoice_label = Label(left_frame, text='Invoice NO .', font=('times new roman', 14, 'bold'), bg='white')
    invoice_label.grid(row=0, column=0, padx=(20, 40), sticky='w')  # 'sticky' aligns the label to the west (left)
    invoice_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    invoice_entry.grid(row=0, column=1)

    # Supplier Name Label and Entry field
    name_label = Label(left_frame, text='Supplier Name .', font=('times new roman', 14, 'bold'), bg='white')
    name_label.grid(row=1, column=0, padx=(20, 40), pady=25, sticky='w')
    name_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    name_entry.grid(row=1, column=1)

    # Supplier Contact Label and Entry field
    contact_label = Label(left_frame, text='Supplier Contact .', font=('times new roman', 14, 'bold'), bg='white')
    contact_label.grid(row=2, column=0, padx=(20, 40), sticky='w')
    contact_entry = Entry(left_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    contact_entry.grid(row=2, column=1)

    # Supplier Description Label and Text field
    description_label = Label(left_frame, text='Description.', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=3, column=0, padx=(20, 40), sticky='nw', pady=25)
    description_text = Text(left_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=3, column=1, pady=25)

    # ------ Buttons for Add, Update, Delete, Clear actions ------ #
    button_frame = Frame(left_frame, bg='white')
    button_frame.grid(row=4, columnspan=2, pady=20)  # Span across 2 columns

    # Add Button
    add_button = Button(
        button_frame,
        text='Add',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: add_supplier(
            invoice_entry.get(),
            contact_entry.get(),
            name_entry.get(),
            description_text.get(1.0, END).strip(),
            treeview
        )
    )
    add_button.grid(row=0, column=0, padx=20)

    # Update Button
    update_button = Button(
        button_frame,
        text='Update',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: update_supplier(
            invoice_entry.get(),
            contact_entry.get(),
            name_entry.get(),
            description_text.get(1.0, END).strip(),
            treeview
        )
    )
    update_button.grid(row=0, column=1)

    # Delete Button
    delete_button = Button(
        button_frame,
        text='Delete',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: delete_supplier(invoice_entry.get(), treeview)
    )
    delete_button.grid(row=0, column=2, padx=20)

    # Clear Button
    clear_button = Button(
        button_frame,
        text='Clear',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: clear(
            invoice_entry,
            name_entry,
            contact_entry,
            description_text,
            treeview,
            deselect_treeview=True
        )
    )
    clear_button.grid(row=0, column=3, padx=20)

    # ------ Right Frame for Supplier Data Display (Table) ------ #
    right_frame = Frame(supplier_frame, bg='white')
    right_frame.place(x=520, y=95, width=500, height=345)

    # Scrollbars for treeview
    Scrolly = Scrollbar(right_frame, orient=VERTICAL)  # Vertical scrollbar
    Scrollx = Scrollbar(right_frame, orient=HORIZONTAL)  # Horizontal scrollbar

    # Treeview widget to display the supplier details in a table format
    treeview = ttk.Treeview(
        right_frame,
        columns=('invoice', 'name', 'contact', 'description'),
        show='headings',
        yscrollcommand=Scrolly.set,
        xscrollcommand=Scrollx.set
    )

    # Pack scrollbars to the appropriate sides
    Scrolly.pack(side=RIGHT, fill=Y)
    Scrollx.pack(side=BOTTOM, fill=X)

    # Link scrollbars to treeview
    Scrollx.config(command=treeview.xview)
    Scrolly.config(command=treeview.yview)

    # Pack treeview widget
    treeview.pack(fill=BOTH, expand=1)

    # Define column headings for the table
    treeview.heading('invoice', text='Invoice ID')
    treeview.heading('name', text='Supplier Name')
    treeview.heading('contact', text='Supplier Contact')
    treeview.heading('description', text='Description')

    # Define column widths
    treeview.column('invoice', width=80)
    treeview.column('name', width=160)
    treeview.column('contact', width=120)
    treeview.column('description', width=300)

    # Populate treeview with data from the database
    treeview_data(treeview)

    # Bind treeview row selection to populate input fields
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, invoice_entry, name_entry, contact_entry, description_text, treeview))

    return supplier_frame
