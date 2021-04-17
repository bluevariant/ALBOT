import cv2
import mediapipe as mp
import time


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh


def handle_hands(hands, image):
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                print(id, cx, cy)


def handle_faces(face_mesh, image):
    image.flags.writeable = False
    results = face_mesh.process(image)
    image.flags.writeable = True

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACE_CONNECTIONS,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec,
            )


if __name__ == "__main__":
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    cap = cv2.VideoCapture(0)
    p_time = 0

    with mp_hands.Hands(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as hands, mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            handle_hands(hands, image)
            handle_faces(face_mesh, image)

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            c_time = time.time()
            fps = 1 / (c_time - p_time)
            p_time = c_time

            cv2.putText(
                image,
                f"FPS: {int(fps)}",
                (0, 24),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 255, 255),
            )
            cv2.imshow("Camera", image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
