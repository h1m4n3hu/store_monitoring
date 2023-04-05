from sqlalchemy import Column, Integer, String
from .db import Base


class BQresults(Base):
    __tablename__ = "bq_results"
    store_id = Column(Integer, primary_key=True)
    timezone_str = Column(String)

class MenuHours(Base):
    __tablename__ = "menu_hours"
    store_id = Column(Integer, primary_key=True)
    day = Column(Integer)
    start_time_local = Column(String)
    end_time_local = Column(String)

class StoreStatus(Base):
    __tablename__ = "store_status"
    store_id = Column(Integer, primary_key=True)
    status = Column(String)
    timestamp_utc = Column(String)
