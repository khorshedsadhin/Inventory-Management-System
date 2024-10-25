from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# import from another python file
from employees import connect_database

# Function to initialize the database and table structure for categories if they do not exist
def create_database_table():
    cursor, connection = connect_database()

    # Create database if it does not exist and switch to it
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create category_data table with fields id, name, and description
    cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, name VARCHAR(100), description TEXT)')

# Function to delete a selected category entry from the database and refresh the view
def delete_category():
    index = treeview.selection()  # Get selected item in treeview
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return

    content = treeview.item(index)
    row = content['values']
    id = row[0]  # Get category ID from selected row

    # Confirmation dialog for deletion
    result = messagebox.askyesno('Confirm', 'Do you really want to delete the record')
    if result:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_system')
            cursor.execute('DELETE FROM category_data WHERE id=%s', (id,))  # Delete category by ID
            connection.commit()
            treeview_data()  # Refresh treeview
            messagebox.showinfo('Info', 'Record is deleted')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

# Function to clear data from the input fields; optionally deselects treeview selection
def clear(id_entry, category_name_entry, description_text, deselect_treeview):
    id_entry.delete(0, END)
    category_name_entry.delete(0, END)
    description_text.delete(1.0, END)

    if deselect_treeview:
        treeview.selection_remove(treeview.selection())  # Deselect any selected row in treeview

# Function to populate input fields when a row is selected in treeview
def select_data(event, id_entry, category_name_entry, description_text):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']

    # Clear input fields and populate with selected row data
    clear(id_entry, category_name_entry, description_text, False)
    id_entry.insert(0, row[0])
    category_name_entry.insert(0, row[1])
    description_text.insert(1.0, row[2])

# Function to retrieve and display all category records from the database in treeview
def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM category_data')
        records = cursor.fetchall()

        # Clear existing rows and repopulate treeview with fetched records
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

# Function to add a new category to the database; includes validation and duplication check
def add_category(id, name, description):
    if id == '' or name == '' or description == '':
        messagebox.showerror('Error', 'All Fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
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
            messagebox.showinfo('Info', 'Data is inserted')
            treeview_data()  # Refresh treeview
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

# Function to build and display the category management form interface
def category_form(window):
    create_database_table()  # Initialize database and table

    global back_image, logo, treeview

    # Frame to contain all category-related elements
    category_frame = Frame(window, width=1070, height=567, bg='white')
    category_frame.place(x=200, y=100)

    # Heading label for the category form
    heading_label = Label(category_frame, text='Manage Category Details', font=('times new roman', 16, 'bold'), bg='#0F4D7D', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # Back button for navigating back, with image and position
    back_image = PhotoImage(file='assets/back.png')
    back_button = Button(category_frame, image=back_image, bd=0, cursor='hand2', bg='white', command=lambda: category_frame.place_forget())
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
    add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D',
                        command=lambda: add_category(id_entry.get(), category_name_entry.get(), description_text.get(1.0, END).strip()))
    add_button.grid(row=0, column=0, padx=20)

    # Delete Button
    delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D', command=delete_category)
    delete_button.grid(row=0, column=1, padx=20)

    # Clear Button
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D',
                          command=lambda: clear(id_entry, category_name_entry, description_text, True))
    clear_button.grid(row=0, column=2, padx=20)

    # Frame for treeview (data table)
    treeview_frame = Frame(category_frame, bg='yellow')
    treeview_frame.place(x=530, y=340, height=200, width=500)

    # Scrollbars for treeview
    Scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    Scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    # Treeview widget to display category details
    treeview = ttk.Treeview(treeview_frame, columns=('id', 'name', 'description'), show='headings', yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)
    Scrolly.pack(side=RIGHT, fill=Y)
    Scrollx.pack(side=BOTTOM, fill=X)
    Scrollx.config(command=treeview.xview)
    Scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    # Define treeview column headings and widths
    treeview.heading('id', text='ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')
    treeview.column('id', width=80)
    treeview.column('name', width=140)
    treeview.column('description', width=300)

    # Populate treeview with data from the database
    treeview_data()

    # Bind treeview row selection to populate input fields
    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, id_entry, category_name_entry, description_text))
