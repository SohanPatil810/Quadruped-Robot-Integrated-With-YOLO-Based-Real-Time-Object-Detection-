import cv2
import supervision as sv
from ultralytics import YOLO
import telegram
import time

# === ESP32-CAM stream URL ===
ESP32_URL = "http://10.169.203.252:81/stream"

# === Telegram Bot Setup ===
BOT_TOKEN = "Enter your Bot token"  # Your bot token
CHAT_ID = "Enter your Chat ID"  # Your chat ID

bot = telegram.Bot(token=BOT_TOKEN)

# === YOLO Setup ===
video = cv2.VideoCapture(ESP32_URL)
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
model = YOLO("yolov8n.pt")  # nano model = fastest

box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()

# === Prepare for video saving ===
ret, frame = video.read()
if not ret:
    print("⚠ Could not read initial frame. Check ESP32-CAM connection.")
    exit()

height, width = frame.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 10, (width, height))

print("🚀 ESP32-CAM Object Detection + Telegram Alerts Running...")
print("💡 Press 'Q' to quit.")

# === Alert Control ===
last_alert_time = 0
ALERT_COOLDOWN = 20  # seconds between alerts

while True:
    ret, frame = video.read()
    if not ret:
        print("⚠ Lost stream. Reconnecting...")
        time.sleep(2)
        video = cv2.VideoCapture(ESP32_URL)
        continue

    # Run YOLO detection
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    detections = detections[detections.confidence > 0.5]
    labels = [results.names[int(cid)] for cid in detections.class_id]

    # Annotate frame
    frame = box_annotator.annotate(scene=frame, detections=detections)
    frame = label_annotator.annotate(scene=frame, detections=detections, labels=labels)

    # Add "Press Q" text
    cv2.putText(frame, "Press 'Q' to quit", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show and save
    cv2.imshow("ESP32-CAM Detection + Telegram", frame)
    out.write(frame)

    # Send Telegram Alert
    if labels and (time.time() - last_alert_time > ALERT_COOLDOWN):
        label_text = ", ".join(set(labels))
        cv2.imwrite("alert.jpg", frame)
        try:
            bot.send_message(chat_id=CHAT_ID, text=f"🚨 Detected: {label_text}")
            bot.send_photo(chat_id=CHAT_ID, photo=open("alert.jpg", "rb"))
            print(f"📨 Sent Telegram alert for: {label_text}")
        except Exception as e:
            print("❌ Telegram send failed:", e)
        last_alert_time = time.time()

    # Exit condition
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        print("🛑 Stopping...")
        break

# === Cleanup ===
video.release()
out.release()
cv2.destroyAllWindows()
print("✅ Done! Video saved as output.avi")
