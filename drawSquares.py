#Finds the vertical location of the blocks in a pre warped image
#Note: each column is 7 wide and 89 down

from PIL import Image, ImageDraw
import cv2
import numpy as np
import utlis as utlis

img = Image.open('myImage0.jpg')
imgCV = cv2.imread("myImage0.jpg")

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
        coordinatesX.append((locationX))
    else:
         d.line([(locationX,0),(locationX,height)], fill=(0,0,255), width=2)
         locationX += stepX2
         coordinatesX.append(locationX)
img.show

for i in range(21):
    for k in range(10):
        imCrop = imgCV(locationX[k]:locationX[k]+5,locationY[i]:locationY[i]-5))
        imCrop.save("Scanned/myImage("+str(i)+","+str(k)+").jpg", quality=95)
        
        #imgRect = utlis.drawRectangle(img,locationX[k],locationY[i],2)
        #biggest = np.array(coordinategrid[i][k])
        #pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        #pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        #pts1 = coordinatesX
        #pts2 = coordinatesY
        #matrix = cv2.getPerspectiveTransform(pts1, pts2)
        #imgWarpColored = cv2.warpPerspective(img, matrix, (50, 50))
        #imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        #imgWarpColored = cv2.resize(imgWarpColored,(50,50))
        #cv2.imwrite("Scanned/myImage("+str(i)+","+str(k)+").jpg",imgWarpColored)


