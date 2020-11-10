import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
from skimage import morphology, filters
import pandas as pd
import matplotlib.patches as mpatches

os.system("cls||clear")


class estimateLiveDead:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def countAndFindLiveDead(
        self, inputImage1, inputImage2, dataFrame1, changeThreshold
    ):
        inputImageA = inputImage1
        inputImageB = inputImage2
        dataFrameWithLiveDead = dataFrame1.copy()
        dataFrameWithLiveDead["ldStatus"] = ""
        scaleWith = np.max(np.max(inputImageA))

        for index, row in dataFrameWithLiveDead.iterrows():
            # images are base 255
            areaChangeObject = np.floor(
                np.absolute(
                    np.sum(inputImageA[(row.coords)[:, 0], (row.coords)[:, 1]]/scaleWith)
                    - np.sum((inputImageB[(row.coords)[:, 0], (row.coords)[:, 1]])/scaleWith)
                )
            )
            dataFrameWithLiveDead["ldStatus"][index] = (
                areaChangeObject > changeThreshold
            )
        return dataFrameWithLiveDead


if __name__ == "__main__":
    estimateLiveDead().testWithAString()
    inputImage = np.load("removedObjectsImage.npy")
    unpickled_df1 = pd.read_pickle("pandasFrame1Pickled.pkl")

    unpickled_df1.columns = (
        unpickled_df1.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("(", "")
        .str.replace(")", "")
        .str.replace("-", "")
    )
    colorInputImage = np.stack((np.array(inputImage),) * 3, -1)
    mixedImage = np.load("removedObjectsImage.npy")
    mixedImage[:, 1:900] = 0
    newTable = estimateLiveDead().countAndFindLiveDead(
        np.load("removedObjectsImage.npy"), mixedImage, unpickled_df1, 2
    )
    for index, row in newTable.iterrows():
        if newTable["ldStatus"][index] == True:
            # cv2.drawMarker(
            #     colorInputImage,
            #     (row.bbox1, row.bbox0),
            #     (row.bbox3, row.bbox2),
            #     (255, 255, 0),
            #     2,
            # )
            cv2.drawMarker(
                colorInputImage, (row.centroid1, row.centroid0), (255, 255, 0), 1
            )
        else:
            cv2.drawMarker(
                colorInputImage, (row.centroid1, row.centroid0), (255, 0, 255), 1
            )

    cv2.imshow("withObjects", colorInputImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

