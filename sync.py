import numpy as np
import cv2
import requests, os, re
import datetime
from cv2 import VideoCapture
import face_recognition

video_capture = VideoCapture(0)
# video_capture.set(5,1)
known_face_encodings = []
known_face_names = []
known_faces_filenames = []
for (dirpath, dirnames, filenames) in os.walk('tof'):
    known_faces_filenames.extend(filenames)
    break
for filename in known_faces_filenames:
    face = face_recognition.load_image_file('tof/'+filename)
    known_face_names.append(re.sub("[0-9]", '', filename[:-4]))
    known_face_encodings.append(face_recognition.face_encodings(face)[0])
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
while True:
    ret, frame = video_capture.read()
    if process_this_frame:
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        face_names.append(name)
        print(name)
        process_this_frame = not process_this_frame
        date = datetime.datetime.now()
        h = date.hour
        m = date.minute
        s = date.second
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name+'{0}h {1}min'.format(h, m), (left + 6, bottom - 6), font, 1.0, (0, 255, 0), 1)
            cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()