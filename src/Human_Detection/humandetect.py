from PIL import ImageTk, Image
import Tkinter as tk
import cv2
import time
import numpy as np
HEIGHT = 600
WIDTH = 600
root = tk.Tk()
cv_image=""
#find="NOT FOUND"
def pro_image(b):
	pro_img.paste(Image.open("camo.jpg"))
	pro_img.paste(Image.open(b))

def start_func(a):
	MODE = "COCO"
	if MODE is "COCO":
	    protoFile = "pose/coco/pose_deploy_linevec.prototxt"
	    weightsFile = "pose/coco/pose_iter_440000.caffemodel"
	    nPoints = 18
	    POSE_PAIRS = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]

	elif MODE is "MPI" :
	    protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
	    weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
	    nPoints = 15
	    POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]


	frame = cv2.imread(a)
	frameCopy = np.copy(frame)
	frameWidth = frame.shape[1]
	frameHeight = frame.shape[0]
	threshold = 0.1

	net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

	t = time.time()
	inWidth = 368
	inHeight = 368
	inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
	                          (0, 0, 0), swapRB=False, crop=False)

	net.setInput(inpBlob)

	output = net.forward()

	H = output.shape[2]
	W = output.shape[3]

	points = []

	for i in range(nPoints):
	    probMap = output[0, i, :, :]
	    minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
	    x = (frameWidth * point[0]) / W
	    y = (frameHeight * point[1]) / H
	    if prob > threshold :
	        cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
	        cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
	        points.append((int(x), int(y)))
	    else :
	        points.append(None)
	num=0
	for pair in POSE_PAIRS:
	    partA = pair[0]
	    partB = pair[1]
	    if points[partA] and points[partB]:
	        cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
	        cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
	        num+=1
	if num >6:
		result.config(text="FOUND")
	cv_image=a.replace('.jpg','res.jpg')
	cv2.imwrite(cv_image, frame)
	pro_image(cv_image)


def load_image(entry):
	original_img.paste(Image.open("camo.jpg"))
	original_img.paste(Image.open(entry))
	#print('mkb')
	result.config(text="NOT FOUND")
	cv_image=entry
	start_func(cv_image)

root.title("XXX  PEACE KEEPER  XXX")

canvas = tk.Canvas(root,height=HEIGHT,width=WIDTH)
canvas.pack()

bg = Image.open("camo.jpg")
background_image = ImageTk.PhotoImage(bg)
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

top_frame = tk.Frame(root,bg="#071F2D",bd=5)
top_frame.place(relx=0.5,rely=0.03,relwidth=0.9,relheight=0.1,anchor='n')

entry = tk.Entry(top_frame,font=("Courier", 20))
entry.place(relwidth=0.65,relheight=1)

load = tk.Button(top_frame,font=("Courier", 20),text=" LOAD ",bg="#394344",command=lambda:load_image(entry.get()))
load.place(relx=0.68,relwidth=0.32,relheight=1)

img_frame = tk.Frame(root,bg="#071F2D",bd=5)
img_frame.place(relx=0.5,rely=0.15,relwidth=0.9,relheight=0.6,anchor='n')

og = Image.open("camo.jpg")
original_img = ImageTk.PhotoImage(og)
orig_label = tk.Label(img_frame,image=original_img)
orig_label.place(relwidth=0.5,relheight=1)

pro = Image.open("camo.jpg")
pro_img = ImageTk.PhotoImage(pro)
pro_label = tk.Label(img_frame,image=pro_img,bg="red")
pro_label.place(relx=0.52,relwidth=0.48,relheight=1)

label1 = tk.Label(root,bg="#54625B",fg="white",text="Original",font=("Courier", 20))
label1.place(relx=0.05,rely=0.75,relwidth=0.45,relheight=0.05)

label2 = tk.Label(root,bg="#54625B",fg="white",text="Processed",font=("Courier", 20))
label2.place(relx=0.52,rely=0.75,relwidth=0.43,relheight=0.05)

result = tk.Label(root,text="NOT FOUND",font=("Courier", 20),bg="#091823",fg="white")
result.place(relx=0.5,rely=0.9,relwidth=0.5,relheight=0.05,anchor='n')

root.mainloop()
