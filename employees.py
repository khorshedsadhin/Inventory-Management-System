from tkinter import *
from tkinter import ttk # for combobox
from tkinter import messagebox
from datetime import date # to access todays date (clear_fields)
from tkcalendar import DateEntry # terminal: pip install tkcalendar
import pymysql # terminal: pip install pymysql


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
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data (empid INT PRIMARY KEY, name VARCHAR(100), '
                   'email VARCHAR(100), gender VARCHAR(50), dob VARCHAR(30), contact VARCHAR(30), education VARCHAR(30),'
                   'employement_type VARCHAR(50), work_shift VARCHAR(50), address VARCHAR(100), doj VARCHAR(30), '
                   'salary VARCHAR(50), usertype VARCHAR(50), password VARCHAR(50))')


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



def select_data(event, empId_entry, name_entry, email_entry, dob_date_entry, gender_combobox, contact_entry,
                employement_type_combobox, education_combobox, work_shift_combobox, address_text, doj_date_entry,
                salary_entry, usertype_combobox, password_entry):

    # Function to select a row from Treeview and fill the form fields with its data
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']

    # Clear previous data from the form fields
    clear_fields(empId_entry, name_entry, email_entry, dob_date_entry, gender_combobox, contact_entry,
                 employement_type_combobox, education_combobox, work_shift_combobox, address_text, doj_date_entry,
                 salary_entry, usertype_combobox, password_entry)

    # Fill form fields with the selected row data
    empId_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_date_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    employement_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    address_text.insert(1.0, row[9])
    doj_date_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    usertype_combobox.set(row[12])
    password_entry.insert(0, row[13])



def add_employee(empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, user_type, password):
    # Function to add a new employee record into the employee_data table

    # Check if all fields are filled
    if (empid == '' or name == '' or email == '' or gender == 'Select Gender' or contact == ''
        or employement_type == 'Select Type' or education == 'Select Education' or work_shift == 'Select Work Shift'
        or address == '\n' or salary == '' or user_type == 'Select User Type' or password == ''):

        # Show error message if any field is empty
        messagebox.showerror('Error', 'All fields are required')

    else:
        # Connect to the database
        cursor, connection = connect_database()
        if not cursor or not connection:
            return

        cursor.execute('USE inventory_system')
        try:
            # Insert the new employee record into the employee_data table
            cursor.execute('INSERT INTO employee_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                           (empid, name, email, gender, dob, contact, employement_type, education, work_shift, address, doj, salary, user_type, password))
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



def clear_fields(empId_entry, name_entry, email_entry, dob_date_entry, gender_combobox,
                 contact_entry, employement_type_combobox, education_combobox, work_shift_combobox,
                 address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry):

    # Function to clear all input fields in the form

    empId_entry.delete(0, END)  # Clear Employee ID field
    name_entry.delete(0, END)  # Clear Name field
    email_entry.delete(0, END)  # Clear Email field

    dob_date_entry.set_date(date.today())  # Reset DOB to today's date

    gender_combobox.set('Select Gender')  # Reset Gender combobox
    contact_entry.delete(0, END)  # Clear Contact field
    employement_type_combobox.set('Select Type')  # Reset Employment Type combobox
    education_combobox.set('Select Education')  # Reset Education combobox
    work_shift_combobox.set('Select Work Shift')  # Reset Work Shift combobox
    address_text.delete(1.0, END)  # Clear Address text box (from 1st row and 1st character)

    doj_date_entry.set_date(date.today())  # Reset DOJ to today's date

    salary_entry.delete(0, END)  # Clear Salary field
    usertype_combobox.set('Select User Type')  # Reset User Type combobox
    password_entry.delete(0, END)  # Clear Password field

    treeview.selection_remove(treeview.selection())  # Remove any row selection in Treeview



def employee_form(window):
    # Function to display the Employee Management form

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
    back_button = Button(top_frame, image=back_image, bd=0, cursor='hand2', bg='white', command= lambda: employee_frame.place_forget())
    back_button.place(x=10, y=0)

    # Search frame for search criteria and buttons
    search_frame = Frame(top_frame, bg='white')
    search_frame.pack()

    # Combobox for selecting search criteria (Id, Name, Email)
    search_combobox =  ttk.Combobox(search_frame, values=('Id', 'Name', 'Email'), font=('times new roman', 12), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)

    # Entry field to input search query
    search_entry = Entry(search_frame, font=('times new roman', 12), bg='lightyellow')
    search_entry.grid(row=0, column=1)

    # Search button
    search_button = Button(search_frame, text='Search', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    search_button.grid(row=0, column=2, padx=20)

    # Show All button to display all employees
    show_button = Button(search_frame, text='Show All', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    show_button.grid(row=0, column=3)

    # Horizontal and vertical scrollbars for the treeview (employee table)
    horizontal_scrollbar = Scrollbar(top_frame, orient=HORIZONTAL)
    vertical_scrollbar = Scrollbar(top_frame, orient=VERTICAL)

    # Treeview to display employee data in table form
    treeview = ttk.Treeview(top_frame, columns=('empId', 'name', 'email', 'gender', 'dob', 'contact', 'employement_type',
                                                'education', 'work_shift', 'address', 'doj', 'salary', 'usertype'), show='headings',
                                                yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

    # Configuring the scrollbar behavior for the treeview
    horizontal_scrollbar.pack(side=BOTTOM, fill=X)
    vertical_scrollbar.pack(side=RIGHT, fill=Y, pady=(10,0))

    horizontal_scrollbar.config(command=treeview.xview)
    vertical_scrollbar.config(command=treeview.yview)

    # Packing the treeview
    treeview.pack(pady=(10,0))

    # Defining columns and their headings in the treeview
    treeview.heading('empId', text='EmpId')
    treeview.heading('name', text='Name')
    treeview.heading('email', text='Email')
    treeview.heading('gender', text='Gender')
    treeview.heading('dob', text='Date of Birth')
    treeview.heading('contact', text='Contact')
    treeview.heading('employement_type', text='Employement Type')
    treeview.heading('education', text='Education')
    treeview.heading('work_shift', text='Work Shift')
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
    treeview.column('dob', width=100)
    treeview.column('employement_type', width=120)
    treeview.column('education', width=120)
    treeview.column('work_shift', width=100)
    treeview.column('address', width=200)
    treeview.column('doj', width=100)
    treeview.column('salary', width=140)
    treeview.column('usertype', width=120)

    treeview_data() # show all the employees information in mysql

    # Frame to hold employee details form (input fields)
    detail_frame = Frame(employee_frame, bg='white')
    detail_frame.place(x=20, y=280)

    # Labels and Entry fields for employee details (e.g., EmpId, Name, Email, etc.)
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

    dob_label = Label(detail_frame, text='Date of Birth', font=('times new roman', 12), bg='white')
    dob_label.grid(row=1, column=2, padx=20, pady=10, sticky='w')

    # DateEntry widget for selecting the Date of Birth
    dob_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly', date_pattern='dd/mm/yyyy')
    dob_date_entry.grid(row=1, column=3)

    contact_label = Label(detail_frame, text='Contact', font=('times new roman', 12), bg='white')
    contact_label.grid(row=1, column=4, padx=20, pady=10, sticky='w')
    contact_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    contact_entry.grid(row=1, column=5, padx=20, pady=10)

    # Employment Type selection
    employement_type_label = Label(detail_frame, text='Employement Type', font=('times new roman', 12), bg='white')
    employement_type_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
    employement_type_combobox = ttk.Combobox(detail_frame, values=('Full Time', 'Part Time', 'Casual', 'Contract', 'Intern'), font=('times new roman', 12), width=18, state='readonly')
    employement_type_combobox.set('Select Type')
    employement_type_combobox.grid(row=2, column=1)

    # Education selection
    education_label = Label(detail_frame, text='Education', font=('times new roman', 12), bg='white')
    education_label.grid(row=2, column=2, padx=20, pady=10, sticky='w')

    education_options = ["B.Tech", "B.Com", "M.Tech", "M.Com", "B.Sc", "M.Sc", "BBA", "MBA", "LLB", "LLM", "B.Arch", "M.Arch"]
    education_combobox = ttk.Combobox(detail_frame, values=education_options, font=('times new roman', 12), width=18, state='readonly')
    education_combobox.set('Select Education')
    education_combobox.grid(row=2, column=3)

    # Work shift selection
    work_shift_label = Label(detail_frame, text='Work Shift', font=('times new roman', 12), bg='white')
    work_shift_label.grid(row=2, column=4, padx=20, pady=10, sticky='w')
    work_shift_combobox = ttk.Combobox(detail_frame, values=('Morning', 'Evening', 'Night'), font=('times new roman', 12), width=18, state='readonly')
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=2, column=5)

    # Address entry (multiline text widget)
    address_label = Label(detail_frame, text='Address', font=('times new roman', 12), bg='white')
    address_label.grid(row=3, column=0, padx=20, pady=10, sticky='w')
    address_text = Text(detail_frame, width=20, height=3, font=('times new roman', 12), bg='lightyellow')
    address_text.grid(row=3, column=1, rowspan=2)

    # Date of Joining entry
    doj_label = Label(detail_frame, text='Date of Joining', font=('times new roman', 12), bg='white')
    doj_label.grid(row=3, column=2, padx=20, pady=10, sticky='w')
    doj_date_entry = DateEntry(detail_frame, width=18, font=('times new roman', 12), state='readonly', date_pattern='dd/mm/yyyy')
    doj_date_entry.grid(row=3, column=3)

    # User Type selection
    usertype_label = Label(detail_frame, text='User Type', font=('times new roman', 12), bg='white')
    usertype_label.grid(row=4, column=2, padx=20, pady=10, sticky='w')
    usertype_combobox = ttk.Combobox(detail_frame, values=('Admin', 'Employee'), font=('times new roman', 12), width=18, state='readonly')
    usertype_combobox.set('Select User Type')
    usertype_combobox.grid(row=4, column=3)

    # Salary entry
    salary_label = Label(detail_frame, text='Salary', font=('times new roman', 12), bg='white')
    salary_label.grid(row=3, column=4, padx=20, pady=10, sticky='w')
    salary_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    salary_entry.grid(row=3, column=5, padx=20, pady=10)

    # Password entry for user creation
    password_label = Label(detail_frame, text='Password', font=('times new roman', 12), bg='white')
    password_label.grid(row=4, column=4, padx=20, pady=10, sticky='w')
    password_entry = Entry(detail_frame, font=('times new roman', 12), bg='lightyellow')
    password_entry.grid(row=4, column=5, padx=20, pady=10)

    # Frame for Add, Update, Delete, and Clear buttons
    button_frame = Frame(employee_frame, bg='white')
    button_frame.place(x=200, y=520)

    # Add Button
    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D', command=lambda: add_employee(empId_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
                                                                                                                                                                 dob_date_entry.get(), contact_entry.get(), employement_type_combobox.get(),
                                                                                                                                                                 education_combobox.get(), work_shift_combobox.get(), address_text.get(1.0, END),
                                                                                                                                                                 doj_date_entry.get(), salary_entry.get(), usertype_combobox.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)

    # Update Button
    update_button = Button(button_frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    update_button.grid(row=0, column=1, padx=20)

    # Delete Button
    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    delete_button.grid(row=0, column=2, padx=20)

    # Clear Button to reset the form
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D', command= lambda: clear_fields(empId_entry, name_entry, email_entry, dob_date_entry, gender_combobox,
                                                                                                                                                                      contact_entry, employement_type_combobox, education_combobox, work_shift_combobox,
                                                                                                                                                                      address_text, doj_date_entry, salary_entry, usertype_combobox, password_entry))
    clear_button.grid(row=0, column=3, padx=20)

    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event, empId_entry, name_entry, email_entry, dob_date_entry, gender_combobox,contact_entry,
                                                    employement_type_combobox, education_combobox, work_shift_combobox,address_text, doj_date_entry,
                                                    salary_entry, usertype_combobox, password_entry)) # left click any row select_data function will be called for that
    create_database_table()
