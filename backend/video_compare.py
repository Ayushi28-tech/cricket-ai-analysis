import cv2

def compare_videos(user_video, pro_video):

    cap1 = cv2.VideoCapture(user_video)
    cap2 = cv2.VideoCapture(pro_video)

    print("Comparing videos...")

    cap1.release()
    cap2.release()

    return "Comparison completed"
