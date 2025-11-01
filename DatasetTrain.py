import pandas as pd 
import random
from datetime import datetime,timedelta
import numpy as np
station_tiers={
    "Dadar":1,"Andheri":1,"Bandra":1,"Borivali":1,
    "Malad":2,"Kandivali":2,"Churchgate":2,"Virar":2,
    "Mumbai Central":3,"Grant Road":3,"Charni Road":3,"Marine Lines":3,
    "Jogeshwari":4,"Dahisar":4
}

stations=list(station_tiers.keys())
directions=["Northbound","Southbound"]
days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Friday"]
def generate_passenger_count(hour,station,day_of_week):
    tier=station_tiers.get(station,3)
    if tier==1:
        base=random.randint(300,450)
    elif tier==2:
        base=random.randint(220,350)
    elif tier==3:
        base=random.randint(120,250)
    else:
        base=random.randint(60,160)
    if 7<=hour<=10:
        peak_boost=random.randint(350,700)
    elif 17<=hour<=21:
        peak_boost=random.randint(300,700)
    else:
        peak_boost=0
#Station Speicific
    if station in ["Dadar","Andheri","Bandra","Borivali"]:
        station_extra=random.randint(100,300)
    elif station in ["Malad","Kandivali","Virar","Churchgate"]:
        station_extra=random.randint(50,200)
    else:
        station_extra=random.randint(0,80)
#Weekend dip (Saturday less dip than Sunday)
    weekend_modifier=0
    if day_of_week =="Saturday":
        weekend_modifier=-random.randint(30,120)
    elif day_of_week=="Sunday":
        weekend_modifier=-random.randint(100,220)
 #Noise addition   
    daily_noise=int(np.random.normal(0,30))
    raw=base+peak_boost+station_extra + weekend_modifier+daily_noise
    multiplicative_noise=raw*random.uniform(-0.08,0.08)
    count=int(round(raw+multiplicative_noise))

    count=max(10,count)
    count=min(count,1000)
    return count
#Generate dataset
def generate_dataset(num_records=3000,start_date=datetime(2025,10,1),days_span=30):
    records=[]
    for _ in range(num_records):
        offset_days=random.randint(0,max(0,days_span-1))
        rand_date=start_date+timedelta(days=offset_days)
        hour=random.randint(4,23)
        minute=random.choice([0,5,10,15,20,30,40,45,50])
        timestamp=datetime(rand_date.year,rand_date.month,rand_date.day,hour,minute)
        day_of_week=timestamp.strftime("%A")
        station=random.choice(stations)
        direction=random.choice(directions)
        passengar_count=generate_passenger_count(hour,station,day_of_week)
        is_peak=1 if (7<=hour<=10 or 17<=hour<=21) else 0

        records.append({
            "timestamp":timestamp,
            "date":timestamp.date().isoformat(),
            "day_of_week":day_of_week,
            "hour":hour,
            "minute":minute,
            "station":station,
            "direction":direction,
            "is_peak_hour":is_peak,
            "passenger_count":passengar_count
        })
        df=pd.DataFrame(records)

        df=df.sort_values("timestamp").reset_index(drop=True)
    return df
if __name__ =="__main__":
    df=generate_dataset(num_records=4000,start_date=datetime(2025,10,1),days_span=30)
    print(df.head(12))
    df.to_csv("mumbai_western_rush_sim.csv",index=False)
    print(f"\Saved mumbai_western_rush_sim.csv (rows:{len(df)})")