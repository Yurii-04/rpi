import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не вдалося відкрити камеру")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Не вдалося зчитати кадр")
        break

    cv2.imshow("Потік з камери", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
