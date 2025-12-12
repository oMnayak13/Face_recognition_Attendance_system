from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import numpy as np
import csv
from datetime import datetime
import os

app = Flask(__name__)

# Path to the images folder
path = "C:/Users/hp/OneDrive/Desktop/Attendance_app/yolo_images"

known_encodings = []
known_names = []

# Load known faces from the folder
for filename in os.listdir(path):
    if filename.endswith((".jpg", ".png", ".jpeg")):
        img_path = os.path.join(path, filename)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])  # use filename as name

known_face_encodings = known_encodings
known_face_names = known_names

# Start webcam
video_capture = cv2.VideoCapture(0)

marked_names = set()

# Function to mark attendance
def mark_attendance(name):
    with open("attendance.csv", "a", newline="") as f:
        writer = csv.writer(f)
        now = datetime.now()
        writer.writerow([name, now.strftime("%H:%M:%S")])

# Route for homepage
@app.route('/')
def index():
    return render_template('face.html')  # Make sure templates/face.html exists

# Generate video frames
def gen_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if name not in marked_names:
                        mark_attendance(name)
                        marked_names.add(name)

                # Draw rectangle and name
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route to get attendance CSV data
@app.route('/get_attendance')
def get_attendance():
    with open("attendance.csv", "r") as f:
        data = list(csv.reader(f))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
