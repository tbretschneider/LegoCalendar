#!/usr/bin/python

# import the necessary packages
import numpy as np
import cv2

def main():
    # define the boundaries as HSV
    # these will need tweaking for the specific colours needed
    boundaries=(((15, 20, 20), (35, 255, 255)), #yellow
                ((36, 20, 20), (80, 255, 255)), #green
                ((81, 50, 50), (155, 255, 255)), #blue
                )

    #kernel for removing tiny islands
    #increse values to remove larger islands, decrease if relevant blocks are being removed
    kernelOpen = np.ones((12, 12))
    #kernel for closing gaps
    #increase if blocks have gaps, decrease is blocks are being merged together
    kernelClose = np.ones((3, 3))


    image = cv2.imread('Calendar1.jpg') #load image
    image = cv2.resize(image, (900, 700), interpolation=cv2.INTER_LINEAR)
    #image = cv2.GaussianBlur(image, (5,5), 0)
    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #convert to HSV for easier colour processing

    lower_bounds = []
    upper_bounds = []
    masks = []
    conts = []
    images = []
    #loop through the colours finding where the blocks are
    for index, colour in enumerate(boundaries):
        #get the upper and lower boundaries for the colour in question
        lower_bounds.append(colour[0])
        upper_bounds.append(colour[1])

        #convert the bounds to something we can use
        lower_bounds[index] = np.array(lower_bounds[index], dtype = "uint8")
        upper_bounds[index] = np.array(upper_bounds[index], dtype = "uint8")

        #make the colour mask to find the contours on
        masks.append(cv2.inRange(image2, lower_bounds[index], upper_bounds[index]))

        #noise reduction as described above
        masks[index] = cv2.morphologyEx(masks[index], cv2.MORPH_OPEN, kernelOpen)
        masks[index] = cv2.morphologyEx(masks[index], cv2.MORPH_CLOSE, kernelClose)

        #find the blocks of colour
        conts.append(cv2.findContours(masks[index].copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0])

        #make a copy of the original image which we can doodle on
        images.append(image.copy())
        cv2.drawContours(images[index], conts[index], -1, (0, 0, 255), 1)

    #you can then get the position and colour of every block like this
    for colour in range(len(boundaries)): #go through each colour
        for cont in conts[colour]: #go through each block of that colour
            x,y,w,h = cv2.boundingRect(cont) #make a rectagle which surounds the contour
            cv2.rectangle(image2, (x, y), (x + w, y + h), (0, 255,0), 2) #find the centre
            print((x, y), colour)


    # show the images
    cv2.imshow("images", np.hstack(images))



    cv2.waitKey()
    cv2.destroyAllWindows()




if __name__ == '__main__':
        main()
