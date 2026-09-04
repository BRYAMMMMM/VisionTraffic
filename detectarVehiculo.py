import cv2
from ultralytics import YOLO

model = YOLO("yolo11s.pt")

cap = cv2.VideoCapture("video2.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)

print("FPS:", fps)

trayectorias = {}

while cap.isOpened():

    ret, im = cap.read()

    if ret == False:
        break

    results = model.track(
        im,
        device="cpu",
        conf=0.30,
        persist=True,
        verbose=False
    )

    result = results[0]

    if result.boxes.id is not None:

        ids = result.boxes.id
        boxes = result.boxes.xyxy

        for track_id, box in zip(ids, boxes):

            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            track_id = int(track_id)

            if track_id not in trayectorias:
                trayectorias[track_id] = []

            posicion = (
                int(center_x),
                int(center_y)
            )

            trayectorias[track_id].append(posicion)

            if len(trayectorias[track_id]) >= 2:

                punto_anterior = trayectorias[track_id][-2]
                punto_actual = trayectorias[track_id][-1]

                delta_x = (
                    punto_actual[0]
                    - punto_anterior[0]
                )

                delta_y = (
                    punto_actual[1]
                    - punto_anterior[1]
                )

                distancia = (
                    delta_x**2 + delta_y**2
                )**0.5

                velocidad_pixeles = distancia * fps

                print(
                    "ID:", track_id,
                    "Posicion:", posicion,
                    "Movimiento:", round(distancia, 2),
                    "pixeles",
                    "Velocidad:", round(velocidad_pixeles, 2),
                    "pixeles/segundo"
                )

    annotated_frame = result.plot()

    for track_id, puntos in trayectorias.items():

        for i in range(1, len(puntos)):

            punto_anterior = puntos[i - 1]
            punto_actual = puntos[i]

            cv2.line(
                annotated_frame,
                punto_anterior,
                punto_actual,
                (255, 255, 0),
                2
            )

    cv2.imshow(
        "VisionTraffic - Tracking",
        annotated_frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()