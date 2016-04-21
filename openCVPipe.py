__author__ = 'luke'


import cv2
import sys

video_capture = cv2.VideoCapture(r'fifo')
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    if ret == False:
        pass

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()