import cv2
import numpy as np
from backend.pose_detection import detect_pose
from sklearn.metrics.pairwise import cosine_similarity
import os

OUTPUT_IMAGE = "output/result.jpg"

# reference image load (example: virat kohli)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref_path = os.path.join(BASE_DIR, "dataset", "kohli.jpg")

ref_img = cv2.imread(ref_path)

def compare_images(user_image):

    user = cv2.imread(user_image)

    user_frame, user_landmarks = detect_pose(user)
    ref_frame, ref_landmarks = detect_pose(ref_img)

    if user is None:
        return 0, OUTPUT_IMAGE

    if ref_img is None:
        print("ERROR: kohli.jpg not loaded")
        return 0, OUTPUT_IMAGE

    if user_landmarks is None or len(user_landmarks) == 0:
        return 0, OUTPUT_IMAGE

    if ref_landmarks is None or len(ref_landmarks) == 0:
        return 0, OUTPUT_IMAGE
    
    user_flat = np.array(user_landmarks).flatten().reshape(1, -1)
    ref_flat = np.array(ref_landmarks).flatten().reshape(1, -1)

    similarity = int(cosine_similarity(user_flat, ref_flat)[0][0] * 100)

    # side-by-side image
    h = min(user_frame.shape[0], ref_frame.shape[0])

    user_frame = cv2.resize(user_frame, (int(user_frame.shape[1] * h / user_frame.shape[0]), h))
    ref_frame = cv2.resize(ref_frame, (int(ref_frame.shape[1] * h / ref_frame.shape[0]), h))

    combined = np.hstack((user_frame, ref_frame))
    
    top_space = 80   # space height

    h, w = combined.shape[:2]

    # black strip add on top
    new_img = np.zeros((h + top_space, w, 3), dtype=np.uint8)

    # original image ko neeche shift karo
    new_img[top_space:top_space+h, 0:w] = combined

    combined = new_img

    # main text
    h_total, w_total = combined.shape[:2]

    font = cv2.FONT_HERSHEY_SIMPLEX

    # 🔹 AI Match (center, SMALL)
    text_main = f"AI Match: {similarity}%"
    scale_main = 0.8
    thickness_main = 2

    (text_w, text_h), _ = cv2.getTextSize(text_main, font, scale_main, thickness_main)

    x_main = (w_total - text_w) // 2
    y_main = 30   # inside black space

    cv2.putText(combined, text_main, (x_main, y_main),
        font, scale_main, (0,255,0), thickness_main)

    # Compared with (VISIBLE COLOR)
    text_sub = "Compared with Kohli"
    scale_sub = 0.6
    thickness_sub = 2

    (text_w2, text_h2), _ = cv2.getTextSize(text_sub, font, scale_sub, thickness_sub)

    x_sub = (w_total - text_w2) // 2
    y_sub = 60

    cv2.putText(combined, text_sub, (x_sub, y_sub),
        font, scale_sub, (0,255,255), thickness_sub)

    # Bottom Right Watermark
    watermark = "AI Cricket Analysis"
    scale_wm = 0.5
    thickness_wm = 1

    (text_wm, text_hm), _ = cv2.getTextSize(watermark, font, scale_wm, thickness_wm)

    x_wm = w_total - text_wm - 10
    y_wm = h_total - 10

    cv2.putText(combined, watermark, (x_wm, y_wm),
        font, scale_wm, (180,180,180), thickness_wm)
        
    cv2.imwrite(OUTPUT_IMAGE, combined)

    return similarity, OUTPUT_IMAGE