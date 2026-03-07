import cv2
import mediapipe as mp
import numpy as np

VIDEO_PATH = "dataset/virat_kohli/cover_drive.mp4"

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(VIDEO_PATH)

pose_frames = []

while True:

    ret, frame = cap.read()

    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    if results.pose_landmarks:

        landmarks = []

        for lm in results.pose_landmarks.landmark:
            landmarks.append([lm.x, lm.y])

        pose_frames.append(landmarks)

cap.release()

pose_frames = np.array(pose_frames)

np.save("dataset/virat_pose.npy", pose_frames)

print("Virat pose dataset created")