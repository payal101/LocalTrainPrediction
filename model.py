import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

df=pd.read_csv("mumbai_western_rush_sim.csv")
print(df.shape)
print(df.head())
print(df.describe())

#Passenger count by hour
plt.figure(figsize=(10,6))
sns.boxplot(x="hour",y="passenger_count",data=df)
plt.title("Passenger Count Distribution by Hour")
plt.show()

#Passenger count by station
plt.figure(figsize=(12,6))
sns.boxplot(x="station",y="passenger_count",data=df)
plt.xticks(rotation=45)
plt.title("Passenger count by station")
plt.show()

#Feature Engineering
df["is_peak_hour"]=((df["hour"]>=7)&(df["hour"]<=10))|((df["hour"]>=17)&(df["hour"]<=21))
df["is_peak_hour"]=df["is_peak_hour"].astype(int)

for col in ["station","day_of_week","direction"]:
    le=LabelEncoder()
    df[col]=le.fit_transform(df[col])
import joblib
joblib.dump(le,f"{col}_encoder.pkl")
print(df.head())

X=df.drop(columns=["passenger_count","timestamp","date"])
y=df["passenger_count"]

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)
 
from sklearn.ensemble import RandomForestRegressor
model=RandomForestRegressor(n_estimators=100,random_state=42)
model.fit(X_train,y_train)

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
preds=model.predict(X_test)
mse=mean_squared_error(y_test,preds)
rmse=np.sqrt(mse)

print("MAE",mean_absolute_error(y_test,preds))
print("RMSE",rmse)


#predictions vs actual
import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(y_test,preds,alpha=0.5)
plt.xlabel("Actual Passenger Count")
plt.ylabel("Predicted Passenger Count")
plt.title("Model Performance")
plt.show()

import joblib
joblib.dump(model,"rush_model.pkl")
print("Model saved as rush_model.pkl") 
