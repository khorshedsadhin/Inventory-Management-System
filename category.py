from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# import from another python file
from employees import connect_database

def create_database_table():
    # Function to create a database and a table for employee data if they don't exist
    cursor, connection = connect_database()

    # Create database and use it
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')

    # Create the employee_data table if it doesn't already exist
    cursor.execute('CREATE TABLE IF NOT EXISTS category_data (id INT PRIMARY KEY, name VARCHAR(100), description TEXT)')

def delete_category():

    index =treeview.selection()
    content=treeview.item(index)
    row=content['values']
    id=row[0]
    if not index:
        messagebox.showerror('Error', 'No row is selected')
        return
    else:
        result = messagebox.askyesno('Confirm', 'Do you really want to delete the record')

        if result:
            cursor, connection =connect_database()
            if not cursor or not connection:
                return

            try:
                cursor.execute('use inventory_system')
                cursor.execute('DELETE FROM category_data WHERE id=%s',id)
                connection.commit()
                treeview_data()
                messagebox.showinfo('Info', 'Record is deleted')
            except Exception as e:
                messagebox.showerror('Error',f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()



def clear(id_entry, category_name_entry, description_text, check):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)

    if check:
        treeview.selection_remove(treeview.selection())

def select_data(event, id_entry, category_name_entry, description_text):
    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']

    clear(id_entry, category_name_entry, description_text, False)

    id_entry.insert(0,row[0])
    category_name_entry.insert(0,row[1])
    description_text.insert(1.0,row[2])

def treeview_data():
    cursor, connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('use inventory_system')
        cursor.execute('Select * from category_data')
        records =cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')

    finally:
        cursor.close()
        connection.close()

def add_category(id, name, description):
    if id=='' or name=='' or description=='':
        messagebox.showerror('Error', 'All Fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:

            cursor.execute('use inventory_system')

            cursor.execute('SELECT * from category_data WHERE id=%s', id)
            if cursor.fetchone():
                messagebox.showerror('Error', 'Id already exists')
                return
            cursor.execute('INSERT INTO category_data VALUES(%s, %s, %s)', (id, name, description))
            connection.commit()
            messagebox.showinfo('Info', 'Data is inserted')
            treeview_data()

        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')

        finally:
            cursor.close()
            connection.close()


def category_form(window):
    create_database_table()

    global back_image,logo,treeview
    category_frame = Frame(window, width=1070, height=567, bg='white')
    category_frame.place(x=200, y=100)

    heading_label = Label(category_frame, text='Manage Category Details', font=('times new roman', 16, 'bold'), bg='#0F4D7D', fg='white')
    heading_label.place(x=0, y=0, relwidth=1)  # relwidth=1 ensures the label spans the width of the frame

    back_image = PhotoImage(file='assets/back.png')  # Load back button image
    back_button = Button(category_frame, image=back_image, bd=0, cursor='hand2', bg='white',
                         command= lambda: category_frame.place_forget())
    back_button.place(x=10, y=30)  # Position the back button

    logo=PhotoImage(file='assets/product_category.png')
    label=Label (category_frame, image=logo, bg='white')
    label.place(x=30, y=100)

    details_frame=Frame(category_frame, bg= 'white')
    details_frame.place(x=500, y=60)

    id_label = Label(details_frame, text='Id', font=('times new roman', 14, 'bold'), bg='white')
    id_label.grid(row=0, column=0, padx=20, sticky='w')
    id_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    id_entry.grid(row=0, column=1)

    category_name_label = Label(details_frame, text='Category Name', font=('times new roman', 14, 'bold'), bg='white')
    category_name_label.grid(row=1, column=0, padx=20, sticky='w')
    category_name_entry = Entry(details_frame, font=('times new roman', 14, 'bold'), bg='lightyellow')
    category_name_entry.grid(row=1, column=1, pady=20)


    description_label = Label(details_frame, text='Desceiption', font=('times new roman', 14, 'bold'), bg='white')
    description_label.grid(row=2, column=0, padx=20, sticky='nw')

    description_text = Text(details_frame, width=25, height=6, bd=2, bg='lightyellow')
    description_text.grid(row=2, column=1)

    button_frame=Frame(category_frame, bg= 'white')
    button_frame.place(x=580, y=280)


    add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2',
                         fg='white', bg='#0F4D7D', command=lambda : add_category(id_entry.get(), category_name_entry.get(),description_text.get(1.0,END).strip()))
    add_button.grid(row=0, column=0, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2',
                            fg='white', bg='#0F4D7D', command=lambda :delete_category ())
    delete_button.grid(row=0, column=1, padx=20)

    clear_button = Button(button_frame, text='clear', font=('times new roman', 14), width=8, cursor='hand2',
                          fg='white', bg='#0F4D7D', command=lambda :clear(id_entry, category_name_entry, description_text, True) )
    clear_button.grid(row=0, column=2, padx=20)



    treeview_frame=Frame(category_frame, bg= 'yellow')
    treeview_frame.place(x=530, y=340, height=200, width=500)

    Scrolly = Scrollbar(treeview_frame, orient=VERTICAL)  # Vertical scrollbar
    Scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)  # Horizontal scrollbar

    # Treeview widget to display the supplier details in a table format
    treeview = ttk.Treeview(treeview_frame, column=('id','name', 'description'), show='headings',
                             yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)

    # Pack scrollbars to the appropriate sides
    Scrolly.pack(side=RIGHT, fill=Y)
    Scrollx.pack(side=BOTTOM, fill=X)

    # Link scrollbars to treeview
    Scrollx.config(command=treeview.xview)
    Scrolly.config(command=treeview.yview)

    # Pack treeview widget
    treeview.pack(fill=BOTH, expand=1)

    # Define column headings for the table
    treeview.heading('id', text='ID')
    treeview.heading('name', text='Category Name')
    treeview.heading('description', text='Description')

    treeview.column('id', width=80)
    treeview.column('name', width=140)
    treeview.column('description', width=300)
    treeview_data()

    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event, id_entry, category_name_entry, description_text)) # left click any row select_data function will be called for that
