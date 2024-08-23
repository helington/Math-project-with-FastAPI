import cv2
import mediapipe as mp
import numpy as np


mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection


def draw_golden_spiral(image, center, scale):
    num_turns = 3  
    angle = 0
    points = []

    while angle < num_turns * 2 * np.pi:
        r = scale * np.exp(0.306349 * angle)
        x = int(center[0] + r * np.cos(angle))
        y = int(center[1] + r * np.sin(angle))
        points.append((x, y))
        angle += 0.1

   
    for i in range(len(points) - 1):
        cv2.line(image, points[i], points[i + 1], (0, 255, 0), 2)


image = cv2.imread('monalisa.jpg')
height, width, _ = image.shape


image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
    results = face_mesh.process(image_rgb)

    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_eye_x = int(face_landmarks.landmark[33].x * width)
            left_eye_y = int(face_landmarks.landmark[33].y * height)
            right_eye_x = int(face_landmarks.landmark[263].x * width)
            right_eye_y = int(face_landmarks.landmark[263].y * height)
            center_x = (left_eye_x + right_eye_x) // 2
            center_y = (left_eye_y + right_eye_y) // 2

            
            draw_golden_spiral(image, (center_x, center_y), scale=5)

with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
    results = face_detection.process(image_rgb)

    if results.detections:
        for detection in results.detections:
            mp_drawing.draw_detection(image, detection)

cv2.imshow('Espiral Áurea', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
