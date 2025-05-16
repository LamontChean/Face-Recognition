import face_recognition
import cv2
import os

# Load known data
known_data_encodings = []
known_data_names = []

for filename in os.listdir("storage"):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(f"storage/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_data_encodings.append(encoding)
        known_data_names.append(os.path.splitext(filename)[0])


# Initialize webcam
video_capture = cv2.VideoCapture(0)

print("Starting camera. Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()

    # Resize frame for speed
    small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect and encode faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_data_encodings, face_encoding)
        name = "Unauthorized"

        if True in matches:
            match_index = matches.index(True)
            name = known_data_names[match_index]

        # Scale back up face locations 
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw box
        cv2.rectangle(frame,(left, top), (right, bottom), (0,255,0) if name != "Unauthorized" else (0,0,255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255),2)

        cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()