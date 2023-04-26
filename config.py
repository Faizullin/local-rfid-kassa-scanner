import subprocess as sp
import socket, os
ip_camera = "http://192.168.1.103:8080/shot.jpg"




res = sp.getoutput("hostname -I")
res = socket.gethostbyname(socket.gethostname())
m= False
if res and "." in res and m:
    ip_camera = f"192.168.{ res.split('.')[2] }.101:4747"
    print("Updated ip camera in:",ip_camera,res)

PREFIX_PATH =  "/home/adminu/Desktop/uhf/local-rfid-kassa-scanner"
PATHS={
    "db": os.path.join(PREFIX_PATH, os.path.join("data","db.sqlite3")),
    'faces_path': os.path.join(PREFIX_PATH, os.path.join("data","face_encodings.pickle")),
    'driver': os.path.join(PREFIX_PATH, "data/driver/raspberry/libCFComApi.so"),
    'train_model': os.path.join(PREFIX_PATH, "data/face_encodings.pickle"),
    "urls":{
        'imgin' : ip_camera,
        "api": "https://rfid-kassa.com"
    }
}

camera_settings={
    'devices':{
        0: 0,
        1: ip_camera
    },
}

