import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

def detect_pose(video_path):
    
    cap = cv2.VideoCapture(video_path)

    with mp_pose.Pose() as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

    cap.release()

    return "Pose detection completed"
