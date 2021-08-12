##### This contains some code from rasterarray.py, which finds some of the project colors

def projectColorIdentify():

    import cv2
    from utils.colorutils import get_dominant_color

    projectNum = 8
    disty1 = 23
    distybox = 18
    disty2 = disty1 + distybox
    disty = 50
    xleft = 50
    xright = 120
    n = 1
    projectColors = []

    img = cv2.imread("Scanned/myImage2.jpg")

    for i in range(projectNum):
        cv2.rectangle(img,(xleft,disty1),(xright,disty2), (255,0,0),2)
    

        
        cv2.imwrite("Scanned/projectImage("+str(i)+").jpg",img[disty1:disty2,xleft:xright])

        hsv_image = cv2.imread("Scanned/projectImage("+str(i)+").jpg")
        hsv_image = cv2.cvtColor(hsv_image, cv2.COLOR_BGR2HSV)

        dom_color = get_dominant_color(hsv_image, k=3)
        projectColors.append(dom_color)

        disty1 = disty1 + disty
        disty2 = disty1 + distybox

    cv2.imshow("final_image", img)
    cv2.waitKey(0)
    
    return projectColors

#cv2.imshow('Image Dominant Color', final_image)
    #cv2.waitKey(0)

'''
    imgWarpColored = cv2.warpPerspective("Scanned/projectImage("+str(i)+").jpg", matrix, (50, 50))
    imgWarpColored = imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
    imgWarpColored = cv2.resize(imgWarpColored,(50,50))

    hsv_image = cv2.cvtColor("Scanned/projectImage("+str(i)+").jpg", cv2.COLOR_BGR2HSV)
    dom_color = get_dominant_color(hsv_image, k=3)
    projectColors.append(dom_color)
    
    n += 1
'''

#cv2.imshow("Result", img)
#cv2.waitKey()
#print(projectColors)


'''
###############################################################

pathImage = "Scanned/myImage2.jpg"
img = cv2.imread(pathImage)

heightImg = 1000
widthImg  = 1000
thres = 20,70
kernel = np.ones((5, 5))
projectNum = 6
k = 1
coordinategrid = []

img = cv2.resize(img, (widthImg, heightImg))
########################################################################
 
utlis.initializeTrackbars()
count=0
 
if 0 ==0:
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
 
    xcoordinatecol1 = 100.0 / 1599.0 * widthImg
    blockwidth = 70.0 / 1599.0 * widthImg
    blockwidthsep = 40.0 / 1599.0 * widthImg
    blocksepcol = 120.0 / 1599.0 * widthImg
    ycoordinaterow1 = 69. / 1200.0 * heightImg
    blockheight = 20.0 / 1200.0 * heightImg
    blockheightsep = 34 / 1200.0 * heightImg

    blockrightone = np.array([[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]],[[blockwidthsep + blockwidth, 0]]])
    blockjumpcolumn = np.array([[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]],[[blockwidth + blocksepcol, 0]]])
    blockdownone = np.array([[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]],[[0, blockheight + blockheightsep]]])

    rowdownone = []

    for i in range(projectNum):
        coordinategrid.append(ycoordinaterow1 + i *  (blockheightsep + blockheight))

    coordinategrid = np.round(np.array(coordinategrid)).astype(int)

    for i in range(1, projectNum):
        print(i)
        imgBigContour = utlis.drawRectangle(imgBigContour,np.array(coordinategrid[i]),2)
        biggest = np.array(coordinategrid[i])
        pts1 = np.float32(biggest) # PREPARE POINTS FOR WARP
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20]
        imgWarpColored = cv2.resize(imgWarpColored,(50,50))
        cv2.imwrite("Scanned/myImage("+str(i)+","+str(k)+").jpg",imgWarpColored)
#####
            
    for i in range(projectNum):
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
    cv2.imwrite("Funtest.jpg",imgBigContour)

# using get dominant colour to output dominant colour for each squre- nice output
projectColours = []
allColours = []

if 0 ==0:
    for i in range(projectNum):
        if 0 == 0:
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
            allColours.append(projectColours)

            projectColours.append(dom_color)
            
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
    cv2.imshow('Image Dominant Color', final_image)
    cv2.waitKey(0)


#### define project colours
print(projectColours)

'''
