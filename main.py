import cv2
import time
from emailing import send_email, clean_folder
import glob
from threading import Thread
import os

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()
    # transfer to gray from colour for reduce data
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    # Gaussian blur to reduce data even more
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # storing the first frame for comparison
    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta_frame,
                                 50,
                                 255,
                                 cv2.THRESH_BINARY)[1]
    # remove noise
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame,
                                       cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame,
                                  (x, y),
                                  (x + w, y + h),
                                  (0, 255, 0),
                                  3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images\\{count}.png", frame)
            count += 1
            all_images = sorted(glob.glob("images\\*.png"))
            index_of_img_to_send = int(len(all_images) / 2)
            image_to_send = all_images[index_of_img_to_send]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        img_to_delete = sorted(glob.glob("images\\*.png"))
        for img in img_to_delete:
            if img != image_to_send:
                os.remove(img)
        email_thread = Thread(target=send_email, args=(image_to_send,))
        email_thread.daemon = True

        email_thread.start()

    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()


