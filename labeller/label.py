import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse

def showimg(img,name="s"):
    if (args.showbbox):
        show=True
        print"will show plots"
        plt.imshow(img)
        plt.show()
    else :
        show=False



# In[3]:
def update(labelfile,x):
    a=False
    try:
        text_file = open("labels/"+labelfile+".txt", "a")
        a=True
    except:
        text_file = open(labelfile+".txt", "w")

    if a:
        text_file.write(x+"\n")
    else:
        text_file.write(x+"\n")
    text_file.close()


def findcords(img,template,method):
    w, h = template.shape[::-1]
    img_copy=img.copy()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    method = eval(method)
    # Apply template Matching
    res = cv2.matchTemplate(img_rgb,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

################COODR LABEL FILE #######################
    x= "plate 0 0 0 "+(str)(top_left[0]-5)+' '+(str)(top_left[1]-5)+' '+(str)(bottom_right[0]+5)+' '+(str)(bottom_right[1]+5) +" 0 0 0 0 0 0 0 0"  
    x= "plate 0 0 0 "+(str)(top_left[0])+' '+(str)(top_left[1])+' '+(str)(bottom_right[0])+' '+(str)(bottom_right[1]) +" 0 0 0 0 0 0 0 0"  

################END COODR LABEL FILE #######################
    cv2.rectangle(img_copy,(top_left[0],top_left[1]), (bottom_right[0],bottom_right[1]), (0,255,0), 2)

    cv2.rectangle(img_copy,(top_left[0]-5,top_left[1]-5), (bottom_right[0]+5,bottom_right[1]+5), (0,0,255), 2)

    showimg(img_copy)
    #cv2.imwrite('res'+meth+'.jpg',ima_rgb)
    return x

# In[4]:

def main(_):
    if not os.path.isdir("labels"):
        os.mkdir("labels")
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']


    i=0
    for filename in os.listdir("_2 image/"):
        if filename.endswith(".png") or filename.endswith(".jpg"): 
            l= os.path.join("_2 image/", filename)
            id= filename.split('_')[0]
            imgtobelabeled=cv2.imread(l)
            tempatetobematched=cv2.imread("cropped/"+id+"_cropped.jpg",0)
            try:
                coords=findcords(imgtobelabeled,tempatetobematched,methods[1])
            except:
                print "Error detected at image id :",id
                print imgtobelabeled.shape
                print tempatetobematched.shape
            #print coords
            labelfile=id+'_2'
            update(labelfile,coords)
            i=i+1
            if i%500 == 0: 
                print "processed ",i," images"
        else:

            continue

ap = argparse.ArgumentParser()
ap.add_argument("--showbbox",required = False,action="store_true",help = "Show each image with the bbox in it ")
args = (ap.parse_args())
main(args)