lection
    return [logoImage, employee_icon, supplier_icon, category_icon, products_icon, sales_icon, exit_icon]

def create_menu_button(frame, icon, text, callback):
    """Creates a menu button inside the given frame."""
    button = Button(frame, image=icon, compound=LEFT, text=text, font=('times new roman', 20, 'bold'),
                    anchor='w', padx=10, command=callback)
    button.pack(fill=X)
