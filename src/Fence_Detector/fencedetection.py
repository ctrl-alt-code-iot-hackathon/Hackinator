from PIL import ImageTk, Image
import Tkinter as tk
import cv2
import numpy as np
from matplotlib import pyplot as plt


HEIGHT = 600
WIDTH = 600
root = tk.Tk()

def pro_image(b):
	pro_img.paste(Image.open("camo.jpg"))
	pro_img.paste(Image.open(b))

def start_detection(images):
	result.config(text="NO BREAKAGE")
	img = cv2.imread(images)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	edges = cv2.GaussianBlur(edges,(5,5),0)

	k_square = np.ones((5,5),np.uint8)
	k_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	thresh = cv2.dilate(edges,k_ellipse,iterations=1)
	thresh = cv2.erode(thresh,k_square,iterations=2)
	minLineLength = 100
	maxLineGap = 10
	lines = cv2.HoughLinesP(thresh,1,np.pi/180,100,minLineLength,maxLineGap)
	x_sum = cv2.reduce(thresh, 0, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
	y_sum = cv2.reduce(thresh, 1, cv2.REDUCE_SUM, dtype=cv2.CV_32S)
	if lines is not None:
	    for line in lines:
	        for x1,y1,x2,y2 in line:
	            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

	h=img.shape[0]
	w= img.shape[1]
	flag1=0
	flag2=0
	flag3=0
	count = 0
	n=0
	p=0
	for i in range(0,h-5,5):
	    flag1=0
	    flag2=0
	    flag3=0
	    for j in range(0,w-5,5):
	        count=0;
	        for k in range(i,i+5):
		        for l in range(j,j+5):
		            p=n
		            if img[k][l][0]==0 and img[k][l][1]==255 and img[k][l][2]==0:
				        n=j
				        #count=count+1
				        #print(i,"    ",j,"    ",img[k][l]," ")
	                if (n-p)>30:
				        flag3=1
				        break

	    if flag3==1:
	        break

	if flag3==1:
		result.config(text="BREAKAGE DETECTED")
	ima=images.replace('.jpg','res.jpg')
	cv2.imwrite(ima,img)
	pro_image(ima)

def load_image(entry):
	pro_img.paste(Image.open("camo.jpg"))
	original_img.paste(Image.open(entry))
	start_detection(entry)

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

result = tk.Label(root,text="Not Found",font=("Courier", 20),bg="#091823",fg="white")
result.place(relx=0.5,rely=0.85	,relwidth=0.5,relheight=0.05,anchor='n')

root.mainloop()
