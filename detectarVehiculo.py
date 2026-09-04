import cv2
from ultralytics import YOLO

model = YOLO("yolo11s.pt")

cap = cv2.VideoCapture("video2.mp4")

while cap.isOpened():

    ret, im = cap.read()

    if ret == False:
        break

    results = model(
        im,
        device="cpu",
        conf=0.30,
        verbose=False
    )

    result = results[0]

    annotated_frame = result.plot()

    cv2.imshow("VisionTraffic - Deteccion", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()