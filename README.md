# Quadruped Robot with YOLO-based Real-Time Object Detection

This project showcases an advanced quadruped robot that integrates **Arduino-based locomotion** with **YOLOv8 AI object detection** using an **ESP32-CAM**. It supports smartphone remote control and fully autonomous detection with **Telegram alerts**.

\---

## 🚀 Overview

The system consists of two major components:

### **1. Locomotion \& Control (Arduino Nano)**

An Arduino Nano controls 12 servo motors to perform coordinated quadruped movements such as walking, turning, sitting, standing, and dancing.

### **2. Vision \& Intelligence (YOLOv8 + ESP32-CAM)**

A Python script processes live ESP32-CAM footage, performs real-time object detection using YOLOv8, and sends instant photo alerts to a Telegram bot.

\---

## ✨ Key Features

* **12-DOF Quadruped Movement** using inverse kinematics.
* **Real-Time Object Detection** with YOLOv8 (nano model).
* **Smart Telegram Alerts** with image snapshots.
* **Multiple Movement Modes,** including walk, turn, sit, stand, and dance.
* **Precise Servo Control** using `FlexiTimer2` for 50Hz synchronised updates.

\---

## 🛠️ Hardware Requirements

### **Robot Body \& Movement**

* **Arduino Nano**
* **Nano 328P Expansion IO Shield**
* **12× SG90 Servos**
* **HC-05 Bluetooth Module**
* **2× Lithium-ion Batteries**
* **LM2596 Buck Converter**

### **Vision System**

* **ESP32-CAM Module**
* **Computer (Windows/Linux)** to run the YOLO detection script

\---

## 💻 Software Setup

### **1. Arduino Locomotion Setup**

1. Install required libraries (`Servo.h`, `FlexiTimer2`).
2. Open the file **`spider\_remote.ino`** and upload it to the Arduino Nano.
3. Install a controller app on your smartphone:
**Bluetooth RC Controller** (Android)

Control Mapping:

* **F / B** → Walk Forward / Backward
* **L / R** → Turn Left / Right
* **X / x** → Stand / Sit
* **V / U** → Wave / Dance

\---

### **2. YOLOv8 Vision \& Telegram Alerts (Python)**

Run these commands in your terminal:

```bash
cd C:\\Users\\sohan\\esp32cam-yolo
.\\.venv\\Scripts\\activate
python detect\_esp32\_telegram.py
```

The script will:

* Read ESP32-CAM video stream
* Detect objects using YOLOv8
* Save detection images
* Send alerts via Telegram bot

\---

## 🧠 System Workflow (Step-by-Step)

### **1. Inverse Kinematics (IK)**

Given coordinates (X, Y, Z), the angles for the hip, thigh, and knee servos are calculated to place each leg precisely.

### **2. Smooth Motion Control**

`FlexiTimer2` triggers a 50Hz interrupt for:

* Linear interpolation of servo positions
* Smooth leg transitions without jerkiness

### **3. ESP32-CAM Video Stream**

Live feed URL example:

```
http://10.169.203.252:81/stream
```

Each frame is forwarded into YOLOv8.

### **4. YOLO Detection \& Telegram Alerts**

On detection:

1. Frame is processed
2. Bounding boxes \& labels are drawn
3. Snapshot saved as `alert.jpg`
4. Sent to Telegram bot
5. 20-second cooldown prevents alert spam

\---

## 📂 Project Structure

```
├── spider\_remote.ino          # Arduino movement \& Bluetooth logic
├── FlexiTimer2.cpp/.h         # Timer library for precise servo handling
├── detect\_esp32\_telegram.py   # YOLO detection + Telegram alert script
├── STL Files                  # Robot 3D print files
```

### STL Download

Robot body STL files can be downloaded here:
https://www.thingiverse.com/thing:4815137



## ⭐ Acknowledgements

* Ultralytics YOLOv8
* ESP32-CAM Community
* Arduino Libraries

