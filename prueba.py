import cv2

cap = cv2.VideoCapture("video.mp4")
x=100
y=100
dx = 2
dy=2
trayectoria=[]
while cap.isOpened():

    ret, im = cap.read()

    if ret == False:
        break
    cv2.rectangle(im, (x, y), (x + 200, y + 150), (0, 255, 0), 2)
    cv2.putText(im,"VEHICULO",(100, 90),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2)
    x=x+dx
    y=y+dy
    trayectoria.append((x, y))
    if len(trayectoria)>1:
        punto_anterior = trayectoria[-2]
        punto_actual = trayectoria[-1]
        dx=punto_actual[0]-punto_anterior[0]
        dy=punto_actual[1]-punto_anterior[1]
        distancia = (dx**2 + dy**2)**0.5
        print("Movimiento",distancia)
        for i in range(1,len(trayectoria)):
            cv2.line(im, trayectoria[i-1], trayectoria[i], (255, 255, 0),2)
    cv2.imshow("image", im)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
