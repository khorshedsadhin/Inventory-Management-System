from tkinter import *
from tkinter import ttk # for combobox
from tkcalendar import DateEntry # terminal: pip install tkcalendar

# Functionality Part
def employee_form(window):
    # Function to display the Employee Management form

    # Create a frame for the employee form
    global back_image
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
    add_button = Button(button_frame, text='Add', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    add_button.grid(row=0, column=0, padx=20)

    # Update Button
    update_button = Button(button_frame, text='Update', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    update_button.grid(row=0, column=1, padx=20)

    # Delete Button
    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    delete_button.grid(row=0, column=2, padx=20)

    # Clear Button to reset the form
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12), width=10, cursor='hand2', fg='white', bg='#0F4D7D')
    clear_button.grid(row=0, column=3, padx=20)


# GUI Part
#object of Tk class is needed to create window
window = Tk()

window.title('Dashboard')
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position to center the window
x_cordinate = int((screen_width/2) - (1270/2))
y_cordinate = int((screen_height/2) - (668/2))

window.geometry(f"1270x668+{x_cordinate}+{y_cordinate}") # {x_cordinate}+{y_cordinate} means window will appear in center(which we calculated)
window.resizable(0,0) #disable maximize button
window.config(bg='white')

bg_image =  PhotoImage(file='assets/inventory.png')
#compound makes image and title show at the same time
titleLabel = Label(window, image=bg_image, compound=LEFT, text='  Inventory Management System',
                   font=('times new roman' , 40, 'bold'), bg='#010c48', fg='white', anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1) #where the title will appear,  without .place titleLabel won't be shown

logoutButton = Button(window, text='Logout', font=('times new roman', 20, 'bold'), fg='#010c48')
logoutButton.place(x=1100, y=10)

subtitleLabel = Label(window, text='Welcome Admin\t\t Date: 08-07-2024\t\t Time: 12:36:17 pm', font=('times new roman', 15), bg='#4d636d', fg='white')
subtitleLabel.place(x=0, y=70, relwidth=1)

leftFrame = Frame(window)
leftFrame.place(x=10, y=102, width=200, height=555)

logoImage = PhotoImage(file='assets/logo.png')
imageLabel = Label(leftFrame, image=logoImage)
imageLabel.pack()

menuLabel = Label(leftFrame, text='Menu', font=('times new roman', 20), bg='#009688')
menuLabel.pack(fill=X)

employee_icon = PhotoImage(file='assets/employee.png')
employee_button = Button(leftFrame,image=employee_icon, compound=LEFT, text=' Employees', font=('times new roman', 20, 'bold'), anchor='w', padx=10, command= lambda: employee_form(window))
employee_button.pack(fill=X)

supplier_icon = PhotoImage(file='assets/supplier.png')
supplier_button = Button(leftFrame,image=supplier_icon, compound=LEFT, text=' Suppliers', font=('times new roman', 20, 'bold'),anchor='w', padx=10)
supplier_button.pack(fill=X)

category_icon = PhotoImage(file='assets/category.png')
category_button = Button(leftFrame,image=category_icon, compound=LEFT, text=' Categories', font=('times new roman', 20, 'bold'),anchor='w', padx=10)
category_button.pack(fill=X)

products_icon = PhotoImage(file='assets/product.png')
products_button = Button(leftFrame,image=products_icon, compound=LEFT, text=' Products', font=('times new roman', 20, 'bold'),anchor='w', padx=10)
products_button.pack(fill=X)

sales_icon = PhotoImage(file='assets/sales.png')
sales_button = Button(leftFrame,image=sales_icon, compound=LEFT, text=' Sales', font=('times new roman', 20, 'bold'),anchor='w', padx=10)
sales_button.pack(fill=X)

exit_icon = PhotoImage(file='assets/exit.png')
exit_button = Button(leftFrame,image=exit_icon, compound=LEFT, text=' Exit', font=('times new roman', 20, 'bold'),anchor='w', padx=10)
exit_button.pack(fill=X)

emp_frame = Frame(window, bg='#2C3E50', bd=3,relief=RIDGE)
emp_frame.place(x=400, y=125, height=170, width=280)
total_emp_icon = PhotoImage(file='assets/total_emp.png')
total_emp_icon_label = Label(emp_frame, image=total_emp_icon, bg='#2C3E50')
total_emp_icon_label.pack(pady=10)

total_emp_label = Label(emp_frame, text='Total Employees', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold'))
total_emp_label.pack()

total_emp_count_label = Label(emp_frame, text='0', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold'))
total_emp_count_label.pack()

sup_frame = Frame(window, bg='#8E44AD', bd=3,relief=RIDGE)
sup_frame.place(x=800, y=125, height=170, width=280)
total_sup_icon = PhotoImage(file='assets/total_sup.png')
total_sup_icon_label = Label(sup_frame, image=total_sup_icon, bg='#8E44AD')
total_sup_icon_label.pack(pady=10)

total_sup_label = Label(sup_frame, text='Total Suppliers', bg='#8E44AD', fg='white', font=('times new roman', 15, 'bold'))
total_sup_label.pack()

total_sup_count_label= Label(sup_frame, text='0', bg='#8E44AD', fg='white', font=('times new roman', 30, 'bold'))
total_sup_count_label.pack()

cat_frame = Frame(window, bg='#27AE60', bd=3,relief=RIDGE)
cat_frame.place(x=400, y=310, height=170, width=280)
total_cat_icon = PhotoImage(file='assets/total_cat.png')
total_cat_icon_label = Label(cat_frame, image=total_cat_icon, bg='#27AE60')
total_cat_icon_label.pack(pady=10)

total_cat_label = Label(cat_frame, text='Total Categories', bg='#27AE60', fg='white', font=('times new roman', 15, 'bold'))
total_cat_label.pack()

total_cat_count_label= Label(cat_frame, text='0', bg='#27AE60', fg='white', font=('times new roman', 30, 'bold'))
total_cat_count_label.pack()

prod_frame = Frame(window, bg='#2C3E50', bd=3,relief=RIDGE)
prod_frame.place(x=800, y=310, height=170, width=280)
total_prod_icon = PhotoImage(file='assets/total_prod.png')
total_prod_icon_label = Label(prod_frame, image=total_prod_icon, bg='#2C3E50')
total_prod_icon_label.pack(pady=10)

total_prod_label = Label(prod_frame, text='Total Products', bg='#2C3E50', fg='white', font=('times new roman', 15, 'bold'))
total_prod_label.pack()

total_prod_count_label= Label(prod_frame, text='0', bg='#2C3E50', fg='white', font=('times new roman', 30, 'bold'))
total_prod_count_label.pack()

sales_frame = Frame(window, bg='#E74C3C', bd=3,relief=RIDGE)
sales_frame.place(x=600, y=495, height=170, width=280)
total_sales_icon = PhotoImage(file='assets/total_sales.png')
total_sales_icon_label = Label(sales_frame, image=total_sales_icon, bg='#E74C3C')
total_sales_icon_label.pack(pady=10)

total_sales_label = Label(sales_frame, text='Total Sales', bg='#E74C3C', fg='white', font=('times new roman', 15, 'bold'))
total_sales_label.pack()

total_sales_count_label = Label(sales_frame, text='0', bg='#E74C3C', fg='white', font=('times new roman', 30, 'bold'))
total_sales_count_label.pack()

window.mainloop() #show window
