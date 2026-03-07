import cv2
from backend.pose_detection import detect_pose

def compare_videos(user_video, reference_video):

    cap1 = cv2.VideoCapture(user_video)
    cap2 = cv2.VideoCapture(reference_video)

    while True:

        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        frame1 = cv2.resize(frame1,(640,480))
        frame2 = cv2.resize(frame2,(640,480))

        frame1 = detect_pose(frame1)
        frame2 = detect_pose(frame2)

        combined = cv2.hconcat([frame1, frame2])

        cv2.imshow("Cricket Shot Comparison", combined)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
