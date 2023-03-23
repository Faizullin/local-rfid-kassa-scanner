from urllib.request import urlopen
import numpy as np;
import datetime,requests,sys,face_recognition,os,cv2,time,pickle
from threading import Thread

__all__=['WebCamera','LocalCamera','FaceDetector']


class Camera(object):
    path=None
    state=True
    def on(self):
        self.state = True

    def off(self):
        self.state=False
    def __del__(self):
        self.off()

class WebCamera(Camera):
    def __init__(self,path):
        self.path=path;
        if not(type(path) is str and path.startswith('http')):
            raise Exception("WRONG")

    def read(self):
        try:
            info = urlopen(self.path).read()
        except Exception as err:
            print("Error",err)
            return 0,None;
        if info==b'':
            return False,None
        imgNp=np.array(bytearray(info),dtype=np.uint8)
        return (True,cv2.imdecode(imgNp,-1));


class LocalCamera(Camera):
    def __init__(self,path):
        self.path=path;
        print("connection: ",self.connect())
            

    def connect(self):
        try:
            self.vid = cv2.VideoCapture(self.path)
            return self.vid.read()[0]

        except Exception as err:
            print("Camera connection error ("+str(err)+")")
            self.vid=None
            return False
    def read(self):
        if self.vid is None:
            self.connect()
            return False,None;
        return self.vid.read()
    def __del__(self):
        
        if self.vid is not None:
            self.vid.release()

class FaceDetector():
    current_frame = None
    camera_index = 0
    state=False
    method = 1
    model = {
        'face_encodings': None,
        'face_names': None
    }
    delay = 0
    def __init__(self, config=None,ser=None):
        self.ser = ser
        self.devices=[]
        for dev in range(len(config.camera_settings['devices'])):
            if type(config.camera_settings['devices'][dev]) is str and config.camera_settings['devices'][dev].startswith('http'):
                self.devices.append(WebCamera(config.camera_settings['devices'][dev]))
            elif type(config.camera_settings['devices'][dev]) is int:
                self.devices.append(LocalCamera(config.camera_settings['devices'][dev]))
            else:
                raise Exception("wrong camera path/index");
        self.faces_path = config.PATHS['faces_path']
        print(self.devices)
        
    def on(self):
        self.state= True;

    def off(self):
        self.state = False;
        cv2.destroyAllWindows();

    def run(self):
        while True:
            if not self.state:
                time.sleep(1)
                continue
            ret,frame = self.devices[self.index].read()

            if not ret: 
                self.ser.die("No frame")
                continue
            frame = self.resize(frame, width=500)
            if self.method == 0:
                self.current_frame = frame
                pass
            else:
                detected=False
                if self.method == 1:
                    detected,frame = self.detect_face(frame)
                    self.current_frame = frame
                    if detected:
                        print(f"Found {detected}")
                if self.delay:
                    self.sleep(self.delay)
                if detected!=False:
                    pass
            # cv2.imshow("FRAME",frame)
            # if cv2.waitKey(1) == ord('q'):
            #     self.off()
            #     return


    def read(self):
        #return self.current_frame is not None, self.current_frame
        ret,frame = self.devices[self.index].read()
        if not ret: 
            self.ser.die("No frame")
            self.off()
            return False,None
        return ret,frame;

    def resize(self,img,width=None,inter=cv2.INTER_AREA):
        (h,w)=img.shape[:2]
        if width is not None:
            r=width/float(w);
            dim=(width,int(h*r));
        return cv2.resize(img,dim,interpolation=inter);

    def sleep(self,delay=0):
        time.sleep(delay)
        
    def detect_face(self,frame):
        res=False
        rgb_frame = frame[:, :, ::-1]

        # Find the face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame, model='hog')
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations, model='large')

        # Loop through each face in the frame and compare it to the pre-trained encodings
        for face_encoding, face_location in zip(face_encodings, face_locations):

            matches = face_recognition.compare_faces(self.model['face_encodings'], face_encoding,tolerance=0.6)
            name="Unknown"
            face_distances = face_recognition.face_distance(self.model['face_encodings'],face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.model['face_names'][best_match_index]
                res = True

            # Draw a rectangle around the face and label it with the name
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            

            
        
        return res,frame

    def load_faces(self):
        with open("data/face_encodings.pickle", "rb") as f:
            face_encodings, face_names = pickle.load(f)
            self.model['face_encodings'] = face_encodings
            self.model['face_names'] = face_names


    