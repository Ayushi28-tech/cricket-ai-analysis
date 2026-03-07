import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def detect_pose(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    landmarks_list = []

    if results.pose_landmarks:

        for landmark in results.pose_landmarks.landmark:

            h, w, _ = frame.shape
            cx = int(landmark.x * w)
            cy = int(landmark.y * h)

            landmarks_list.append([landmark.x, landmark.y])

            cv2.circle(frame,(cx,cy),5,(0,255,0),-1)

    return frame, landmarks_list