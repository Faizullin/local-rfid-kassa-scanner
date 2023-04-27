import cv2

# Create a video capture object
cap = cv2.VideoCapture(2)

# Check if camera is opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

ret, frame = cap.read()
cv2.imwrite('./image.png', frame)