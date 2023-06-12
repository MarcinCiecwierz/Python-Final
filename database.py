from sqlalchemy import Column, Date, Double, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create table
def create_tables():
    database_url = 'sqlite:///mydatabase.db'
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)
    session.commit()

Base = declarative_base()

# Tables in database
class Truck(Base):
    __tablename__ = 'Truck'
    Id = Column(Integer, primary_key=True)
    Model = Column(String(50), nullable=False)
    Registration = Column(String(10), nullable=False)
    Weight = Column(Double, nullable=False)
    InsuranceDate = Column(Date, nullable=False)
    ReviewDate = Column(Date, nullable=False)
    def __str__(self):
        return f"{self.Id} {self.Model} {self.Registration} {self.Weight} {self.InsuranceDate} {self.ReviewDate}"


class Semitrailer(Base):
    __tablename__ = 'Semitrailer'
    Id = Column(Integer, primary_key=True)
    Model = Column(String(50), nullable=False)
    Registration = Column(String(10), nullable=False)
    Weight = Column(Double, nullable=False)
    InsuranceDate = Column(Date, nullable=False)
    ReviewDate = Column(Date, nullable=False)
    def __str__(self):
        return f"{self.Id} {self.Model} {self.Registration} {self.Weight} {self.InsuranceDate} {self.ReviewDate}"


class Driver(Base):
    __tablename__ = 'Driver'
    Id = Column(Integer, primary_key=True)
    Name = Column(String(50), nullable=False)
    LastName = Column(String(50), nullable=False)
    PESEL = Column(String(15), nullable=False)
    Address = Column(String(50), nullable=False)
    PhoneNumber = Column(String(10), nullable=False)

    def __str__(self):
        return f"{self.Id} {self.Name} {self.LastName} {self.PESEL} {self.Address} {self.PhoneNumber}"

class Company(Base):
    __tablename__ = 'Company'
    Id = Column(Integer, primary_key=True)
    Name = Column(String(50), nullable=False)
    NIP = Column(String(50), nullable=False)

    def __str__(self):
        return f"{self.Id} {self.Name} {self.NIP}"


class Semitruck(Base):
    __tablename__ = 'Semitruck'
    Id = Column(Integer, primary_key=True)
    MaxWeight = Column(Double, nullable=False)
    Truck_Id = Column(Integer, ForeignKey('Truck.Id'), nullable=False)
    Semitrailer_Id = Column(Integer, ForeignKey('Semitrailer.Id'), nullable=False)
    Driver_Id = Column(Integer, ForeignKey('Driver.Id'), nullable=False)
    Truck = relationship("Truck")
    Semitrailer = relationship("Semitrailer")
    Driver = relationship("Driver")

    def __str__(self):
        return f"{self.Id}{self.MaxWeight}{self.Truck_Id}{self.Semitrailer_Id} {self.Driver_Id}"

class Order(Base):
    __tablename__ = 'Order'
    Id = Column(Integer, primary_key=True)
    Semitruck_Id = Column(Integer, ForeignKey('Semitruck.Id', ondelete="RESTRICT"),nullable=False)
    Company_Id = Column(Integer, ForeignKey('Company.Id', ondelete="RESTRICT"), nullable=False)
    From = Column(String(50), nullable=False)
    To = Column(String(50), nullable=False)
    DateFrom = Column(Date, nullable=False)
    DateTo = Column(Date, nullable=False)
    Distance = Column(Double, nullable=False)
    Money = Column(Double, nullable=False)
    WeightOrder = Column(Double, nullable=False)
    Company = relationship("Company")
    Semitruck = relationship("Semitruck")

    def __str__(self):
        return f"{self.Id} {self.Semitruck_Id} {self.Company_Id} {self.From} {self.To} {self.DateFrom} {self.DateTo} {self.Distance} {self.Money} {self.WeightOrder}"

#Mapping for other implementation
type_mapping = {
    'Order': Order,
    'Truck' : Truck,
    'Driver' : Driver,
    'Semitrailer' : Semitrailer,
    "Semitruck" : Semitruck,
    'Company' : Company
}