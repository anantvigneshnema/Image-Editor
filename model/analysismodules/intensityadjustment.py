import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
from skimage import morphology, filters
from skimage.restoration import denoise_tv_chambolle, denoise_bilateral

os.system("cls||clear")


class cleanInputImage:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def cleanInputMovie(self, imageToClean, arrayOfValues):

        if len(imageToClean.shape) == 3:
            inputImage = cv2.cvtColor(imageToClean, cv2.COLOR_BGR2GRAY)
        else:
            inputImage = imageToClean.copy()

        temp = arrayOfValues
        # if len(inputImage.shape) == 3:
        #     inputImage = cv2.fastNlMeansDenoisingColored(inputImage)
        # else:
        #     inputImage = cv2.fastNlMeansDenoising(inputImage)
        _, inputImage = cv2.threshold(inputImage, temp[0], 255, cv2.THRESH_TOZERO)
        # cv2.imshow("", inputImage.astype(np.uint8))
        # cv2.waitKey(0)
        # inputImage = cv2.subtract(inputImage, temp[0])
        # inputImage = cv2.normalize(
        #     inputImage, None, 0, 255, cv2.NORM_MINMAX
        # )  # self.rescale(inputImage)
        _, inputImage = cv2.threshold(inputImage, temp[1], 255, cv2.THRESH_TOZERO_INV)
        # super_threshold_indices = inputImage > temp[1]
        # inputImage[super_threshold_indices] = 0
        # inputImage = cv2.normalize(
        #     inputImage, None, 0, 255, cv2.NORM_MINMAX
        # )  # self.rescale(inputImage)

        # inputImage = morphology.area_opening(inputImage, temp[2])
        # inputImage = morphology.flood_fill(inputImage,(1,1),0)
        # inputImage = cv2.subtract(inputImage, openedImage)
        # inputImage = cv2.normalize(
        #     inputImage, None, 0, 255, cv2.NORM_MINMAX
        # )  # self.rescale(inputImage)

        # if temp[3] != 0:
        #     super_threshold_indices = inputImage > temp[3]
        #     inputImage[super_threshold_indices] = 0
        #     inputImage = cv2.normalize(inputImage, None, 0, 255, cv2.NORM_MINMAX)
        if temp[2] != 0:
            inputImage = filters.meijering(inputImage, black_ridges=False) * 255
        inputImage = cv2.normalize(inputImage, None, 0, 255, cv2.NORM_MINMAX)
        _, inputImage = cv2.threshold(inputImage, temp[3], 255, cv2.THRESH_TOZERO)
        _, inputImage = cv2.threshold(inputImage, temp[4], 255, cv2.THRESH_TOZERO_INV)
        inputImage = cv2.normalize(inputImage, None, 0, 255, cv2.NORM_MINMAX)
        # _, inputImage = cv2.threshold(inputImage, 0.95, 255, cv2.THRESH_TOZERO_INV)
        # if temp[5] != 0:
        #     inputImage = cv2.subtract(inputImage, temp[5])
        #     inputImage = cv2.normalize(inputImage, None, 0, 255, cv2.NORM_MINMAX)  #

        # if temp[6] != 0:
        #     super_threshold_indices = inputImage > temp[6]
        #     inputImage[super_threshold_indices] = 0
        #     inputImage = cv2.normalize(inputImage, None, 0, 255, cv2.NORM_MINMAX)

        # cv2.imshow("removedObjectsImage", inputImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return inputImage


if __name__ == "__main__":
    cleanInputImage().testWithAString()
    frame_no = 0
    cap = cv2.VideoCapture(r"C:\Users\Sid\Desktop\iPOD 1 (right)\12l.MOV")
    advicedAngle = 0
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    _, originalImage = cap.read()

    cleanInputImage().cleanInputMovie(
        cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY), [180, 255, 1, 100, 250, 0, 0]
    )
