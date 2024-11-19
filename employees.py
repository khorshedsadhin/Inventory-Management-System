import re  # to check validation
from tkinter import *
from tkinter import ttk  # for combobox
from tkinter import messagebox
from datetime import date  # to access today's date (clear_fields)
from tkcalendar import DateEntry  # terminal: pip install tkcalendar
import pymysql  # terminal: pip install pymysql


def connect_database():
    # Function to establish a connection to the MySQL database
    try:
        connection = pymysql.connect(host='localhost', user='root', password='1234')
        cursor = connection.cursor()
    except:
        # Show an error message if there's an issue connecting to the database
        messagebox.showerror('Error', 'Database connectivity issue, open mysql command line client')
        return None, None

    return cursor, connection


def create_database_table():
    # Function to create a database and a table for employee data if they don't exist
    cursor, connection = connect_database()

    # Create database and use it
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create the employee_data table if it doesn't already exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee_data (
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
                      )''')


def treeview_data():
    # Function to fetch all data from the employee_data table and populate the Treeview widget
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_system')

    try:
        # Fetch all employee records
        cursor.execute('SELECT * from employee_data')
        employee_records = cursor.fetchall()

        # Clear the Treeview before adding new data
        treeview.delete(*treeview.get_children())

        # Insert fetched records into the Treeview
        for record in employee_records:
            treeview.insert('', END, values=record)

    except Exception as e:
        # Show error message in case of any issue
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        # Close the database connection
        cursor.close()
        connection.close()


def select_data(event, empId_entry, name_entry, email_entry, gender_combobox, contact_entry,
                education_combobox, address_text, doj_date_entry,
                salary_entry, usertype_combobox, password_entry):

    # Function to select a row from Treeview and fill the form fields with its data
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']

    # Clear previous data from the form fields
    clear_fields(empId_entry, name_entry, email_entry, gender_combobox, contact_entry,
                 education_combobox, address_text, doj_date_entry,
                 salary_entry, usertype_combobox, password_entry, False)

    # Fill form fields with the selected row data
    empId_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])

    # Check if contact number has a leading "0" and add it if missing
    contact_number = str(row[4])
    if not contact_number.startswith("0"):
        contact_number = "0" + contact_number

    contact_entry.insert(0, contact_number)

    education_combobox.set(row[5])
    address_text.insert(1.0, row[6])
    doj_date_entry.set_date(row[7])
    salary_entry.insert(0, row[8])
    usertype_combobox.set(row[9])
    password_entry.insert(0, row[10])


def add_employee(empid, name, email, gender, contact, education, address, doj, salary, user_type, password):
    # Function to add a new employee record into the employee_data table

    # Check if all fields are filled
    if (empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == ''
        or education == 'Select Education' or address == '\n' or salary == ''
        or user_type == 'Select User Type' or password == ''):

        # Show error message if any field is empty
        messagebox.showerror('Error', 'All fields are required')
        return

    # Contact validation: 11 digits, starts with "01", third digit 3-9, other 8 can be any digit
    if not re.fullmatch(r"01[3-9]\d{8}", contact):
        messagebox.showerror('Error', 'Invalid contact number!')
        return

    # Gmail validation: contains "@gmail.com", all lowercase
    if not re.fullmatch(r"[a-z0-9._%+-]+@gmail\.com", email):
        messagebox.showerror('Error', 'Email must be a valid Gmail address!')
        return

    # Salary validation: must be a positive integer
    if not re.fullmatch(r"\d+", salary):
        messagebox.showerror('Error', 'Salary must be a valid integer number!')
        return

    # Password validation: at least 4 characters
    if not re.fullmatch(r".{4,}", password):
        messagebox.showerror('Error', 'Password must be at least 4 characters long!')
        return

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_system')
    try:
        address = address.strip()  # to not add \n at the end of the data

        # Insert the new employee record into the employee_data table
        cursor.execute('''INSERT INTO employee_data (empid, name, email, gender, contact,
                          education, address, doj, salary, usertype, password)
                          VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                       (empid, name, email, gender, contact, education, address, doj, salary, user_type, password))
        connection.commit()  # Commit the transaction

        # Refresh the Treeview with the new data
        treeview_data()

        # Show success message
        messagebox.showinfo('Success', 'Data is inserted successfully')

    except Exception as e:
        # Show error message in case of any issue
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        # Close the database connection
        cursor.close()
        connection.close()


def clear_fields(empId_entry, name_entry, email_entry, gender_combobox,
                 contact_entry, education_combobox, address_text, doj_date_entry,
                 salary_entry, usertype_combobox, password_entry, check):

    # Function to clear all input fields in the form

    empId_entry.delete(0, END)  # Clear Employee ID field
    name_entry.delete(0, END)  # Clear Name field
    email_entry.delete(0, END)  # Clear Email field

    gender_combobox.set('Select Gender')  # Reset Gender combobox
    contact_entry.delete(0, END)  # Clear Contact field
    education_combobox.set('Select Education')  # Reset Education combobox
    address_text.delete(1.0, END)  # Clear Address text box (from 1st row and 1st character)

    doj_date_entry.set_date(date.today())  # Reset DOJ to today's date

    salary_entry.delete(0, END)  # Clear Salary field
    usertype_combobox.set('Select User Type')  # Reset User Type combobox
    password_entry.delete(0, END)  # Clear Password field

    if check:
        treeview.selection_remove(treeview.selection())  # Remove any row selection in Treeview


def update_employee(empid, name, email, gender, contact, education, address, doj, salary, user_type, password):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')
        return

    # Contact validation: 11 digits, starts with "01", third digit 3-9, other 8 can be any digit
    if not re.fullmatch(r"01[3-9]\d{8}", contact):
        messagebox.showerror('Error', 'Invalid contact number!')
        return

    # Gmail validation: contains "@gmail.com", all lowercase
    if not re.fullmatch(r"[a-z0-9._%+-]+@gmail\.com", email):
        messagebox.showerror('Error', 'Email must be a valid Gmail address!')
        return

    # Salary validation: must be a positive integer
    if not re.fullmatch(r"\d+", salary):
        messagebox.showerror('Error', 'Salary must be a valid integer number!')
        return

    # Password validation: at least 4 characters
    if not re.fullmatch(r".{4,}", password):
        messagebox.showerror('Error', 'Password must be at least 4 characters long!')
        return

    # Connect to the database
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    try:
        cursor.execute('USE inventory_system')

        # Select the row which is going to be updated (check if update is needed or not)
        cursor.execute('SELECT * FROM employee_data WHERE empid=%s', (empid,))
        current_data = cursor.fetchone()
        current_data = current_data[1:]  # excluding empid (primary key) to compare

        address = address.strip()

        new_data = (name, email, gender, contact, education, address, doj, salary, user_type, password)

        if current_data == new_data:
            messagebox.showinfo('Information', 'No changes detected')
            return

        # Update Database
        cursor.execute('''UPDATE employee_data SET name=%s, email=%s, gender=%s, contact=%s,
                          education=%s, address=%s, doj=%s, salary=%s, usertype=%s, password=%s
                          WHERE empid=%s''',
                       (name, email, gender, contact, education, address, doj, salary, user_type, password, empid))
        connection.commit()
        treeview_data()
        messagebox.showinfo('Success', 'Data is updated successfully')

    except Exception as e:
        # Show error message in case of any issue
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        # Close the database connection
        cursor.close()
        connection.close()


def delete_employee(empid):
    selected = treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'No row is selected')

    else:
        result = messagebox.askyesno('Confirm', 'Do you really want to delete the record')

        if result:
            # Connect to the database
            cursor, connection = connect_database()
            if not cursor or not connection:
                return

            try:
                cursor.execute('USE inventory_system')
                cursor.execute('DELETE FROM employee_data where empid=%s', (empid,))
                connection.commit()
                treeview_data()
                messagebox.showinfo('Success', 'Record is deleted')

            except Exception as e:
                # Show error message in case of any issue
                messagebox.showerror('Error', f'Error due to {e}')

            finally:
                # Close the database connection
                cursor.close()
                connection.close()


def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'No option is selected')

    elif value == '':
        messagebox.showerror('Error', 'Enter the value to search')

    else:
        search_option = search_option.replace(' ', '_')

        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        try:
            cursor.execute('USE inventory_system')
            cursor.execute(f'SELECT * from employee_data WHERE {search_option} LIKE %s', f'%{value}%')
            records = cursor.fetchall()

            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert('', END, value=record)

        except Exception as e:
            # Show error message in case of any issue
            messagebox.showerror('Error', f'Error due to {e}')

        finally:
            # Close the database connection
            cursor.close()
            connection.close()


def show_all(search_combobox, search_entry):
    treeview_data()
    search_combobox.set('Search By')
    search_entry.delete(0, END)


def employee_form(window):
    # Function to display the Employee Management form
    create_database_table()

    # Create a frame for the employee form
    global back_image, treeview
    employee_frame = Frame(window, width=1070, height=567, bg='white')
    employee_frame.place(x=200, y=100)

    # Create a heading label for the employee management section
    heading_label = Label(employee_frame, text='Manage Employee Details', font=('times new roman', 16, 'bold'), bg='#0F4D7D', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)

    # Top frame for search options
    top_frame = Frame(employee_frame, bg='white')
    top_frame.place(x=0, y=40, relwidth=1, height=235)

    # Back button to exit the employee form
    back_image = PhotoImage(file='assets/back.png')
    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white', command=lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)

    # Search frame for search criteria and buttons
    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()

    # Combobox for selecting search criteria
    search_combobox = ttk.Combobox(search_frame, values=('EmpId', 'Name', 'Email', 'Gender'), font=('times new roman', 12), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)

    # Entry field to input search query
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)

    # Search button
    search_button = Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                           command=lambda: search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)

    # Show All button to display all employees
    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                         command=lambda: show_all(search_combobox, search_entry))
    show_button.grid(row=0, column=3)

    # Horizontal and vertical scrollbars for the treeview (employee table)
    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)

    # Treeview to display employee data in table form
    treeview = ttk.Treeview(top_frame, columns=('empId', 'name', 'email', 'gender', 'contact',
                                                'education', 'address', 'doj', 'salary', 'usertype'),
                            show='headings', yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    # Configuring the scrollbar behavior for the treeview
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10, 0))

    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    # Packing the treeview
    treeview.pack(pady=(10, 0))

    # Defining columns and their headings in the treeview
    treeview.heading('empId', text='EmpId')
    treeview.heading('name', text='Name')
    treeview.heading('email', text='Email')
    treeview.heading('gender', text='Gender')
    treeview.heading('contact', text='Contact')
    treeview.heading('education', text='Education')
    treeview.heading('address', text='Address')
    treeview.heading('doj', text='Date of Joining')
    treeview.heading('salary', text='Salary')
    treeview.heading('usertype', text='User Type')

    # Setting the width of each column
    treeview.column('empId', width=60)
    treeview.column('name', width=140)
    treeview.column('email', width=180)
    treeview.column('gender', width=80)
    treeview.column('contact', width=100)
    treeview.column('education', width=120)
    treeview.column('address', width=200)
    treeview.column('doj', width=100)
    treeview.column('salary', width=140)
    treeview.column('usertype', width=120)

    treeview_data()  # show all the employees information in mysql

    # Frame to hold employee details form (input fields)
    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    # Labels and Entry fields for employee details
    empId_label = Label(detail_frame, text='EmpId', font=('times new roman', 12), bg='white')
    empId_label.grid(row=0, column=0, padx=20, pady=10, sticky='w')
    empId_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    empId_entry.grid(row=0, column=1, padx=20, pady=10)

    name_label = Label(detail_frame, text='Name', font=('times new roman', 12), bg='white')
    name_label.grid(row=0, column=2, padx=20, pady=10, sticky='w')
    name_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    name_entry.grid(row=0, column=3, padx=20, pady=10)

    email_label = Label(detail_frame, text='Email', font=('times new roman', 12), bg='white')
    email_label.grid(row=0, column=4, padx=20, pady=10, sticky='w')
    email_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    email_entry.grid(row=0, column=5, padx=20, pady=10)

    gender_label = Label(detail_frame, text='Gender', font=('times new roman', 12), bg='white')
    gender_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')

    # Combobox for selecting gender
    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female'), font=('times new roman', 12), width=18, state='readonly')
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=1, column=1)

    contact_label = Label(detail_frame, text='Contact', font=('times new roman', 12), bg='white')
    contact_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=3, padx=20, pady=10)

    # Education selection
    education_label = Label(detail_frame, text='Education', font=('times new roman', 12), bg='white')
    education_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')

    education_options = ["B.Tech", "B.Com", "M.Tech", "M.Com", "B.Sc", "M.Sc", "BBA", "MBA", "LLB", "LLM", "B.Arch", "M.Arch"]
    education_combobox = ttk.Combobox(detail_frame, values=education_options, font=('times new roman', 12), width=18, state='readonly')
    education_combobox.set('Select Education')
    education_combobox.grid(row=2, column=1)

    # Address entry (multiline text widget)
    address_label = Label(detail_frame, text='Address', font=('times new roman', 12), bg='white')
    address_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('times new roman', 12), bg='lightyellow')
    address_text.grid(row=2, column=3, rowspan=2)

    # Date of Joining entry
    doj_label = Label(detail_frame, text='Date of Joining', font=('times new roman', 12), bg='white')
    doj_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly', date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=1)

    # Salary entry
    salary_label = Label(detail_frame, text='Salary', font=('times new roman', 12), bg='white')
    salary_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    salary_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    salary_entry.grid(row=1, column=5, padx=20, pady=10)

    # User Type selection
    usertype_label = Label(detail_frame, text='User Type', font=('times new roman', 12), bg='white')
    usertype_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')
    usertype_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('times new roman', 12), width=18, state='readonly')
    usertype_combobox.set('Select User Type')
    usertype_combobox.grid(row=2, column=5)

    # Password entry for user creation
    password_label = Label(detail_frame, text='Password', font=('times new roman', 12), bg='white')
    password_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')

    # Set the 'show' parameter to '*' to mask the input
    password_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow', show='*')
    password_entry.grid(row=3, column=5, padx=20, pady=10)

    # Add a hint label below the password entry field
    password_hint_label = Label(detail_frame, text='must be at least 4 characters',
                                font=('times new roman', 10), fg='grey', bg='white')
    password_hint_label.grid(row=4, column=5, padx=20, sticky='w')


    # Frame for Add, Update, Delete, and Clear buttons
    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=520)

    # Add Button
    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                        command=lambda: add_employee(empId_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
                                                     contact_entry.get(), education_combobox.get(), address_text.get(1.0, END),
                                                     doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    # Update Button
    update_button = Button(button_frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                           command=lambda: update_employee(empId_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
                                                           contact_entry.get(), education_combobox.get(), address_text.get(1.0, END),
                                                           doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    update_button.grid(row=0, column=1, padx=20)

    # Delete Button
    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                           command=lambda: delete_employee(empId_entry.get()))
    delete_button.grid(row=0, column=2, padx=20)

    # Clear Button to reset the form
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D',
                          command=lambda: clear_fields(empId_entry, name_entry, email_entry, gender_combobox,
                                                       contact_entry, education_combobox, address_text, doj_date_entry,
                                                       salary_entry, usertype_combobox, password_entry, True))
    clear_button.grid(row=0, column=3, padx=20)

    treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, empId_entry, name_entry, email_entry, gender_combobox, contact_entry,
                                                                 education_combobox, address_text, doj_date_entry,
                                                                 salary_entry, usertype_combobox, password_entry))  # left click any row select_data function will be called for that
    return employee_frame
