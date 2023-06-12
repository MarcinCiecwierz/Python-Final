# Transport Managment System
## Intro
Transport Managment System is a application that allows user to manage and track transporatation-related activities. It helps to manage orders, trucks, drivers and companies.

## Instalation
1. Clone project from repository.
2. Install packeges using command:
```
pip install -r requirements
```
**Make sure to have python installed on your machine**

## Packeges used
- Tkinter
- SQLAlchemy

## Running the application
1. Run the application by executing the 'gui.py' file.
2. After running it GUI will open.
3. There are two notebooks:
- Records
- Insert
4. In the *Record* tab, you can manage existing records.
5. Using *combobox*, you can choose between tables that are in database.
6. After choosing and clicking *Show Records* button it will display all records from chosen table.
7. After clicking on record you can either update or delete it.
- Update - It will open a new window with fields with current data of record. After changing text (or no) you can press *Update* button to update record with changes.
- Deletion - If a record is not used as a foregin key in other record it will delete chosen record and will pop up a window with proper message. But if record is used as a foregin key it will not delete it and will pop up a window with proper message.
8. In the "Insert" tab, you can insert new records into the database.
9. Choose a desired table from *combobox* and press *Select table*.
10. It will show fields with proper labels and there user can insert data.
11. After inserting correct input press *Insert data* button to insert data to database. If field is empty it will show proper message.

## Functionality

- Display Records: Select a table from the combobox menu and click "Show Records" button to display records from table.
- Delete Record: Select a record from the table and click "Delete Selected Record" button to delete record from database.
- Update Records: Select a record from the table and click "Update selected Record" button to update record.
- Select Table: Select a table from the combobox menu and click "Select Table"
- Insert Data: Fill the fields for selected table and click "Insert Data" button to add new record to database.

## Structure

- Truck: Represents a truck used for transportation.
- Driver: Represents a driver who operates the trucks.
- Company: Represents a company involved in transportation.
- Semitrailer: Represents a semitrailer attached to a truck.
- Semitruck: Represents a combination of a truck and a semitrailer and driver.
- Order: Represents a transportation order placed by a company.

## Examples

Here is examples of using Transport Managment System:

### Viewing Records

1. Select "Order" from the dropdown menu in the "Records" tab.
2. Click the "Show Records" button to display all the orders in the table.

### Updating a record 

1. Select "Order" from the dropdown menu in the "Records" tab.
2. Click the "Show Records" button to display all the orders in the table.
3. Select a record to be updated.
4. Click "Update Record" button.
5. Insert proper data in window.
6. Click "Update" button.
7. Record is updated.

## Problems faced during development

1. Making a safe deletion of a record, because if there was not safe deletion it would delete chosen record and any record that was using its id.
2. Problem while updating, proper window was opening with proper fileds, but after clicking "Update" button it will not actually update it.
3. While inserting new record, e.g In table 'Order' there are two foregins key needed. I wanted to let user choose from already existing records, but I could not find any way to make it work. So I had to leave it the way it is.