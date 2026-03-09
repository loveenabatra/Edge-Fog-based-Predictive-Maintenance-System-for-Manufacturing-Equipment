import pandas as pd
import joblib
import json
import time
import paho.mqtt.client as mqtt

model = joblib.load("predictive_model.pkl")

THINGSBOARD_HOST = "thingsboard.cloud"
ACCESS_TOKEN = "d00a9ohvqpbwczmaygb5"

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.connect(THINGSBOARD_HOST,1883,60)

data = pd.read_csv("sensor_stream.csv")

features = ["sensor2","sensor3","sensor4","sensor7","sensor11","sensor12","sensor15"]

for index,row in data.iterrows():

    input_data = row[features].values.reshape(1,-1)

    prediction = model.predict(input_data)[0]

    payload = {
    "temperature": float(row["sensor2"]),
    "pressure": float(row["sensor3"]),
    "turbine_temp": float(row["sensor4"]),
    "core_speed": float(row["sensor7"]),
    "fuel_flow": float(row["sensor11"]),
    "bypass_ratio": float(row["sensor12"]),
    "fan_speed": float(row["sensor15"]),
    "failure_prediction": int(prediction)
}

    client.publish(
        "v1/devices/me/telemetry",
        json.dumps(payload)
    )

    print(payload)

    time.sleep(2)