from __future__ import print_function
from activitydetector import ActivityDetector
from imutils.video import VideoStream
import argparse
import time
import os
from threading import Thread


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=True,
	help="path to output directory to store snapshots")
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
def gg(vs,args):
    bg.test(args,vs)

print("[INFO] warming up camera...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(1.0)
Thread(target=ActivityDetector(vs, args["output"]).root.mainloop(),args=()).start()
