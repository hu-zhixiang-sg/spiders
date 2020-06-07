from sqlalchemy import create_engine, Column, Integer, String, DateTime, FLOAT, TEXT, TIMESTAMP, Date, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mssql+pyodbc://localhost/Spiders?driver=SQL+Server+Native+Client+11.0', echo=True)
Base = declarative_base()

class FlightSpiderTable(Base):
    __tablename__ = 'FlightSpiderTable'
    __table_args__ = {'schema': 'dbo'}

    Id = Column('Id', Integer, autoincrement=True, primary_key=True)

    date = Column('date', Date)
    moving_average = Column('moving_average', Integer)
    num_flights = Column('num_flights', Integer)

    InsertedByUser = Column('InsertedByUser', String(100))
    InsertedTimeStamp = Column('InsertedTimeStamp', DateTime)

class MaskSpiderTable(Base):
    __tablename__ = 'MaskSpiderTable'
    __table_args__ = {'schema': 'dbo'}

    Id = Column('Id', Integer, autoincrement=True, primary_key=True)

    date = Column('date', Date)
    mask_count = Column('mask_count', Integer)

    InsertedByUser = Column('InsertedByUser', String)
    InsertedTimeStamp = Column('InsertedTimeStamp', DateTime)

class UberSpiderTable(Base):
    __tablename__ = 'UberSpiderTable'
    __table_args__ = {'schema': 'dbo'}

    Id = Column('Id', Integer, autoincrement=True, primary_key=True)

    time = Column('time', DateTime)
    origin = Column('origin', String)
    destination = Column('destination', String)
    Pool = Column('Pool', FLOAT)
    UberX = Column('UberX', FLOAT)
    WAV = Column('WAV', FLOAT)

    InsertedByUser = Column('InsertedByUser', String)
    InsertedTimeStamp = Column('InsertedTimeStamp', DateTime)

Base.metadata.create_all(engine)