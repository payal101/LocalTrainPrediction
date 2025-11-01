import requests
import json

url = "http://127.0.0.1:5000/predict"
data = {
    "day_of_week":2,
    "direction":1,
    "hour":17,
    "is_peak_hour":1,
    "minute":30,
    "station":5
}

response = requests.post(url, json=data)
print(response.status_code)
print(response.text)



