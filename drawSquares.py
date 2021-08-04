#Finds the vertical location of the blocks in a pre warped image
#Note: each column is 7 wide and 89 down

from PIL import Image, ImageDraw
import cv2
import numpy as np
import utlis as utlis

img = Image.open('myImage0.jpg')
d = ImageDraw.Draw(img) # used for drawing the lines later

width, height = img.size
# print(width, height)
image= cv2.imread("myImage0.jpg")

legoNumY = 21
legoNumX = 10

# find horizontal lines
locationY = height*7/94
stepY = height*4/90
#nex = location + step
coordinatesY = [locationY]

for i in range(legoNumY):
    d.line([(0,locationY),(width,locationY)], fill=(0,0,255), width=2)
    locationY += stepY
    coordinatesY.append(locationY)

# find vertical lines
locationX = width*8.5/100
stepX1 = width*7/100
stepX2 = width*11.8/100
coordinatesX = [locationX]

for i in range(legoNumX):
    if i % 2 ==0:
        d.line([(locationX,0),(locationX,height)], fill=(0,0,255), width=2)
        locationX += stepX1
        coordinatesX.append(locationX)
    else:
         d.line([(locationX,0),(locationX,height)], fill=(0,0,255), width=2)
         locationX += stepX2
         coordinatesX.append(locationX)
        
    

img.show()
