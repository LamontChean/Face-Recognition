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

# Load input image
input_image_path = "input.jpg"
image = face_recognition.load_image_file(input_image_path)
image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Detect and encode faces
face_locations = face_recognition.face_locations(image)
face_encodings = face_recognition.face_encodings(image, face_locations)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_data_encodings, face_encoding)
    name = "Unauthorized"

    if True in matches:
        match_index = matches.index(True)
        name = known_data_names[match_index]

    color = (0,255,0) if name != "Unauthorized" else (0,0,255)
    cv2.rectangle(image_bgr, (left, top), (right, bottom), color, 2)
    cv2.putText(image_bgr, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

cv2.imshow("Result", image_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()