import time
import RPi.GPIO as GPIO
import face_recognition
import picamera
import numpy as np

face_locations = []
face_encodings = []
name = ""

#Initialize Raspberry Pi Camera
camera = picamera.PiCamera()
# Set camera to a low resolution to prevent lag
camera.resolution = (320, 240)
out = np.empty((240, 320, 3), dtype=np.uint8)
#Prep GPIO for connected speed controller
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

# Import face images for the camera to recognize
# Make sure that the given faces are placed within the same folder as the python script
# Domenico's face
Didi_image = face_recognition.load_image_file("Didi.jpg")
Didi_face_encoding = face_recognition.face_encodings(Didi_image)[0]
# Jordan's face
Zois_image = face_recognition.load_image_file("Zois.jpg")
Zois_face_encoding = face_recognition.face_encodings(Zois_image)[0]
# Eugenio's face
Euge_image = face_recognition.load_image_file("Euge.jpg")
Euge_face_encoding = face_recognition.face_encodings(Euge_image)[0]

# Array of known faces
known_faces = [Euge_face_encoding, Didi_face_encoding, Zois_face_encoding]

# Boolean to determine if a robotics member is recognized
approved = False

# Create infinite loop as this script will always be running on the pi
while True:
    print ("Scanning")

    # Begin grabbing each frame and checking if any if the known faces appear using the face_recognition library
    camera.capture(output, format="rgb")
    
    face_locations = face_recognition.face_locations(out)
    face_encodings = face_recognition.face_encodings(out, face_locations)
    face_names = []
    
    # Check each face found in each frame and determine whether access should be granted or not
    for face in face_encodings:
        match = face_recognition.compare_faces(known_faces, face, tolerance=0.5)
        name = None

        if match[0]:
            name = "Eugenio"
            approved = True
        elif match[1]:
            name = "Domenico"
            approved = True
        elif match[2]:
            name = "Zois"
            approved = True

    if approved:
        print("Member Recognized:")
        print(name)
        GPIO.output(7,1)
        time.sleep(2)
        GPIO.output(7,0)
        time.sleep(0.0001)
        approved = False
        break