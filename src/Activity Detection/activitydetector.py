# import the necessary packages
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
from pygame import mixer # Load the required library
from time import sleep
HEIGHT = 800
WIDTH = 800
class ActivityDetector:



	def __init__(self, vs, outputPath):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		mixer.init()
		mixer.music.load('res/buzzzer.mp3')
		self.fgbg = cv2.createBackgroundSubtractorMOG2()
		self.vs = vs
		self.outputPath = outputPath
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.activity="No Activity"
		self.sound_running = False
		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None

		# create a button, that when pressed, will take the current
		# frame and save it to file

		# btn = tki.Button(self.root, text="Snapshot!",
		# 	command=self.takeSnapshot)
		# btn.pack(side="bottom", fill="both", expand="yes", padx=10,
		# 	pady=10)

		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()

		# set a callback to handle when the window is closed
		self.root.wm_title("XXX  PEACE KEEPER  XXX")
		self.canvas = tki.Canvas(self.root,height=HEIGHT,width=WIDTH)
		self.canvas.pack()

		self.background_image = tki.PhotoImage(file="res/camo.PPM")
		self.background_label = tki.Label(self.root, image=self.background_image)
		self.background_label.place(relwidth=1, relheight=1)

		self.button_frame = tki.Frame(self.root,bg="#091722",bd=5)
		self.button_frame.place(relx=0.7,rely=0.05,relwidth=0.25,relheight=0.1)

		self.on = tki.Button(self.button_frame,text = " ON ", bg="#54625B", fg="white",highlightbackground="#54625B",command=lambda:self.on_func())
		self.on.place(relwidth=0.5,relheight=1)
		self.off = tki.Button(self.button_frame,text = " OFF ", bg="#54625B", fg="white",highlightbackground="#54625B",command=lambda:self.off_func())
		self.off.place(relx=0.5,relwidth=0.5,relheight=1)

		self.status = tki.Label(self.root,text=" Status ",font=("Courier", 25),bg="#071F2D",fg="white")
		self.status.place(relx=0.7,rely=0.2,relwidth=0.25,relheight=0.1)

		self.stati_frame = tki.Frame(self.root,bg="#091722",bd=5)
		self.stati_frame.place(relx=0.7,rely=0.3,relwidth=0.25,relheight=0.1)

		self.stati_label = tki.Label(self.stati_frame,bg="#8D978E",fg="#6BF688",text="Active",font=("Courier", 25))
		self.stati_label.place(relwidth=1,relheight=1)

		self.gps_frame = tki.Frame(self.root,bg="#091722")
		self.gps_frame.place(relx=0.05,rely=0.6,relwidth=0.5,relheight=0.3)

		self.gps_label = tki.Label(self.gps_frame,text="No Activity",fg="red",font=("Courier", 40),bg="#091722")
		self.gps_label.place(relwidth=1,relheight=1)

		self.pos = tki.Label(self.root,text="Position",font=("Courier", 20),bg="#091722",fg="white")
		self.pos.place(relx=0.68,rely=0.55,relwidth=0.3,relheight=0.1)

		self.lat_frame = tki.Frame(self.root,bg="#091722",bd=5)
		self.lat_frame.place(relx=0.68,rely=0.65,relwidth=0.3,relheight=0.1)

		self.lat_label = tki.Label(self.lat_frame,bg="#7B857B",text="Latitude: 78.9080980",font=("Courier", 25))
		self.lat_label.place(relwidth=1,relheight=1)

		self.lon_frame = tki.Frame(self.root,bg="#091722",bd=5)
		self.lon_frame.place(relx=0.68,rely=0.745,relwidth=0.3,relheight=0.1)

		self.lon_label = tki.Label(self.lon_frame,bg="#7B857B",text="Longitude: 67.0989080",font=("Courier", 25))
		self.lon_label.place(relwidth=1,relheight=1)

		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

	def on_func(self):
		print("Status: Active")
		self.stati_label.config(text="Active")
		self.stati_label.config(fg="#6BF688")

	def off_func(self):
		print("Status: Inactive")
		self.stati_label.config(text="Inactive")
		self.stati_label.config(fg="red")

	def activity_detection(self):
		self.gps_label.config(text=self.activity)

	def videoLoop(self):
		# DISCLAIMER:
		# I'm not a GUI developer, nor do I even pretend to be. This
		# try/except statement is a pretty ugly hack to get around
		# a RunTime error that Tkinter throws due to threading
		try:
			# keep looping over frames until we are instructed to stop
			while not self.stopEvent.is_set():
				# grab the frame from the video stream and resize it to
				# have a maximum width of 300 pixels
				self.frame = self.vs.read()
				self.frame = imutils.resize(self.frame, width=690)

				# OpenCV represents images in BGR order; however PIL
				# represents images in RGB order, so we need to swap
				# the channels, then convert to PIL and ImageTk format
				image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
				image = Image.fromarray(image)
				image = ImageTk.PhotoImage(image)
				frame = self.vs.read()
				img = cv2.resize(frame,(256,144))
				fgmask = self.fgbg.apply(img)
				s=0
				for vec in fgmask:
					for white in vec:
						if white==255:
						   s=s+1
				print(s)
				if s>2500:
					self.activity="Activity Detected"
					cv2.imwrite('detected/'+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'.jpg',frame)
					if not self.sound_running:
						mixer.music.play()
						self.sound_running=True
				else:
					self.activity="No Activity Detected"
					if self.sound_running:
						mixer.music.stop()
						self.sound_running=False

				self.activity_detection()
				#    cv.imshow('frame',frame)
				k = cv2.waitKey(30) & 0xff
				if k == 27:
					break
				# if the panel is not None, we need to initialize it
				if self.panel is None:
					self.panel = tki.Label(image=image,bg="#091823")
					self.panel.image = image
					self.panel.place(relx=0.05,rely=0.05,relwidth=0.5,relheight=0.5)

				# otherwise, simply update the panel
				else:
					self.panel.configure(image=image)
					self.panel.image = image

		except RuntimeError, e:
			print("[INFO] caught a RuntimeError")

	def onClose(self):
		# set the stop event, cleanup the camera, and allow the rest of
		# the quit process to continue
		print("[INFO] closing...")
		self.stopEvent.set()
		self.vs.stop()
		self.root.quit()
