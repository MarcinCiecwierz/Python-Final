import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Company, Driver, Order, Semitrailer, Semitruck, Truck, create_tables
import os

database_url = 'sqlite:///mydatabase.db'

#Initialize database
def initialize_database(database_url):
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

#Selec query
def perform_select(session, table_model):
    #Join tables for Semitruck and Order
    if table_model == Semitruck:
        query = session.query(Semitruck.Id, Truck.Registration, Semitrailer.Registration, Driver.Name) \
            .join(Truck) \
            .join(Semitrailer) \
            .join(Driver)
    elif table_model == Order:
        query = session.query(Order.Id, Order.Semitruck_Id, Company.Name, Order.From, Order.To, Order.DateFrom, Order.DateTo, Order.Distance, Order.Money, Order.WeightOrder) \
            .join(Order.Semitruck) \
            .join(Order.Company)
    else:
        query = session.query(table_model)
    results = query.all()
    return results

#Insert query
def insert_data(session, table_model, **args):
    new_record = table_model(**args)
    session.add(new_record)
    session.commit()

#Update Query
def update_record(session, record, **update_values):
    for key, value in update_values.items():
        setattr(record, key, value)
    session.commit()

#Seeding
def create_tables_with_seeding():
    create_tables()

    truck_args = {
        'Model': 'ABC',
        'Registration': 'XYZ123',
        'Weight': 5000.0,
        'InsuranceDate': datetime.date(2024, 5, 10),
        'ReviewDate': datetime.date(2024, 5, 10)
    }
    insert_data(session, Truck, **truck_args)

    semitrailer_args = {
        'Model': 'DEF',
        'Registration': 'UVW456',
        'Weight': 7000.0,
        'InsuranceDate': datetime.date(2024, 5, 10),
        'ReviewDate': datetime.date(2024, 5, 10)
    }
    insert_data(session, Semitrailer, **semitrailer_args)

    driver_args = {
        'Name': 'John',
        'LastName': 'Doe',
        'PESEL': '123456789',
        'Address': 'Jana Pawla 2',
        'PhoneNumber': '1234567890'
    }
    insert_data(session, Driver, **driver_args)

    company_args = {
        'Name': 'DeliveryCompanyJ&K',
        'NIP': '1234567890'
    }
    insert_data(session, Company, **company_args)

    semitruck_args = {
        'MaxWeight': 40000.0,
        'Truck_Id': 1,
        'Semitrailer_Id': 1,
        'Driver_Id': 1
    }
    insert_data(session, Semitruck, **semitruck_args)

    order_args = {
        'Semitruck_Id': 1,
        'Company_Id': 1,
        'From': 'Warsaw',
        'To': 'Berlin',
        'DateFrom': datetime.date(2023, 5, 20),
        'DateTo': datetime.date(2023, 5, 21),
        'Distance': 400.0,
        'Money': 1000.0,
        'WeightOrder': 5000.0
    }
    insert_data(session, Order, **order_args)

    session.close()


session, engine = initialize_database(database_url)

#Create database if mydatabase.db does not exist
database_file = "mydatabase.db"
if not os.path.exists(database_file):
    create_tables_with_seeding()
    print("Created data base with sample data.")

session.close()
engine.dispose()
