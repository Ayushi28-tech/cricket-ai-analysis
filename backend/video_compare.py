import cv2
import numpy as np
from backend.pose_detection import detect_pose
from sklearn.metrics.pairwise import cosine_similarity

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
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    user_poses = []

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame, landmarks = detect_pose(frame)

        if landmarks:
            user_poses.append(landmarks)

        out.write(frame)

    cap.release()
    out.release()

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

    feedback = "Good cover drive posture"

    if similarity < 60:
        feedback = "Work on front elbow and balance"

    return similarity, feedback, OUTPUT_VIDEO