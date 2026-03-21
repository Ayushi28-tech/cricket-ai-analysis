import cv2
import numpy as np
from backend.pose_detection import detect_pose
from sklearn.metrics.pairwise import cosine_similarity

OUTPUT_IMAGE = "output/result.jpg"

# reference image load (example: virat kohli)
ref_img = cv2.imread("dataset/kohli.jpg")

def compare_images(user_image):

    user = cv2.imread(user_image)

    user_frame, user_landmarks = detect_pose(user)
    ref_frame, ref_landmarks = detect_pose(ref_img)
    if ref_img is None:
        print("ERROR: kohli.jpg not loaded")
        
    if user_landmarks is None or len(user_landmarks) == 0:
        return 0, OUTPUT_IMAGE

    if ref_landmarks is None or len(ref_landmarks) == 0:
        return 0, OUTPUT_IMAGE
    
    user_flat = np.array(user_landmarks).flatten().reshape(1, -1)
    ref_flat = np.array(ref_landmarks).flatten().reshape(1, -1)

    similarity = int(cosine_similarity(user_flat, ref_flat)[0][0] * 100)

    # side-by-side image
    combined = np.hstack((user_frame, ref_frame))

    cv2.putText(combined, f"Match: {similarity}%", (50,50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imwrite(OUTPUT_IMAGE, combined)

    return similarity, OUTPUT_IMAGE