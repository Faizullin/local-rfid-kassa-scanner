import subprocess as sp
import socket
ip_camera = "http://192.168.1.101:8080/shot.jpg"




res = sp.getoutput("hostname -I")
res = socket.gethostbyname(socket.gethostname())
m= False
if res and "." in res and m:
    ip_camera = f"192.168.{ res.split('.')[2] }.101:4747"
    print("Updated ip camera in:",ip_camera,res)
    
#ENABLE_ACCOUNT = 'https://myaccount.google.com/lesssecureapps?pli=1&rapt=AEjHL4OCX7qsNoB5qwZmOXuzjiyqPPY65E6x-NCYKREntcOhDo8tBWgQU0kPqTccNDabUzDNZ2lPYMz0LGGSPL7JMfhb77-Ueg'
PATHS={
    "db":"/home/adminu/Desktop/uhf/local-rfid-kassa-scannerdata/db/main.db",
    'events':'/home/adminu/Desktop/uhf/local-rfid-kassa-scannerdata/config/events.txt',
    'info':'/home/adminu/Desktop/uhf/local-rfid-kassa-scannerdata/config/info.json',
    "DCIM":"/home/adminu/Desktop/uhf/local-rfid-kassa-scannerdata/DCIM/",
    'faces_path': "/home/adminu/Desktop/uhf/local-rfid-kassa-scannerdata/models.faces.pickle",
    "urls":{
        #"esp":f"http://192.168.{ip}.7/",
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

