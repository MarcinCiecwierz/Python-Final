from tkinter import LEFT, Entry, OptionMenu, StringVar, Tk, Label, messagebox
from tkinter.ttk import Treeview, Button, Combobox, Notebook, Frame
from database import Truck, Order, Driver, Semitrailer, Semitruck, Company
from queries import initialize_database, insert_data, perform_select, update_record
from database import type_mapping
from tkcalendar import DateEntry
import datetime


database_url = 'sqlite:///mydatabase.db'

session, engine = initialize_database(database_url)

#Set window
root = Tk()
root.title('Transport')
root.geometry("1000x500")

#Add Notebook
n = Notebook(root)
n.pack(fill="both", expand=True)


record_types = [Order, Truck, Driver, Semitrailer, Semitruck, Company]


#Function to show records
def show_records(table_model):
    results = perform_select(session, table_model)
    #Clear any existing data in tree widget
    tree.delete(*tree.get_children())
    #Change columns name for Semitruck and Order
    if table_model == Semitruck:
        columns = ("ID", "Truck Registration", "Semitrailer Registration", "Driver Name")
    elif table_model == Order:
        columns = ("Id", "Semitruck_Id", "Company", "From", "To", "DateFrom", "DateTo", "Distance", "Money", "WeightOrder")
    else:
        #Other tables
        columns = tuple(table_model.__table__.columns.keys())
        #Set columns of the tree
    tree["columns"] = columns
    #Headings for each column
    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)
        #Insert data into tree widget
    for result in results:
        #Convert for Semitruck and Order
        if table_model in [Semitruck, Order]:
            values = [str(value) for value in result]
        #Convert so strings with spaces will work
        else:
            values = [str(getattr(result, attr)) for attr in columns]
        #Insert values to tree
        tree.insert("", "end", values=values)


def show_records_from_combobox():
    #Get selected table from combobox
    selected_type = combo_box_select.get()

    if selected_type:
        #Find the corresponding record type from the record_types list
        record_type = next((rt for rt in record_types if rt.__name__ == selected_type), None)
        #Call show records on chosen table
        if record_type:
            show_records(record_type)


def get_referenced_tables(selected_type, record_id):
    referenced_by = []
    #Iterate over each table
    for rt in record_types:
        #Iterate over each column in table
        for column in rt.__table__.columns:
            #Check if column has foregin key
            if column.foreign_keys:
                #Get foregin key of column
                foreign_key = list(column.foreign_keys)[0]
                #Check if the table of foregin key match selected table
                if foreign_key.column.table == selected_type.__table__:
                    #Select referencing records by its id
                    referencing_records = session.query(rt).filter(column == record_id).all()
                    #If referencing record exist, add the name of referencing table to list
                    if referencing_records:
                        referenced_by.append(rt.__name__)
    return referenced_by


def delete_selected_record():
    selected_item = tree.focus()
    if selected_item:
        #Get values of selected item
        values = tree.item(selected_item)['values']
        #Get id
        record_id = values[0]
        #Find selected record type based on combobox
        selected_type = next((rt for rt in record_types if rt.__name__ == combo_box_select.get()), None)
        #Check if a valid record type is found
        if selected_type:
            #Select record with given record ID
            record = session.query(selected_type).get(record_id)
            #Check if record actually exists
            if record:
                #Get referencing tables for record
                referenced_by = get_referenced_tables(selected_type, record_id)
                #Check if the record is referenced by other table
                if referenced_by:
                    messagebox.showerror("Error", f"Record is referenced by {', '.join(referenced_by)}")
                else:
                    #Delete and commit changes
                    session.delete(record)
                    session.commit()
                    messagebox.showinfo("Success", "Record deleted successfully")
                    show_records(selected_type)
            else:
                messagebox.showerror("Error", "Record not found")
        else:
            messagebox.showerror("Error", "Invalid table selected")
    else:
        messagebox.showwarning("Warning", "No record selected")


def update_selected_record():
    selected_item = tree.focus()
    #Check if item is selected
    if selected_item:
        #get values from selected item
        values = tree.item(selected_item)['values']
        #Get id
        record_id = values[0]
        #Find selected record type based on combobox
        selected_type = next((rt for rt in record_types if rt.__name__ == combo_box_select.get()), None)
        #Check if a valid record type is found
        if selected_type:
            #Select record with given record ID
            record = session.query(selected_type).get(record_id)
            #Check if record actually exists
            if record:
                #Create window
                update_window = Tk()
                update_window.title("Update Record")
                update_window.geometry("300x400")
                entry_wid = {}
                label_wid = {}
                #Create labels and entry widgets for each column
                for i, column in enumerate(selected_type.__table__.columns):
                    if column.primary_key:
                        continue
                    label = Label(update_window, text=column.name)
                    label.pack(side="top")
                    label_wid[column.name] = label
                    entry = Entry(update_window)
                    entry.pack(side="top")
                    entry.insert(0, str(getattr(record, column.name)))
                    entry_wid[column.name] = entry

                def update():
                    #Dictionary with new values
                    update_values = {}
                    #Iterate over each column and entry
                    for column, entry in entry_wid.items():
                        #Get tet entered in entry widget
                        text = entry.get()
                        #Check if text is empty
                        if text == "":
                            messagebox.showerror("Error", f"{column} can't be empty")
                            return
                        #Change column type for date columns
                        if column in ['DateFrom', 'DateTo', 'InsuranceDate', 'ReviewDate']:
                            x = text.split('-')
                            d_obj = datetime.date(int(x[0]), int(x[1]), int(x[2]))
                            print(column, ":", text)
                            update_values[column] = d_obj
                        else:
                            print(column, ":", text)
                            update_values[column] = text
                    #Update record
                    update_record(session, record, **update_values)
                    messagebox.showinfo("Success", "Record updated successfully")
                    #Close update window
                    update_window.destroy()
                    #Refresh gui window with updated record
                    show_records(selected_type)
            
                #Add button
                update_button = Button(update_window, text="Update", command=update)
                update_button.pack(side="top")

                update_window.mainloop()
            else:
                messagebox.showerror("Error", "Record not found")
        else:
            messagebox.showerror("Error", "Invalid table selected")
    else:
        messagebox.showwarning("Warning", "No record selected")


f1 = Frame(n)
n.add(f1, text="Records")


tree = Treeview(f1, show="headings")
tree.pack()


combo_box_select = Combobox(f1, values=[rt.__name__ for rt in record_types], width=12)
combo_box_select.pack()


combo_box_select.set('Order')
show_records_from_combobox()


button = Button(f1, text="Show Records", command=show_records_from_combobox)
button.pack()


button_delete_record = Button(f1, text="Delete Selected Record", command=delete_selected_record)
button_delete_record.pack()


button_update_record = Button(f1, text="Update Selected Recod", command=update_selected_record)
button_update_record.pack()


f2 = Frame(n)
n.add(f2, text="Insert")


entry_wid = {}
label_wid = {}


def destroy_widgets():
    for entry in entry_wid.values():
        entry.destroy()
    for label in label_wid.values():
        label.destroy()

    entry_wid.clear()
    label_wid.clear()


selected_type = None


def chosen_type():
    #Declare as global type
    global selected_type
    #Destroy any existing labels and entry widgets
    destroy_widgets()
    #Get selected type from combobox
    type_name = combo_box_insert.get()
    selected_type = type_name
    #Check if type name is in mapping from database
    if type_name in type_mapping:
        #Update selected type to corresponding type
        selected_type = type_mapping[type_name]
        #Iterate over columns of selected type's table
        for column in selected_type.__table__.columns:
            #Skip pk
            if column.primary_key:
                continue
            #Create different Entry widget for date input
            if column.name in ['DateFrom', 'DateTo', 'InsuranceDate', 'ReviewDate']:
                label = Label(f2, text=column.name)
                label.pack(side="top")
                label_wid[column.name] = label
                date_entry = DateEntry(f2, date_pattern="yyyy-mm-dd")
                date_entry.pack(side="top")
                entry_wid[column.name] = date_entry
            #Create Entry widget
            else:
                label = Label(f2, text=column.name)
                label.pack(side="top")
                label_wid[column.name] = label
                entry = Entry(f2)
                entry.pack(side="top")
                entry_wid[column.name] = entry


def insert():
    insert_values = {}
    #Iterate over each column and entry
    for column, entry in entry_wid.items():
        #Get text entered
        text = entry.get()
        #If text is empty
        if text == "":
            messagebox.showerror("Error", f"{column} can't be empty")
            return
        #Change column type for date columns
        if column in ['DateFrom', 'DateTo', 'InsuranceDate', 'ReviewDate']:
            x = text.split('-')
            d_obj = datetime.date(int(x[0]), int(x[1]), int(x[2]))
            print(column, ":", text)
            insert_values[column] = d_obj
        else:
            print(column, ":", text)
            insert_values[column] = text
    insert_data(session, selected_type, **insert_values)
    messagebox.showinfo("Success", "Record inserted successfully")


combo_box_insert = Combobox(f2, values=[rt.__name__ for rt in record_types], width=12)
combo_box_insert.pack()


button1 = Button(f2, text="Select Table", command=chosen_type)
button1.pack()


print_button = Button(f2, text="Insert Data", command=insert)
print_button.pack()


root.mainloop()
