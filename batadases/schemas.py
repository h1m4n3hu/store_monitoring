from pydantic import BaseModel

class BQresults(BaseModel):
    store_id: int
    timezone_str: str
    class Config:
        orm_mode = True

class MenuHours(BaseModel):
    store_id: int
    day: int
    start_time_local: str
    end_time_local: str
    class Config:
        orm_mode = True

class StoreStatus(BaseModel):
    store_id: int
    status: str
    tiimestamp_utc: str
    class Config:
        orm_mode = True
