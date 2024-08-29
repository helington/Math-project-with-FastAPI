import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

def modify_image(image_path):
    def draw_golden_spiral(image, center, scale):
        num_turns = 3
        angle = 0
        points = []

        while angle < num_turns * 2 * np.pi:
            r = scale * np.exp(0.306349 * angle)
            x = int(center[0] + r * np.cos(angle))
            y = int(center[1] - r * np.sin(angle))
            points.append((x, y))
            angle += 0.1

        for i in range(len(points) - 1):
            cv2.line(image, points[i], points[i + 1], (0, 255, 0), 2)


    image = cv2.imread(image_path)
    height, width, _ = image.shape

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
        results = face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                left_cheek = face_landmarks.landmark[234]
                right_cheek = face_landmarks.landmark[454]
                chin = face_landmarks.landmark[152]
                forehead = face_landmarks.landmark[10]
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                left_x, left_y = int(left_cheek.x * width), int(left_cheek.y * height)
                right_x, right_y = int(right_cheek.x * width), int(right_cheek.y * height)
                chin_x, chin_y = int(chin.x * width), int(chin.y * height)
                forehead_x, forehead_y = int(forehead.x * width), int(forehead.y * height)
                left_eye_x, left_eye_y = int(left_eye.x * width), int(left_eye.y * height)
                right_eye_x, right_eye_y = int(right_eye.x * width), int(right_eye.y * height)

                face_length = abs(right_x - left_x)
                face_height = abs(chin_y - forehead_y)

                print(f"Face Length: {face_length} pixels")
                print(f"Face Height: {face_height} pixels")

                cv2.circle(image, (left_x, left_y), 5, (0, 255, 0), -1)
                cv2.circle(image, (right_x, right_y), 5, (0, 255, 0), -1)
                cv2.circle(image, (chin_x, chin_y), 5, (0, 255, 0), -1)
                cv2.circle(image, (forehead_x, forehead_y), 5, (0, 255, 0), -1)

                if face_length > face_height:
                    golden_height = int(face_length / 1.618)
                    golden_width = face_length
                else:
                    golden_width = int(face_height * 1.618)
                    golden_height = face_height

                center_x = (left_x + right_x) // 2
                center_y = (forehead_y + chin_y) // 2
                top_left_x = center_x - golden_width // 2
                top_left_y = center_y - golden_height // 2
                bottom_right_x = center_x + golden_width // 2
                bottom_right_y = center_y + golden_height // 2

                cv2.rectangle(image, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 2)

                eye_center_x = (left_eye_x + right_eye_x) // 2
                eye_center_y = (left_eye_y + right_eye_y) // 2

                draw_golden_spiral(image, (eye_center_x, eye_center_y), scale=5)

    cv2.imwrite(image_path, image)