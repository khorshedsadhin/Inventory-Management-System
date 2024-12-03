from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Import the function to connect to the database
from employees import connect_database

# Function to initialize the database and table structure for categories if they do not exist
def create_database_table():
    """
    Initializes the database and table structure for categories if they do not exist.
    """
    cursor, connection = connect_database()

    # Create database if it does not exist and switch to it
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create category_data table with fields id, name, and description
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS category_data (
            id INT PRIMARY KEY,
            name VARCHAR(100),
            description TEXT
        )
    ''')

    connection.commit()
    cursor.close()
    connection.close()

# Function to delete a selected category entry from the database and refresh the view
def delete_category():
    """
    Deletes the selected category from the database after user confirmation.
    """
    # Get selected item in treeview
    selected_items = treeview.selection()
    if not selected_items:
        messagebox.showerror('Error', 'No row is selected')
        return

    for selected_item in selected_items:
        # Get the category ID from the selected row
        content = treeview.item(selected_item)
        row = content['values']
        category_id = row[0]

        # Confirmation dialog for deletion
        confirm = messagebox.askyesno('Confirm Deletion', f'Do you really want to delete the record with ID {category_id}?')
        if confirm:
            cursor, connection = connect_database()
            if not cursor or not connection:
                messagebox.showerror('Error', 'Database connection failed')
                return

            try:
                cursor.execute('USE inventory_system')
                cursor.execute('DELETE FROM category_data WHERE id=%s', (category_id,))
                connection.commit()
                messagebox.showinfo('Success', f'Category with ID {category_id} has been deleted')
                treeview_data()  # Refresh treeview to reflect changes
            except Exception as e:
                messagebox.showerror('Error', f'Error deleting record: {e}')
            finally:
                cursor.close()
                connection.close()

# Function to clear data from the input fields; optionally deselects treeview selection
def clear_fields(id_entry, category_name_entry, description_text, deselect_treeview=True):
    """
    Clears the input fields and optionally deselects any selected row in the treeview.

    Args:
        id_entry (Entry): The entry widget for Category ID.
        category_name_entry (Entry): The entry widget for Category Name.
        description_text (Text): The text widget for Description.
        deselect_treeview (bool): Whether to deselect the selected row in the treeview.
    """
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)

    if deselect_treeview:
        treeview.selection_remove(treeview.selection())  # Deselect any selected row in treeview

# Function to populate input fields when a row is selected in treeview
def select_data(event, id_entry, category_name_entry, description_text):
    """
    Populates the input fields with data from the selected row in the treeview.

    Args:
        event: The event object.
        id_entry (Entry): The entry widget for Category ID.
        category_name_entry (Entry): The entry widget for Category Name.
        description_text (Text): The text widget for Description.
    """
    selected_items = treeview.selection()
    if not selected_items:
        return

    selected_item = selected_items[0]
    content = treeview.item(selected_item)
    row = content['values']

    # Clear input fields and populate with selected row data
    clear_fields(id_entry, category_name_entry, description_text, deselect_treeview=False)
    id_entry.insert(0, row[0])
    category_name_entry.insert(0, row[1])
    description_text.insert(1.0, row[2])

# Function to retrieve and display all category records from the database in treeview
def treeview_data():
    """
    Fetches all category records from the database and populates the treeview.
    """
    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Database connection failed')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM category_data')
        records = cursor.fetchall()

        # Clear existing rows
        treeview.delete(*treeview.get_children())

        # Insert fetched records into treeview
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error fetching data: {e}')
    finally:
        cursor.close()
        connection.close()

# Function to add a new category to the database; includes validation and duplication check
def add_category(id, name, description):
    """
    Adds a new category to the database after validating inputs and checking for duplicate IDs.

    Args:
        id (str): The unique identifier for the category.
        name (str): The name of the category.
        description (str): A brief description of the category.
    """
    # Validate that all fields are filled
    if not id.strip() or not name.strip() or not description.strip():
        messagebox.showerror('Error', 'All fields are required')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Database connection failed')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM category_data WHERE id=%s', (id,))

        # Check if ID already exists in the database
        if cursor.fetchone():
            messagebox.showerror('Error', 'ID already exists')
            return

        # Insert new category data into category_data table
        cursor.execute('INSERT INTO category_data VALUES (%s, %s, %s)', (id, name, description))
        connection.commit()
        messagebox.showinfo('Success', 'Category added successfully')
        treeview_data()  # Refresh treeview to display the new category
    except Exception as e:
        messagebox.showerror('Error', f'Error inserting data: {e}')
    finally:
        cursor.close()
        connection.close()

# Function to update an existing category in the database; includes validation
def update_category(id, name, description):
    """
    Updates an existing category in the database after validating inputs.

    Args:
        id (str): The unique identifier for the category to be updated.
        name (str): The new name for the category.
        description (str): The new description for the category.
    """
    # Validate that all fields are filled
    if not id.strip() or not name.strip() or not description.strip():
        messagebox.showerror('Error', 'All fields are required for update')
        return

    cursor, connection = connect_database()
    if not cursor or not connection:
        messagebox.showerror('Error', 'Database connection failed')
        return

    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM category_data WHERE id=%s', (id,))

        # Check if the category ID exists
        if not cursor.fetchone():
            messagebox.showerror('Error', 'Category ID does not exist')
            return

        # Update the category details in the database
        cursor.execute('''
            UPDATE category_data
            SET name = %s, description = %s
            WHERE id = %s
        ''', (name, description, id))
        connection.commit()
        messagebox.showinfo('Success', 'Category updated successfully')
        treeview_data()  # Refresh treeview to display updated data
    except Exception as e:
        messagebox.showerror('Error', f'Error updating data: {e}')
    finally:
        cursor.close()
        connection.close()

# Function to build and display the category management form interface
def category_form(window):
    """
    Builds and displays the category management form interface.

    Args:
        window (Tk): The main application window.
    """
    create_database_table()  # Initialize database and table

    global back_image, logo, treeview

    # Frame to contain all category-related elements
    category_frame = Frame(window, width=1070, height=567, bg='white')
    category_frame.place(x=200, y=100)

    # Heading label for the category form
    heading_label = Label(
        category_frame,
        text='Manage Category Details',
        font=('Helvetica', 16, 'bold'),
        bg='#0F4D7D',
        fg='white'
    )
    heading_label.place(x=0, y=0, relwidth=1)

    # Back button for navigating back, with image and position
    back_image = PhotoImage(file='assets/back.png')
    back_button = Button(
        category_frame,
        image=back_image,
        bd=0,
        cursor='hand2',
        bg='white',
        command=lambda: category_frame.place_forget()
    )
    back_button.place(x=10, y=30)

    # Logo for category form
    logo = PhotoImage(file='assets/product_category.png')
    logo_label = Label(category_frame, image=logo, bg='white')
    logo_label.place(x=30, y=100)

    # Frame for the input fields
    details_frame = Frame(category_frame, bg='white')
    details_frame.place(x=500, y=60)

    # ID Label and Entry
    id_label = Label(details_frame, text='ID', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    id_entry.grid(row=0, column=1)

    # Category Name Label and Entry
    category_name_label = Label(details_frame, text='Category Name', font=('times new roman', 14, 'bold'), bg='white')
    category_name_label.grid(row=1, column=0, padx=20, sticky='w')
    category_name_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    category_name_entry.grid(row=1, column=1, pady=20)

    # Description Label and Text Area
    description_label = Label(details_frame, text='Description', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=2, column=0, padx=20, sticky='nw')
    description_text = Text(details_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=2, column=1)

    # Frame for buttons
    button_frame = Frame(category_frame, bg='white')
    button_frame.place(x=580, y=280)

    # Add Button
    add_button = Button(
        button_frame,
        text='Add',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: add_category(id_entry.get(), category_name_entry.get(), description_text.get(1.0, END).strip())
    )
    add_button.grid(row=0, column=0, padx=10)

    # Update Button
    update_button = Button(
        button_frame,
        text='Update',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: update_category(id_entry.get(), category_name_entry.get(), description_text.get(1.0, END).strip())
    )
    update_button.grid(row=0, column=1, padx=10)

    # Delete Button
    delete_button = Button(
        button_frame,
        text='Delete',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=delete_category
    )
    delete_button.grid(row=0, column=2, padx=10)

    # Clear Button
    clear_button = Button(
        button_frame,
        text='Clear',
        font=('times new roman', 14),
        width=8,
        cursor='hand2',
        fg='white',
        bg='#0F4D7D',
        command=lambda: clear_fields(id_entry, category_name_entry, description_text)
    )
    clear_button.grid(row=0, column=3, padx=10)

    # Frame for treeview (data table)
    treeview_frame = Frame(category_frame, bg='yellow')
    treeview_frame.place(x=530, y=340, height=200, width=500)

    # Scrollbars for treeview
    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    # Treeview widget to display category details
    treeview = ttk.Treeview(
        treeview_frame,
        columns=('id', 'name', 'description'),
        show='headings',
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set
    )
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    # Define treeview column headings and widths
    treeview.heading('id', text='ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')
    treeview.column('id', width=80, anchor='center')
    treeview.column('name', width=140, anchor='center')
    treeview.column('description', width=300, anchor='center')

    # Populate treeview with data from the database
    treeview_data()

    # Bind treeview row selection to populate input fields
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, id_entry, category_name_entry, description_text))

    return category_frame
