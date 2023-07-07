import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('D:\DEV\SE_IoT\Projeto_Final\Smart_Home_IoT\Cloud_Storage\smart-home-iot-52bab-firebase-adminsdk-hf6b4-ff69bd278b.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


user_email = "nicolas.freire.vasconcellos@gmail.com"
room_name = "Sala"

userDoc_ref = db.collection("users").document(user_email)
roomDoc_ref = userDoc_ref.collection("rooms").document(room_name)

from datetime import datetime, timedelta
date = datetime.now()
date_formatted = date.strftime("%d/%m/%Y %H:%M:%S")
yesterday = datetime.now() - timedelta(1)
yesterday_formatted = yesterday.strftime("%d/%m/%Y %H:%M:%S")

device_channel = "0"
device_ref = roomDoc_ref.collection("Sensors").document(device_channel)
device_ref.set({"associatedRoomRef": roomDoc_ref, "channel": device_channel, 
                "connectionState": True, "connectionStateSaved": False, 
                "dataPoints": [{"x": 1677521896044, "y": 0}, {"x": 1677521926982, "y": 0}], 
                "name": "Luz", "notifications": [{"date": date, 
                                                  "dateFormatted": date_formatted, 
                                                  "description": "Novo Valor Recebido: 25,60"}, 
                                                  {"date": yesterday, 
                                                  "dateFormatted": yesterday_formatted, 
                                                  "description": "Novo Valor Recebido: 25,60"}], 
                "type": "DIGITAL", "value": 25.6, "valueSaved": 0.0})

