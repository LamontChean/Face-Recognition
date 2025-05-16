import face_recognition
import cv2
import os

# Load known faces (you could call this once at startup)
def load_known_faces(folder="storage"):
    encodings = []
    names = []
    for file in os.listdir(folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            img = face_recognition.load_image_file(os.path.join(folder, file))
            encoding = face_recognition.face_encodings(img)[0]
            encodings.append(encoding)
            names.append(os.path.splitext(file)[0])
    return encodings, names

# Perform recognition on a new image
def recognize_faces(image_path, known_encodings, known_names, output_path):
    image = face_recognition.load_image_file(image_path)
    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, encoding)
        name = "Unauthorized"
        if True in matches:
            name = known_names[matches.index(True)]

        color = (0, 255, 0) if name != "Unauthorized" else (0, 0, 255)
        cv2.rectangle(image_bgr, (left, top), (right, bottom), color, 2)
        cv2.putText(image_bgr, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    cv2.imwrite(output_path, image_bgr)
    return output_path