from flask import Flask,request,jsonify
import joblib
import pandas as pd
app=Flask(__name__)
model=joblib.load("rush_model.pkl")
@app.route('/predict',methods=['POST'])
def predict():
    data=request.get_json()
    print("Receieved data",data)

    if "day_index" in data:
        data["day_of_week"]=data.pop("day_index")
    if "station_index"in data:
        data["station"]=data.pop("station_index")
    day_map ={
        0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
    
    station_map={
        0:"Central ",1:"South",2:"East",3:"West"
    }
    if "day_of_week" in data and isinstance(data["day_of_week"],int):
        data["day_of_week"]=day_map[data["day_of_week"]]
    if "station" in data  and isinstance(data["station"],int):
        data["station"]=station_map[data["station"]]
    df=pd.DataFrame([data])
    df=df.reindex(columns=model.feature_names_in_,fil_value=0)
    prediction=model.predict(df)
    return jsonify({
        "input_received":data,
        "prediction":float(prediction[0]),
        "status":"success"
    })
if __name__ =="__main__":
    app.run(debug=True)
