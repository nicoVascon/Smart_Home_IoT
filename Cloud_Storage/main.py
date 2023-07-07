import Firebase_Functions as ff

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

newValue = 23.5
sensorChannel = 1

# ff.Add_Device_Sensor(userDoc_ref, room_name, sensorChannel, "Presença", "DIGITAL")
# ff.setValue(userDoc_ref, room_name, sensorChannel, newValue)

actuatorChannel = 2
newValue = 13.6
actuatorName = "Aquecedor"
associatedSensorChannel = None
# ff.Add_Device_Actuator(userDoc_ref, room_name, actuatorChannel, actuatorName, "DIGITAL", associatedSensorChannel)
ff.setValue(userDoc_ref, room_name, actuatorChannel, newValue, isSensor=False)

