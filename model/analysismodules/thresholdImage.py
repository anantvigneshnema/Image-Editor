import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
from skimage import morphology, measure

os.system("cls||clear")


class thresholdImage:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def thresholdInputMovie(self, cleanedImageUint8, arrayOfValues):
        temp = arrayOfValues
        cleanedImageUint8 = np.uint8(cleanedImageUint8)
        if temp[1] > 0:
            threshedImage = cv2.adaptiveThreshold(
                cleanedImageUint8,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                temp[1],
                temp[0],
            )
            # cv2.imshow("threshedImage", threshedImage)
            # cv2.imwrite("threshedImage1.jpg", threshedImage)
            # cv2.waitKey(0)

            # cv2.destroyAllWindows()
        elif temp[1] == -1:
            _, threshedImage = cv2.threshold(cleanedImageUint8, 0, 255, cv2.THRESH_OTSU)
            # cv2.imshow("threshedImage", threshedImage)
            # cv2.imwrite("threshedImage2.jpg", threshedImage)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        elif temp[1] == -2:
            _, threshedImage = cv2.threshold(
                cleanedImageUint8, temp[0], 255, cv2.THRESH_BINARY
            )
        else:
            threshedImage = cv2.adaptiveThreshold(
                cleanedImageUint8,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                2 * math.floor(np.mean(cleanedImageUint8.shape) / 16) + 1,
                temp[0],
            )
            # cv2.imshow("threshedImage", threshedImage)
            # cv2.imwrite("threshedImage3.jpg", threshedImage)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

        if temp[5] != 0:
            kernel = np.ones((temp[5], temp[5]), np.uint8)
            closedImage = cv2.morphologyEx(threshedImage, cv2.MORPH_CLOSE, kernel)
            # cv2.imshow("closedImage", closedImage)
            # cv2.imwrite("closedImage.jpg", closedImage)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
        else:
            closedImage = threshedImage

        fillHolesImage = closedImage
        # contour, _ = cv2.findContours(
        #     fillHolesImage, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
        # )

        # for cnt in contour:
        #     cv2.drawContours(fillHolesImage, [cnt], 0, 255, -1)

        # cv2.imshow("fillHolesImagee", fillHolesImage)
        # cv2.imwrite("fillHolesImage.jpg", fillHolesImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print("This works")

        if temp[2] >= 0 and temp[3] >= 0:  # upper and lower limit
            # removedLowerObjectsImage = morphology.remove_small_objects(
            #     measure.label(fillHolesImage.astype(bool),connectivity=fillHolesImage.ndim),
            #     min_size=temp[2],
            #     connectivity=fillHolesImage.ndim,
            #     in_place=False,
            # )  # lower limti only

            # removedUpperObjectsImage = morphology.remove_small_objects(
            #     measure.label(fillHolesImage.astype(bool),connectivity=fillHolesImage.ndim),
            #     min_size=temp[3],
            #     connectivity=fillHolesImage.ndim,
            #     in_place=False,
            # )  # upper limti only
            # removedLowerObjectsImage = ((removedLowerObjectsImage>0).astype(np.uint8)) * 255
            # removedUpperObjectsImage = ((removedUpperObjectsImage>0).astype(np.uint8)) * 255
            # removedObjectsImage = cv2.bitwise_xor(
            #     removedLowerObjectsImage, removedUpperObjectsImage
            # )
            # removedObjectsImage = ((removedObjectsImage>0).astype(np.uint8)) * 255

            nb_components, output, stats, _ = cv2.connectedComponentsWithStats(
                fillHolesImage, connectivity=4
            )
            sizes = stats[1:, -1]
            nb_components = nb_components - 1
            removedObjectsImage = np.zeros((output.shape))
            for i in range(0, nb_components):
                if sizes[i] >= temp[2] and sizes[i] <= temp[3]:
                    removedObjectsImage[output == i + 1] = 255

        elif temp[2] >= 0:
            # removedObjectsImage = morphology.remove_small_objects(
            #     measure.label(fillHolesImage.astype(bool),connectivity=fillHolesImage.ndim),
            #     min_size=temp[2],
            #     connectivity=fillHolesImage.ndim,
            #     in_place=False,
            # )  # lower limti only
            nb_components, output, stats, _ = cv2.connectedComponentsWithStats(
                fillHolesImage, connectivity=4
            )
            sizes = stats[1:, -1]
            nb_components = nb_components - 1
            removedObjectsImage = np.zeros((output.shape))
            for i in range(0, nb_components):
                if sizes[i] >= temp[2]:
                    removedObjectsImage[output == i + 1] = 255

        # cv2.imshow("removedObjectsImage", removedObjectsImage)
        # np.save("removedObjectsImage", removedObjectsImage)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print("This works")

        thresoldedImageFinal = removedObjectsImage
        return thresoldedImageFinal


if __name__ == "__main__":
    thresholdImage().testWithAString()

    thresholdImage().thresholdInputMovie(
        cv2.cvtColor(cv2.imread(r"croppedImage2.jpg"), cv2.COLOR_BGR2GRAY),
        [-50, 0, 60, 300, 0, 3],
    )

