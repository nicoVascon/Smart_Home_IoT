import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from datetime import datetime, timedelta

def Add_Room(userDoc_ref : firestore.DocumentReference, 
             roomName : str, 
             roomType : str):
    """
    Adds a room to the user's collection of rooms.

    :param userDoc_ref: The reference to the user's document in Firestore.
    :type userDoc_ref: firestore.DocumentReference
    :param roomName: The name of the room.
    :type roomName: str
    :param roomType: The type of the room.
    :type roomType: str
    """ 
    roomDoc_ref = userDoc_ref.collection("rooms").document(roomName)
    roomDoc_ref.set({"Room_Name": roomName, "Room_Type": roomType})

def Add_Device_Sensor(userDoc_ref : firestore.DocumentReference,
                      roomName : str, 
                      deviceChannel : int, 
                      deviceName : str, 
                      deviceType : str):
    roomDoc_ref = userDoc_ref.collection("rooms").document(roomName)
    device_ref = roomDoc_ref.collection("Sensors").document(str(deviceChannel))
    device_dict = {
        "associatedRoomRef": roomDoc_ref, 
        "channel": deviceChannel, 
        "connectionState": True, 
        "connectionStateSaved": False, 
        "dataPoints": [], 
        "name": deviceName, 
        "notifications": [], 
        "type": deviceType, 
        "value": 0.0, 
        "valueSaved": 0.0
    }
    device_ref.set(device_dict)

def Add_Device_Actuator(userDoc_ref : firestore.DocumentReference,
                      roomName : str,
                      deviceChannel : int, 
                      deviceName : str, 
                      deviceType : str, 
                      associatedSensorChannel : int):
    roomDoc_ref = userDoc_ref.collection("rooms").document(roomName)
    device_ref = roomDoc_ref.collection("Actuators").document(str(deviceChannel))
    if associatedSensorChannel is not None:
        associatedSensorRef = roomDoc_ref.collection("Sensors").document(associatedSensorChannel)
    else:
        associatedSensorRef = None
    device_dict = {
        "associateddSensorRef": associatedSensorRef, 
        "channel": deviceChannel, 
        "connectionState": True, 
        "connectionStateSaved": False, 
        "dataPoints": [], 
        "name": deviceName, 
        "notifications": [], 
        "type": deviceType, 
        "value": 0.0, 
        "valueSaved": 0.0
    }
    device_ref.set(device_dict)

def setValue(userDoc_ref : firestore.DocumentReference,
             roomName : str, 
             deviceChannel : int, 
             value : float, 
             isSensor : bool):
    roomDoc_ref = userDoc_ref.collection("rooms").document(roomName)
    if isSensor:
        device_ref = roomDoc_ref.collection("Sensors").document(str(deviceChannel))
        description = "Novo Valor Recebido: " + str(value)
        addNotification(device_ref, currentDate, description)
    else:
        device_ref = roomDoc_ref.collection("Actuators").document(str(deviceChannel))
    
    device_ref.update({"value": value})

    currentDate = datetime.now()
    addDataPoint(device_ref, currentDate, value)

def addDataPoint(device_ref : firestore.DocumentReference, 
                 currentDate : datetime, 
                 value : float):
    x = int(currentDate.timestamp()*1000)
    device_ref.update({"dataPoints": firestore.ArrayUnion([{"x": x, "y": value}])})

def addNotification(device_ref : firestore.DocumentReference, 
                    currentDate : datetime, 
                    description : str):
    device_ref.update({"notifications": firestore.ArrayUnion([{"date": currentDate, 
                                                            "dateFormatted": currentDate.strftime("%d/%m/%Y %H:%M:%S"), 
                                                            "description": description}])})
    
def setAssociatedSensor(userDoc_ref : firestore.DocumentReference,
                         roomName : str, 
                         deviceChannel : int, 
                         associatedSensorChannel : int):
    roomDoc_ref = userDoc_ref.collection("rooms").document(roomName)
    actuatorRef = roomDoc_ref.collection("Actuators").document(str(deviceChannel))
    associatedSensorRef = roomDoc_ref.collection("Sensors").document(str(associatedSensorChannel))
    actuatorRef.update({"associateddSensorRef": associatedSensorRef})