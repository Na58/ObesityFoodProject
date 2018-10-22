from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from sqlalchemy import ForeignKey
import json


Base = declarative_base()

# Database Schema for Obesity
class Obesity(Base):
    __tablename__ = 'obesity'
    pha = Column(Integer, ForeignKey('pha.pha_code'), primary_key=True)
    child_obesity = Column(Float)
    child_obesity_f = Column(Float)
    child_obesity_m = Column(Float)
    adult_obesity = Column(Float)
    adult_obesity_f = Column(Float)
    adult_obesity_m = Column(Float)

# Database Schema for PHA
class PHA(Base):
    __tablename__ = 'pha'
    pha_code = Column(Integer, primary_key=True)
    pha_name = Column(String)
    coor = Column(String)

# Database for ABR
class ABR(Base):
    __tablename__ = 'abr'
    abn = Column(Integer, primary_key=True)
    coor = Column(String)
    pha_code = Column(Integer, ForeignKey('pha.pha_code'))

# Write to PHAWriter
class PHAWriter:
    def __init__(self, fname='../ProcessedData/phn_result.json'):
        self.data_pool = json.load(open(fname))

    def enter_record(self, session):
        record = list()
        for data in self.data_pool.items():
            record.append(Obesity(pha=int(data[0]),
                                  child_obesity=data[1]['child'], child_obesity_f=data[1]['female_child'],
                                  child_obesity_m=data[1]['male_child'], adult_obesity=data[1]['adult'],
                                  adult_obesity_f=data[1]['female_adult'], adult_obesity_m=data[1]['male_adult']))
        self.write_to_db(record, session)

    def write_to_db(self, record, session):
        session.add_all(record)
        session.commit()

# Write PHA Geographical Information
class PHAGEOWriter:
    def __init__(self, fname='../ProcessedData/PHA_GEO.json'):
        self.data_pool = json.load(open(fname))

    def enter_record(self, session):
        record = list()
        for data in self.data_pool.items():
            record.append(PHA(pha_code=int(data[0]), pha_name=str(data[1]['pha_name']), coor=str(data[1]['coor'])))
        self.write_to_db(record, session)

    def write_to_db(self, record, session):
        session.add_all(record)
        session.commit()

# Write to ABR Table
class ABRWriter:
    def __init__(self, fname='../ProcessedData/abr.json'):
        self.data_pool = json.load(open(fname))

    def enter_record(self, session):
        record = list()
        for data in self.data_pool.items():
            record.append(ABR(abn=int(data[0]), pha_code=int(data[1]['pha_code']), coor=str(data[1]['coor'])))
        self.write_to_db(record, session)

    def write_to_db(self, record, session):
        session.add_all(record)
        session.commit()

# Create database
class DBCreater:

    @staticmethod
    def create_database():
        configs = {
            'drivername': 'sqlite',
            # 'username': '',
            # 'password': '',
            # 'host': '',
            # 'port': '',
            # 'database': 'pikachu_w_abr_v1.db',
            'database': 'pikachu.db',
            # 'query': '',
        }

        engine = create_engine(URL(**configs), echo=True)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()

        Base.metadata.create_all(engine)

        pha_writer = PHAWriter()
        pha_writer.enter_record(session)

        geo_writer = PHAGEOWriter()
        geo_writer.enter_record(session)

        # abr_writer = ABRWriter()
        abr_writer = ABRWriter(fname='../ProcessedData/abr_V1.json')
        abr_writer.enter_record(session)

if __name__ == '__main__':

    DBCreater.create_database()












