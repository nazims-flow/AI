import cv2
import numpy as np

# Replace '0' with the path to your video file, e.g., 'road_car_view.mp4'
cap = cv2.VideoCapture('test_video.mp4')

# Ensure the video capture is opened successfully
if not cap.isOpened():
    print("Error: Couldn't open the video file.")
    exit()

# Set the resolution (optional)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, img = cap.read()
    if not ret:
        print("End of video")
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    mask = np.zeros_like(edges)
    height, width = mask.shape
    polygon = np.array([[
        (0, height),
        (width, height),
        (width // 2, height // 2)
    ]])
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    lines = cv2.HoughLinesP(masked_edges, rho=6, theta=np.pi/60, threshold=160, lines=np.array([]), minLineLength=40, maxLineGap=25)

    line_img = np.zeros_like(img)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 10)

    result = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)

    cv2.imshow('Result', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()
