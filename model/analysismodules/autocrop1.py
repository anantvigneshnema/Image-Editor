import cv2
import numpy as np
import os
import math
import scipy.spatial as scipspa
import scipy.ndimage
import os
from skimage import feature, filters
os.system("cls||clear")

class movieAutoCrop:

    def __init__(self):
        self.count = 0

    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    # input should be an uncropped image, and angle and output should be angle, coordinates
    def autoCropInputMovie(self, originalImage, advicedAngle, algoChoice): 
        if len(originalImage.shape) == 3:
            inputGreyImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        else:
            inputGreyImage = originalImage.copy()

        # region - produces greyscale, cleaned and canny image
        cleanInputImage = inputGreyImage
        edges = feature.canny(inputGreyImage)#, sigma = 0.5)
        edges=  ((edges).astype(int)*255).astype('uint8') # 0 or 1
        
        # FOR HOUGH
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
        contourEdges = cv2.dilate(edges, kernel, iterations = 3)
        contourEdges = cv2.erode(contourEdges, kernel,iterations = 2)
        
        image = edges
        image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
        gray = contourEdges 
        gray_blurred = cv2.blur(gray, (3, 3)) 
        # Apply Hough transform on the blurred image. 
        #detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20, param1 = 50, param2 = 30, minRadius = 1, maxRadius = 40) 
        detected_circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20,  param1 = 50, param2 = 28,   minRadius = 14, maxRadius = 28) 
        # Draw circles that are detected. 
        if detected_circles is not None:   
        # Convert the circle parameters a, b and r to integers. 
          detected_circles = np.uint16(np.around(detected_circles)) 
        
        algo1CircleCenterAndRadius = []
        height, width = gray_blurred.shape
        for index, pt in enumerate(detected_circles[0, :]): 
            a, b, r = pt[0], pt[1], pt[2] 
            if (inputGreyImage[(b,a)] > 25) and not  ( a < 15  or b < 15 or a > width - 15 or b > height - 15) and not ((a > 700 and a < 1220) or (b > 380 and b < 750)):
               
               cv2.circle(image, (a, b), r, (0, 255, 0), 2)
               algo1CircleCenterAndRadius.append([a,b,r])
               
        # cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # cv2.imshow("image", image)
        # cv2.waitKey(0)
        # return

        # endregion
        algo1CircleCenterAndRadius = np.array(algo1CircleCenterAndRadius)

        widthImg = width
        heightImg = height
        

        if algoChoice == 1:
            if np.shape(algo1CircleCenterAndRadius)[0] >= 2:
                pairSlopeDistance = np.empty((0, 8), int)
                YourTreeName = scipspa.cKDTree(
                    algo1CircleCenterAndRadius[:, 0:2], leafsize=50
                )

                for item in algo1CircleCenterAndRadius:
                    distance, idx = YourTreeName.query(
                        item[:2],
                        k=np.shape(algo1CircleCenterAndRadius)[0],
                        distance_upper_bound=1920,
                    )
                    for index, distMeasure in enumerate(distance):
                        if distMeasure > 1350:
                            slopeCalc = -(
                                algo1CircleCenterAndRadius[idx[index], 1].astype('float') - item[1]
                            ) / (algo1CircleCenterAndRadius[idx[index], 0].astype('float') - item[0])
                            slopeAngle = np.absolute(np.rad2deg(np.arctan(slopeCalc)))
                            if slopeAngle < 45 and slopeAngle > 23:
                                angleDesign = 33
                                angleRot = advicedAngle + angleDesign - slopeAngle
                                if slopeCalc < 0:
                                    angleRot = -angleRot
                                if np.absolute(angleRot) > 5:
                                    angleRot = 0
                                pairSlopeDistance = np.append(
                                    pairSlopeDistance,
                                    [
                                        np.concatenate(
                                            (
                                                item,
                                                algo1CircleCenterAndRadius[idx[index]],
                                                [angleRot],
                                                [distMeasure],
                                            )
                                        )
                                    ],
                                    axis=0,
                                )

            # saving unique distance and angled object or only one pair
            # sort by size of marker and in descending order
            pairSlopeDistance = pairSlopeDistance[
                np.argsort(pairSlopeDistance[:, 2])[::-1]
            ]

            _, indices = np.unique(pairSlopeDistance[:, 6:8:1], return_index=True, axis=0)
            array = np.delete(pairSlopeDistance, indices[1:-1], 0)
            inputImage = scipy.ndimage.rotate(inputGreyImage, angleRot, reshape=False)

            for i in range(0, 2, 1):
                xr = int(
                    np.round(
                        (array[i, 0] - widthImg / 2) * np.cos(np.deg2rad(angleRot))
                        - (-array[i, 1] + heightImg / 2) * np.sin(np.deg2rad(angleRot))
                        + widthImg / 2
                    )
                )
                yr = int(
                    np.round(
                        -(array[i, 0] - widthImg / 2) * np.sin(np.deg2rad(angleRot))
                        + (array[i, 1] - heightImg / 2) * np.cos(np.deg2rad(angleRot))
                        + heightImg / 2
                    )
                )
                
                xr1 = int(
                    np.round(
                        (array[i, 3] - widthImg / 2) * np.cos(np.deg2rad(angleRot))
                        - (-array[i, 4] + heightImg / 2) * np.sin(np.deg2rad(angleRot))
                        + widthImg / 2
                    )
                )
                yr1 = int(
                    np.round(
                        -(array[i, 3] - widthImg / 2) * np.sin(np.deg2rad(angleRot))
                        + (array[i, 4] - heightImg / 2) * np.cos(np.deg2rad(angleRot))
                        + heightImg / 2
                    )
                )
                cv2.circle(
                    inputImage, (xr1, yr1), int(np.round(array[i, 5])), (0, 255, 0), 1
                )
            
           
            allRadii = np.sort(
                np.append(pairSlopeDistance[0, 2:6:3], pairSlopeDistance[1, 2:6:3])
            )[::-1]

            pixToMicronRatio = 500 / np.mean(allRadii[0:2:1])

            minMaxVertices = [
                int(np.ceil(min([xr,xr1]))),
                int(
                    np.ceil(
                        min(([yr,yr1]))
                        + 1250 / pixToMicronRatio
                        - 10
                    )
                ),
                int(np.round(max(([xr,xr1])))),
                int(
                    np.round(
                        max(([yr,yr1]))
                        - 1250 / pixToMicronRatio
                        + 10
                    )
                ),
            ]
            # region about plotting lines
            # coordinates = minMaxVertices([3 2;4 2; 4 1; 3 1; 3 2])
            cv2.line(
                inputImage,
                (minMaxVertices[0], minMaxVertices[1]),
                (minMaxVertices[2], minMaxVertices[1]),
                [0, 255, 0],
                2,
            )
            cv2.line(
                inputImage,
                (minMaxVertices[0], minMaxVertices[1]),
                (minMaxVertices[0], minMaxVertices[3]),
                [0, 255, 0],
                2,
            )
            cv2.line(
                inputImage,
                (minMaxVertices[0], minMaxVertices[3]),
                (minMaxVertices[2], minMaxVertices[3]),
                [0, 255, 0],
                2,
            )
            cv2.line(
                inputImage,
                (minMaxVertices[2], minMaxVertices[1]),
                (minMaxVertices[2], minMaxVertices[3]),
                [0, 255, 0],
                2,
            )

            croppedImage = scipy.ndimage.rotate(inputGreyImage, angleRot, reshape=False)
            croppedImage = croppedImage[
                minMaxVertices[1] : minMaxVertices[3],
                minMaxVertices[0] : minMaxVertices[2],
            ]
            # endregion

        return inputImage, minMaxVertices, angleRot, pixToMicronRatio

if __name__ == "__main__":
        import os
        arr = os.listdir(r"C:\Users\drink\Desktop\Movies")
        frame_no = 5
        count = 0
        for x in arr[0:-1]:
            
            cap = cv2.VideoCapture(r"C:\Users\drink\Desktop\Movies\\"+x)
            advicedAngle = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            _, originalImage = cap.read()
            algoChoice = 1

            try:
                movieAutoCrop().autoCropInputMovie(originalImage, advicedAngle, algoChoice)
                count = count+1
                #print(count)
                inputImage, _, _, _ = movieAutoCrop().autoCropInputMovie(originalImage, advicedAngle, algoChoice)
        
                cv2.namedWindow('image', cv2.WINDOW_NORMAL)
                cv2.imshow("image", inputImage)
                print(x)
                cv2.waitKey(0)
                
               
            except:
                pass

    #movieAutoCrop().testWithAString()


