#### Code to warp an image
### from computervisionzone

from PIL import Image
import cv2
import numpy as np
import utlis as utlis
from utils.colorutils import get_dominant_color
from utlis import colordifference
from ProjectColorIdentify import projectColorIdentify
from gridsplitanddetect import gridsplitanddetect

###############################################################

gridsplitanddetect()
pathImage = "Scanned/myImage0.jpg"
img = cv2.imread(pathImage)

heightImg = 1000
widthImg  = 1000
thres = 20,70
kernel = np.ones((5, 5))

img = cv2.resize(img, (widthImg, heightImg))
projectColors = projectColorIdentify()
projects = ["lightGreen","darkGreen","lightBlue","darkgreen","brown","darkBlue","purple"]

########################################################################
 
utlis.initializeTrackbars()
count=0
 
if 0 == 0:
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    # thres=utlis.valTrackbars() # GET TRACK BAR VALUES FOR THRESHOLDS
    imgThreshold = cv2.Canny(imgBlur,thres[0],thres[1]) # APPLY CANNY BLUR
    imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # APPLY DILATION
    imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
 
    ## FIND ALL COUNTOURS
    imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
    contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # FIND ALL CONTOURS
    cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
 
 
    # FIND THE BIGGEST COUNTOUR
    biggest, maxArea = utlis.biggestContour(contours) # FIND THE BIGGEST CONTOUR

    #biggest = np.array([[[10, 48]],[[102, 48]],[[10, 82]],[[102, 82]]]) #got rid of this, what should it do?
    if biggest.size != 0:
        biggest=utlis.reorder(biggest)
        cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
        imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
 
        # APPLY ADAPTIVE THRESHOLD
        imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
        imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
        imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)
        imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)
 
        # Image Array for Display
        imageArray = ([img,imgGray,imgThreshold,imgContours],
                      [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])
 
    else:
        imageArray = ([img,imgGray,imgThreshold,imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])
 
    xcoordinatecol1 = 19.0 / 1599.0 * widthImg
    blockwidth = 70.0 / 1599.0 * widthImg
    blockwidthsep = 70.0 / 1599.0 * widthImg
    blocksepcol = 126.0 / 1599.0 * widthImg
    ycoordinaterow1 = 40 / 1200.0 * heightImg
    blockheight = 20.0 / 1200.0 * heightImg
    blockheightsep = 37 / 1200.0 * heightImg

    blockrightone = np.array([[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]]])
    blockjumpcolumn = np.array([[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]]])
    blockdownone = np.array([[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]]])

    rowdownone = []

    for i in [1,2,3,4,5,6,7,8,9,10]:
        rowdownone.append(blockdownone)

    rowdownone = np.array(rowdownone)

    firstrowcoordinates = np.zeros(10)
    firstrowcoordinates = [blockdownone,blockdownone,blockdownone,blockdownone,blockdownone,blockdownone,blockdownone,blockdownone,blockdownone,blockdownone]
    for i in [0,2,4,6,8]:
        firstrowcoordinates[i] = [[[xcoordinatecol1, ycoordinaterow1]],[[xcoordinatecol1 + blockwidth, ycoordinaterow1]],[[xcoordinatecol1, ycoordinaterow1 + blockheight]],[[xcoordinatecol1 + blockwidth, ycoordinaterow1 + blockheight]]] + 0.5* i * blockrightone + 0.5 * i * blockjumpcolumn

    for i in [1,3,5,7,9]:
        firstrowcoordinates[i] = firstrowcoordinates[i-1] + blockrightone

    firstrowcoordinates = np.array(firstrowcoordinates)

    coordinategrid = []

    for i in range(0,21,1):
        coordinategrid.append(firstrowcoordinates + i * rowdownone)

    coordinategrid = np.round(np.array(coordinategrid)).astype(int)

    for i in range(0,21,1):
        for k in range(0,10,1):
            imgBigContour = utlis.drawRectangle(imgBigContour,np.array(coordinategrid[i][k]),2)
            biggest = np.array(coordinategrid[i][k])
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(50,50))
            cv2.imwrite("Scanned/myImage("+str(i)+","+str(k)+").jpg",imgWarpColored)
#####
            
    for i in range(21):
        for k in range(10):
            #print(coordinategrid[i][k])
            imgBigContour = utlis.drawRectangle(imgBigContour, np.array(coordinategrid[i][k]), 2)
    blocks = np.array([[[10, 48]], [[102, 48]], [[10, 82]], [[102, 82]]])
    imgBigContour = utlis.drawRectangle(imgBigContour, blocks, 2)
    cv2.imwrite("Funtest.jpg", imgBigContour)
    image = Image.open("Funtest.jpg")
    image.show()
    
#####
    blocks = np.array([[[10, 48]],[[102, 48]],[[10, 82]],[[102, 82]]])
    imgBigContour = utlis.drawRectangle(imgBigContour,blocks,2)
    #cv2.imwrite("Funtest.jpg",imgBigContour)

# using get dominant colour to output dominant colour for each squre- nice output
allColors = []

if 0 == 0:
    for i in range(0,21,1):
        for k in range(0,10,1):
            imgBigContour = utlis.drawRectangle(imgBigContour,np.array(coordinategrid[i][k]),2)
            biggest = np.array(coordinategrid[i][k])
            pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
            imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
            imgWarpColored = cv2.resize(imgWarpColored,(50,50))

            hsv_image = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2HSV)

            # extract dominant color
            # (aka the centroid of the most popular k means cluster)
            dom_color = get_dominant_color(hsv_image, k=3)
            allColors.append(dom_color)

            
            # create a square showing dominant color of equal size to input image
            dom_color_hsv = np.full(imgWarpColored.shape, dom_color, dtype='uint8')
            # convert to bgr color space for display
            dom_color_bgr = cv2.cvtColor(dom_color_hsv, cv2.COLOR_HSV2BGR)
            
            if k == 0:
                output_image = dom_color_bgr
            else:
                # concat input image and dom color square side by side for display
                output_image = np.hstack((output_image, dom_color_bgr))
          
        if i == 0:
            final_image = output_image
        else:
            final_image = np.vstack((final_image,output_image))
        # show results to screen
    #cv2.imshow('Image Dominant Color', final_image)
    #cv2.waitKey(0)

calendarNames = []
for i in range(len(allColors)):
    index = colordifference(allColors[i],projectcolors)
    calendarNames.append(projects[index])
    
#### define project colours
print(calendarNames)





