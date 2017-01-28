import cv2
import time
from selectors import BoxSelector
from trackers import CamshiftTracker,CorrelationTracker
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v","--video",help="(optional) video file...")
ap.add_argument("-t","--tracker",default="camshift",help="tracker to use (camshift/correlation)")
args = vars(ap.parse_args())

#initialize the capure
if args.get("video",None):
    cap = cv2.VideoCapture(args["video"])
else:
    cap = cv2.VideoCapture(0)

trackers = {"camshift":CamshiftTracker,"correlation":CorrelationTracker}
objTracker = None

while True:
    ret,frame = cap.read()
    time.sleep(0.025)
    if not ret:
        break

    image = frame
    bs = BoxSelector(image, "Stream")
    cv2.imshow("Stream",image)
    key = cv2.waitKey(1) & 0xFF

    if key==ord("p"):
        key = cv2.waitKey(0) & 0xFF
        bs_pts = bs.roiPts

        if key==ord("p") and bs_pts:
            objTracker = trackers[args["tracker"].strip().lower()](bs_pts)

    elif key==ord("q"):
        break

    if objTracker is not None:
        trackPts = objTracker.track(image)
        (x,y,w,h) = trackPts
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imshow("Detected",image)



