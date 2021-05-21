import cv2
import mediapipe as mp
import time
import math


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_face_mesh = mp.solutions.face_mesh
hand_states = []


def get_euclidean_distance(pos_a, pos_b):
    return math.sqrt((pos_a.x - pos_b.x) ** 2 + (pos_a.y - pos_b.y) ** 2)


def is_thumb_near_index_finger(thumb_pos, index_pos):
    return get_euclidean_distance(thumb_pos, index_pos) < 0.1


def get_hand_state(hand_landmarks):
    global hand_states

    thumb_is_open = False
    index_is_open = False
    middel_is_open = False
    ring_is_open = False
    pinky_is_open = False
    pseudo_fix_key_point = hand_landmarks[2].x
    state = None

    if (
        hand_landmarks[3].x < pseudo_fix_key_point
        and hand_landmarks[4].x < pseudo_fix_key_point
    ):
        thumb_is_open = True

    pseudo_fix_key_point = hand_landmarks[6].y

    if (
        hand_landmarks[7].y < pseudo_fix_key_point
        and hand_landmarks[8].y < pseudo_fix_key_point
    ):
        index_is_open = True

    pseudo_fix_key_point = hand_landmarks[10].y

    if (
        hand_landmarks[11].y < pseudo_fix_key_point
        and hand_landmarks[12].y < pseudo_fix_key_point
    ):
        middel_is_open = True

    pseudo_fix_key_point = hand_landmarks[14].y

    if (
        hand_landmarks[15].y < pseudo_fix_key_point
        and hand_landmarks[16].y < pseudo_fix_key_point
    ):
        ring_is_open = True

    pseudo_fix_key_point = hand_landmarks[18].y

    if (
        hand_landmarks[19].y < pseudo_fix_key_point
        and hand_landmarks[20].y < pseudo_fix_key_point
    ):
        pinky_is_open = True
    if (
        thumb_is_open
        and index_is_open
        and middel_is_open
        and ring_is_open
        and pinky_is_open
    ):
        state = "FIVE"
    elif (
        not thumb_is_open
        and index_is_open
        and middel_is_open
        and ring_is_open
        and pinky_is_open
    ):
        state = "FOUR"
    elif (
        not thumb_is_open
        and index_is_open
        and middel_is_open
        and ring_is_open
        and not pinky_is_open
    ):
        state = "THREE"
    elif (
        not thumb_is_open
        and index_is_open
        and middel_is_open
        and not ring_is_open
        and not pinky_is_open
    ):
        state = "TWO"
    elif (
        not thumb_is_open
        and index_is_open
        and not middel_is_open
        and not ring_is_open
        and not pinky_is_open
    ):
        state = "ONE"
    elif (
        not thumb_is_open
        and index_is_open
        and not middel_is_open
        and not ring_is_open
        and pinky_is_open
    ):
        state = "ROCK"
    elif (
        thumb_is_open
        and index_is_open
        and not middel_is_open
        and not ring_is_open
        and pinky_is_open
    ):
        state = "SPIDERMAN"
    elif (
        not thumb_is_open
        and not index_is_open
        and not middel_is_open
        and not ring_is_open
        and not pinky_is_open
    ):
        state = "LIKE"
    elif (
        not index_is_open
        and middel_is_open
        and ring_is_open
        and pinky_is_open
        and is_thumb_near_index_finger(hand_landmarks[4], hand_landmarks[8])
    ):
        state = "OK"
    elif (
        not index_is_open and middel_is_open and not ring_is_open and not pinky_is_open
    ):
        state = "FUCK"

    len_states = len(hand_states)
    state_by_multiple_actions = None

    if len_states > 0:
        last_state = hand_states[len_states - 1]

        if last_state[0] == "FOUR" and state == "LIKE":
            state_by_multiple_actions = "GO"

    if state is not None:
        hand_states.append((state, time.time()))

    if state_by_multiple_actions is not None:
        return state_by_multiple_actions

    return state


def handle_hands(hands, image, debug=True, on_event=None):
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            state = get_hand_state(hand_landmarks.landmark)

            # if state == "LIKE":
            #     draw_text(image,"LIKE", 250, 48)

            if on_event is not None:
                on_event(state)

            if state == "OK":
                if debug:
                    draw_text(image, "OK", 250, 48)

            if state == "FUCK":
                if debug:
                    draw_text(image, "HELLO", 250, 48)

            if state == "GO":
                if debug:
                    draw_text(image, "GO", 250, 48)

            if state == "ONE":
                if debug:
                    draw_text(image, "ONE", 250, 48)

            if state == "TWO":
                if debug:
                    draw_text(image, "TWO", 250, 48)

            if state == "THREE":
                if debug:
                    draw_text(image, "THREE", 250, 48)

            if state == "FOUR":
                if debug:
                    draw_text(image, "FOUR", 250, 48)

            if state == "FIVE":
                if debug:
                    draw_text(image, "FIVE", 250, 48)

            if debug:
                print(state)

            # hand_map = [None] * 21
            #
            # for id, lm in enumerate(hand_landmarks.landmark):
            #     h, w, c = image.shape
            #     cx, cy = int(lm.x * w), int(lm.y * h)
            #     hand_map[id] = (cx, cy)
            #
            # if hand_map[0] is not None:
            #     print(hand_map)


def handle_faces(face_mesh, image, drawing_spec):
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


def draw_text(image, text, x, y):
    cv2.putText(
        image,
        text,
        (x, y),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 255, 255),
    )


def start(debug=True, on_event=None):
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    cap = cv2.VideoCapture(0)
    p_time = 0

    with mp_hands.Hands(
        min_detection_confidence=0.7, min_tracking_confidence=0.7
    ) as hands, mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5, min_tracking_confidence=0.5
    ) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # image = cv2.resize(image, (320, 240))

            handle_hands(hands, image, debug=debug, on_event=on_event)

            if debug:
                handle_faces(face_mesh, image, drawing_spec)

                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                c_time = time.time()
                fps = 1 / (c_time - p_time)
                p_time = c_time

                draw_text(image, f"FPS: {int(fps)}", 0, 24)
                cv2.imshow("Camera", image)

                if cv2.waitKey(5) & 0xFF == 27:
                    break

    cap.release()


def get_hands():
    return mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.4)
