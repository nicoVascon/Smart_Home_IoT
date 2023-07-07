import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('D:\DEV\SE_IoT\Projeto_Final\Smart_Home_IoT\Cloud_Storage\smart-home-iot-52bab-firebase-adminsdk-hf6b4-ff69bd278b.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

userDoc_ref = db.collection("users").document("nicolas.freire.vasconcellos@gmail.com")
roomDoc_ref = userDoc_ref.collection("rooms").document("Sala")

roomDoc_ref.set({"Room_Name": "Sala", "Room_Type": "LIVING_ROOM"})
# print(roomDoc_ref.id)
