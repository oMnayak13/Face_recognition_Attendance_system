Face Recognition Attendance System

A real-time Face Recognition Attendance System built using **Python, Flask, OpenCV, and face_recognition**. The application captures live webcam feed, detects and identifies faces from a stored image database, and automatically records attendance with timestamps into a CSV file. A simple web interface allows users to view the video stream, manage attendance records, and download logs.

---

## **Features**

* Real-time face detection and recognition
* Automatic attendance marking with timestamps
* Web-based UI for viewing attendance
* Live webcam video streaming
* Prevents duplicate attendance entries
* CSV-based attendance storage
* Easy face registration (add images to `yolo_images/`)
* Options to refresh faces, clear logs, and download CSV

---

## **Project Structure**

```
Attendance_app/
│── app.py
│── attendance.csv
│── yolo_images/
│     ├── person1.jpg
│     ├── person2.png
│── templates/
      └── face.html
```

---

## **How It Works**

1. Store face images inside `yolo_images/`

   * File name becomes the user name (e.g., `Om.jpg` → Om)

2. The system loads all encodings at startup.

3. When a known face appears in webcam feed, the system:

   * Identifies the person
   * Marks attendance in `attendance.csv`
   * Shows the name and bounding box on video

4. The web UI displays live video and attendance table.

---

## **Installation**

### **1. Clone the repository**

```
git clone https://github.com/<your-username>/<repo-name>.git
```

### **2. Install dependencies**

```
pip install flask opencv-python face_recognition numpy
```

If `face_recognition` fails, install:

```
pip install cmake
```

### **3. Run the application**

```
python app.py
```

### **4. Open in browser**

```
http://127.0.0.1:5000/
```

## **Dependencies**

* Python 3.x
* Flask
* OpenCV
* face_recognition
* NumPy


## **Future Enhancements**

* Database integration (MySQL / MongoDB)
* Admin dashboard
* User registration through UI
* Cloud deployment
* Multi-camera support

