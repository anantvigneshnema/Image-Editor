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

    def countAndFindLiveDead(self):
        for num, currFrame in enumerate(np.arange(1, 3, 1), start=1):
            if num > 1:
                inputImage = np.load("removedObjectsImage.npy")
                colorInputImage = np.stack((np.array(inputImage),) * 3, -1)

                # inputImage = cv2.cvtColor(
                #     cv2.imread(r"removedObjectsImage.jpg"), cv2.COLOR_BGR2GRAY
                # )
                inputImageB = cv2.cvtColor(
                    cv2.imread(r"removedObjectsImageB.jpg"), cv2.COLOR_BGR2GRAY
                )
                inputImageB = inputImage
                # colorInputImage = cv2.cvtColor(inputImage, cv2.COLOR_GRAY2RGB)
                unpickled_df1 = pd.read_pickle("pandasFrame1Pickled.pkl")

                unpickled_df1.columns = (
                    unpickled_df1.columns.str.strip()
                    .str.lower()
                    .str.replace(" ", "_")
                    .str.replace("(", "")
                    .str.replace(")", "")
                    .str.replace("-", "")
                )
                # unpickled_df2 = pd.read_pickle("pandasFrame2Pickled.pkl")
                unpickled_df2 = unpickled_df1
                unpickled_df2.columns = (
                    unpickled_df2.columns.str.strip()
                    .str.lower()
                    .str.replace(" ", "_")
                    .str.replace("(", "")
                    .str.replace(")", "")
                    .str.replace("-", "")
                )
                unpickled_df1["ldStatus"] = ""
                for index, row in unpickled_df1.iterrows():
                    areaChangeObject = np.floor(
                        np.absolute(
                            np.sum(inputImage[(row.coords)[:, 0], (row.coords)[:, 1]])
                            - np.sum(
                                (inputImageB[(row.coords)[:, 0], (row.coords)[:, 1]])
                            )
                        )
                    )
                    unpickled_df1["ldStatus"][index] = areaChangeObject > 0
                    if areaChangeObject > 0:
                        # minr, minc, maxr, maxc = row.bbox
                        # cv2.rectangle(
                        #     colorInputImage,
                        #     (row.bbox1, row.bbox0),
                        #     (row.bbox3, row.bbox2),
                        #     (255, 255, 0),
                        #     2,
                        # )
                        cv2.drawMarker(
                            colorInputImage,
                            (row.bbox1, row.bbox0),
                            (row.bbox3, row.bbox2),
                            (255, 255, 0),
                            2,
                        )
                    else:
                        # minr, minc, maxr, maxc = row.bbox
                        cv2.drawMarker(
                            colorInputImage,
                            (row.centroid1, row.centroid0),
                            (255, 255, 0),
                            1,
                        )
                    # cv2.rectangle(
                    #     colorInputImage,
                    #     (row.bbox1, row.bbox0),
                    #     (row.bbox3, row.bbox2),
                    #     (0, 255, 0),
                    #     2,
                    # )

        cv2.imshow("withObjects", colorInputImage)
        cv2.imwrite("withObjectsLive.jpg", colorInputImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("This works")


if __name__ == "__main__":
    estimateLiveDead().testWithAString()
    estimateLiveDead().countAndFindLiveDead()

