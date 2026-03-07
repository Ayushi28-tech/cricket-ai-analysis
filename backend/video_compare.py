import cv2
from backend.pose_detection import detect_pose

OUTPUT_VIDEO = "uploads/result.mp4"

def compare_videos(user_video):

    cap = cv2.VideoCapture(user_video)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5)

    out = cv2.VideoWriter(
        OUTPUT_VIDEO,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = detect_pose(frame)

        out.write(frame)

        frames += 1

    cap.release()
    out.release()

    similarity = 80
    feedback = "Good shot posture but front elbow slightly low"

    return similarity, feedback, OUTPUT_VIDEO
