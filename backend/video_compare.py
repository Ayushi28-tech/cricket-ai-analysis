import cv2
import numpy as np
from backend.pose_detection import detect_pose
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter

OUTPUT_VIDEO = "output/result.mp4"

# load virat pose dataset
virat_pose = np.load("dataset/virat_pose.npy")

def compare_videos(user_video):

    cap = cv2.VideoCapture(user_video)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    out = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*'avc1'),
        fps,
        (width, height)
    )

    user_poses = []
    feedback_list = []
    bat_positions = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break
    
        frame, landmarks = detect_pose(frame)

        if landmarks:
            user_poses.append(landmarks)

            try:
                feedback_list.append(elbow_feedback(landmarks))
                feedback_list.append(head_position_feedback(landmarks))
            except:
                pass
            
            # bat wrist position store
            try:
                bat_y = landmarks[16][1]
                bat_positions.append(bat_y)
            except:
                pass

        # add watermark
        h, w = frame.shape[:2]

        cv2.rectangle(frame,(10,10),(300,60),(0,0,0),-1)

        cv2.putText(
            frame,
            "AI Cricket Analyzer",
            (20,45),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            2,
            cv2.LINE_AA
        )

        out.write(frame)

    cap.release()
    out.release()
    
    # Shot Phase Detection
    phases = []

    if len(bat_positions) > 10:

        start = bat_positions[0]
        mid = bat_positions[len(bat_positions)//2]
        end = bat_positions[-1]

        if mid < start:
            phases.append("Backlift detected")

        if mid > start:
            phases.append("Downswing detected")

        phases.append("Impact phase detected")

        if end > mid:
            phases.append("Follow Through detected")

    # convert to numpy
    user_poses = np.array(user_poses)

    if len(user_poses) == 0:
        similarity = 0
    else:

        user_flat = user_poses.reshape(len(user_poses), -1)
        virat_flat = virat_pose.reshape(len(virat_pose), -1)

        min_len = min(len(user_flat), len(virat_flat))

        user_flat = user_flat[:min_len]
        virat_flat = virat_flat[:min_len]

        sim = cosine_similarity(user_flat, virat_flat)

        similarity = int(sim.mean() * 100)

    feedback = list(set(feedback_list))

    if len(feedback_list) > 0:

        count = Counter(feedback_list)

        elbow_good = count["Good elbow position"]
        elbow_bad = count["Front elbow too low"]

        head_good = count["Head position stable"]
        head_bad = count["Head falling sideways"]

        feedback = []

        if elbow_bad > elbow_good:
            feedback.append("Front elbow too low")
        else:
            feedback.append("Good elbow position")

        if head_bad > head_good:
            feedback.append("Head falling sideways")
        else:
            feedback.append("Head position stable")

    else:
        feedback = ["Good cover drive posture"]

    return similarity, feedback, phases, OUTPUT_VIDEO

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ba = a - b
    bc = c - b

    cosine = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))

    return angle

def elbow_feedback(landmarks):

    shoulder = landmarks[12]
    elbow = landmarks[14]
    wrist = landmarks[16]

    angle = calculate_angle(shoulder, elbow, wrist)

    if angle < 140:
        return "Front elbow too low"
    else:
        return "Good elbow position"


def head_position_feedback(landmarks):

    nose_x = landmarks[0][0]
    hip_x = landmarks[24][0]

    if abs(nose_x - hip_x) > 0.1:
        return "Head falling sideways"
    else:
        return "Head position stable"