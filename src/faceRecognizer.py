class FaceRecognizer:
    def __init__(self):
        pass
import face_recognition,cv2
import time
import sqlite3

# Connect to the database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL,
             image BLOB NOT NULL)''')

# Load known faces and names from the database
known_face_encodings = []
known_face_names = []
for row in c.execute('SELECT name, image FROM users'):
    name = row[0]
    image = row[1]
    known_face_encodings.append(face_recognition.face_encodings(image)[0])
    known_face_names.append(name)

# Initialize serial port and face recognition
ser = serial.Serial('/dev/ttyACM0', 9600) # Change this to match your serial port
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Read data from serial port scanner
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print("Scanned ID:", line)
        
        # Search for the scanned ID in the database
        c.execute('SELECT name FROM users WHERE id=?', (line,))
        result = c.fetchone()
        if result is not None:
            name = result[0]
            print("Welcome,", name)
        else:
            print("User not found in database")

    # Process video frames for face recognition
    if process_this_frame:
        # Capture frame from camera
        # Replace this with your own code for capturing a video frame
        ret, frame = video_capture.read()

        # Convert the frame from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Initialize an array for the names of the detected faces
        face_names = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If a match was found, use the first one
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            else:
                name = "Unknown"

            # Add the name of the detected face to the list of detected face names
            face_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with the name below the face
        #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv