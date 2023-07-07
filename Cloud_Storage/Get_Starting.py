import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('D:\DEV\SE_IoT\Projeto_Final\Smart_Home_IoT\Cloud_Storage\smart-home-iot-52bab-firebase-adminsdk-hf6b4-ff69bd278b.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# -------------- Add Data --------------
doc_ref = db.collection("users").document("alovelace")
doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1800})

doc_ref = db.collection("users").document("aturing")
doc_ref.set({"first": "Alan", "middle": "Mathison", "last": "Turing", "born": 1912})

# -------------- Read Data --------------
users_ref = db.collection("users")
docs = users_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")