from tkinter import *
from tkinter import ttk

# Function to create the supplier form UI
def supplier_form(window):

   global back_image  # Declare back_image as a global variable to avoid it being garbage collected

   # Create the main frame for the supplier form
   supplier_frame = Frame(window, width=1070, height=567, bg='white')
   supplier_frame.place(x=200, y=100)

   # Create a heading label for the supplier section
   heading_label = Label(supplier_frame, text='Manage Supplier Details', font=('times new roman', 16, 'bold'), bg='#0F4D7D', fg='white')
   heading_label.place(x=0, y=0, relwidth=1)  # relwidth=1 ensures the label spans the width of the frame

   # Back button to exit the supplier form
   back_image = PhotoImage(file='assets/back.png')  # Load back button image
   back_button = Button(supplier_frame, image=back_image, bd=0, cursor='hand2', bg='white', command= lambda: supplier_frame.place_forget())
   back_button.place(x=10, y=30)  # Position the back button

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
   add_button = Button(button_frame, text='Add', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   add_button.grid(row=0, column=0, padx=20)

   # Update Button
   update_button = Button(button_frame, text='Update', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   update_button.grid(row=0, column=1)

   # Delete Button
   delete_button = Button(button_frame, text='Delete', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   delete_button.grid(row=0, column=2, padx=20)

   # Clear Button
   clear_button = Button(button_frame, text='Clear', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   clear_button.grid(row=0, column=3)

   # ------ Right Frame for Supplier Data Display (Table) ------ #
   right_frame = Frame(supplier_frame, bg='white')
   right_frame.place(x=520, y=95, width=500, height=345)

   # Search Section in the Right Frame
   search_frame = Frame(right_frame, bg='white')
   search_frame.pack(pady=(0, 20))  # Add some padding at the bottom

   # Invoice No Label and Search Entry field
   num_label = Label(search_frame, text='Invoice NO .', font=('times new roman', 14, 'bold'), bg='white')
   num_label.grid(row=0, column=0, padx=15, sticky='w')
   search_entry = Entry(search_frame, font=('times new roman', 14, 'bold'), bg='lightyellow', width=15)
   search_entry.grid(row=0, column=1)

   # Search Button
   search_button = Button(search_frame, text='Search', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   search_button.grid(row=0, column=2, padx=15)

   # Show All Button
   show_button = Button(search_frame, text='Show All', font=('times new roman', 14), width=8, cursor='hand2', fg='white', bg='#0F4D7D')
   show_button.grid(row=0, column=3)

   # ------ Treeview (Table) to Display Supplier Information ------ #
   Scrolly = Scrollbar(right_frame, orient=VERTICAL)  # Vertical scrollbar
   Scrollx = Scrollbar(right_frame, orient=HORIZONTAL)  # Horizontal scrollbar

   # Treeview widget to display the supplier details in a table format
   treeview = ttk.Treeview(right_frame, column=('invoice', 'name', 'contact', 'description'), show='headings', yscrollcommand=Scrolly.set, xscrollcommand=Scrollx.set)

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
