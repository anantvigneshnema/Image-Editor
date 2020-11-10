import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
from skimage import data, util, measure
import pandas as pd

os.system("cls||clear")


class objectDetectFromThresholdedImage:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def returnPropertiesOfThresholdedImageObjects(self, inputImage, tempArray):

        #colorInputImage = np.stack((np.array(inputImage),) * 3, -1)
        minAreaThreshold = tempArray[0]
        maxAreaThreshold = tempArray[1]
        label_image = measure.label(inputImage > 1, connectivity=inputImage.ndim)
        rawImageRegionProperties = measure.regionprops_table(
            label_image,
            inputImage,
            properties=[
                "centroid",
                "major_axis_length",
                "minor_axis_length",
                "area",
                "bbox",
                "eccentricity",
                "perimeter",
                "orientation",
                "solidity",
                "coords",
                "intensity_image",
            ],
            separator="",
        )

        rawRegionPropsDF = pd.DataFrame(rawImageRegionProperties)
        # data.to_pickle("pandasFrame1Pickled.pkl")
        rawRegionPropsDF.drop(
            rawRegionPropsDF[rawRegionPropsDF["area"] < minAreaThreshold].index,
            inplace=True,
        )
        rawRegionPropsDF.drop(
            rawRegionPropsDF[rawRegionPropsDF["area"] > maxAreaThreshold].index,
            inplace=True,
        )



        return rawRegionPropsDF

       
       


if __name__ == "__main__":
    objectDetectFromThresholdedImage().testWithAString()
    rawRegionPropsDF = objectDetectFromThresholdedImage().returnPropertiesOfThresholdedImageObjects(
        np.load("removedObjectsImage.npy"), ([30, 300])
    )
    colorInputImage = np.stack((np.array(np.load("removedObjectsImage.npy")),) * 3, -1)
    for index, row in rawRegionPropsDF.iterrows():

        cv2.rectangle(
            colorInputImage,
            (row.bbox1, row.bbox0),
            (row.bbox3, row.bbox2),
            (0, 255, 0),
            2,
        )

    cv2.imshow("withObjects", colorInputImage)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("This works")

