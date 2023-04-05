from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from batadases import models, schemas
from batadases.db import SessionLocal, engine
from databases import Database

from typing import List
from datetime import datetime


models.Base.metadata.create_all(bind=engine)
database = Database('sqlite:///csvdb.db')
database.connect()

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def main():
    return RedirectResponse(url="/docs/")

def mediandate(d1,d2):
    return d1+(d2-d1)/2

def shifted(tim,dat):
    k=str(dat)
    tim=k[:11]+tim+'.000000'
    return datetime.strptime(tim, '%Y-%m-%d %H:%M:%S.%f')

def modified(id,menu_hrs,arr):
    res=[]
    for dat,actv in arr:
        if not res:
            start="00:00:00"
            res.append([shifted(start,dat),dat,actv])
        else:
            if res[-1][1].date()==dat.date():
                if res[-1][2]==actv:
                    res[-1][1]=dat
                else:
                    middle=mediandate(res[-1][1],dat)
                    res[-1][1]=middle
                    res.append([middle,dat,actv])
            else:
                end="23:59:59"
                res[-1][1]=shifted(end,res[-1][1])
                start="00:00:00"
                res.append([shifted(start,dat),dat,actv])
    return res

@app.get("/trigger_report/")
async def trigger(db: Session = Depends(get_db)):
    q="""select * from store_status;"""
    rows=await database.fetch_all(query=q)
    rows.sort(key=lambda x:x[2])
    q="""select * from menu_hours;"""
    menu_hrs_list=await database.fetch_all(query=q)
    menu_hrs={}
    for item in menu_hrs_list:
        try:menu_hrs[item["store_id"]].append([item["day"],item["start_time_local"],item["end_time_local"]])
        except:menu_hrs[item["store_id"]]=[[item["day"],item["start_time_local"],item["end_time_local"]]]

    stat={}
    for i in rows:stat[i[0]]=[]
    for stor,statu,tim in rows:
        try:
            dtobj=datetime.strptime(tim[:-4], '%Y-%m-%d %H:%M:%S.%f')
            stat[stor].append([dtobj,statu])
        except:
            pass
    for stor in stat:
        stat[stor]=modified(stor,menu_hrs,stat[stor])
    # return stat


    q="""select max(timestamp_utc) from store_status"""
    maxtime=await database.fetch_all(query=q)
    maxtime=datetime.strptime(maxtime[0][0][:-4], '%Y-%m-%d %H:%M:%S.%f')
    import csv
    fields=['store_id','uptime_last_hour','uptime_last_day','update_last_week','downtime_last_hour','downtime_last_day','downtime_last_week']
    filename='result.csv'
    rows=[]
    for store in stat:
        hr,dae,wik=0,0,0
        for s,e,v in stat[store][::-1]:
            if ((maxtime-s).total_seconds())<3600:
                hr=((maxtime-s).total_seconds())/60
            if ((maxtime-s).total_seconds())<86400:
                dae=((maxtime-s).total_seconds())/3600
            if ((maxtime-s).total_seconds())<604800:
                wik=((maxtime-s).total_seconds())/3600
        _hr,_dae,_wik=60-hr,24-dae,(24*7)-wik
        # print(_hr,_dae,_wik)
        rows.append([store,hr,dae,wik,_hr,_dae,_wik])

    
    with open(filename, 'w') as csvfile: 
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)
    return "generated"

@app.get("/get_report/")
async def reporter(db: Session = Depends(get_db)):
    return {}