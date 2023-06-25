import face_recognition
import os
import pickle,cv2

# Define the path to the directory containing the face images
PREFIX_PATH = os.getcwd()
faces_dir = os.path.join(PREFIX_PATH, "data/train_face")

# Create lists to store the face encodings and corresponding names
train_face_encodings = []
train_face_names = []

# Loop through each image in the directory
for filename in os.listdir(faces_dir):
    # Load the image using face_recognition
    print("Train",os.path.join(faces_dir, filename),'with name',filename.split(".")[0])
    #image = face_recognition.load_image_file(os.path.join(faces_dir, filename))
    image = cv2.imread(os.path.join(faces_dir, filename))
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, boxes)

    ## Find the face locations and encodings in the image
    #face_locations = face_recognition.face_locations(image)
    #face_encodings = face_recognition.face_encodings(image, face_locations)

    # Add the face encodings and corresponding names to the lists
    for encoding in face_encodings:
        train_face_encodings.append(encoding)
        train_face_names.append(filename.split(".")[0])


with open(os.path.join(PREFIX_PATH, "data/face_encodings.pickle"), "wb") as f:
    print("Data",train_face_names,len(train_face_encodings))
    pickle.dump((train_face_encodings, train_face_names), f)