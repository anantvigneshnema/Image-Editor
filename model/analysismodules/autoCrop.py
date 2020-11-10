import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage

os.system("cls||clear")


class movieAutoCrop:
    def testWithAString(self):  # this is just a very basic stub to prinout
        print("Check if this works")

    def autoCropInputMovie(self):
        advicedAngle = 0
        # region - produces greyscale, cleaned and canny image
        cap = cv2.VideoCapture(r"C:\Users\Sid\Desktop\iPOD 1 (right)\12l.MOV")
        cap.set(1, 0.8)
        ret, originalImage = cap.read()
        inputGreyImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
        cleanInputImage = cv2.medianBlur(inputGreyImage, 3)
        vParam = np.median(cleanInputImage)
        sigmaParam = 0.33
        edges = cv2.Canny(
            cleanInputImage,
            int(max(0, (1.0 - sigmaParam) * vParam)),
            int(min(255, (1.0 + sigmaParam) * vParam)),
        )
        # endregion

        inputImage = originalImage.copy()
        heightImg, widthImg = inputImage.shape[:2]
        # region - algorithm 1 to detect circles with contours
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        algo1CircleCenterAndRadius = np.array([])

        # loop over detected contours
        # it can be empty in which case room doesnt run
        for cnt in contours:
            approxContourFit = cv2.approxPolyDP(
                cnt, 0.03 * cv2.arcLength(cnt, True), True
            )
            # epsilon is for accurate shape hugging
            # number of corners (beyond pentagon = 5 this is a guess)
            if len(approxContourFit) >= 8:
                (center, size, angle) = cv2.fitEllipse(approxContourFit)
                center = (int(np.round(center[0])), int(np.round(center[1])))

                if (
                    size[0] * size[1] / 4 > 50
                    and size[0] * size[1] / 4 < 700
                    and size[0] / size[1] >= 0.9
                    and size[0] / size[1] <= 1.1
                    and inputGreyImage[center[::-1]] > 50
                    and size[0] >= 14
                    and size[0] <= 50
                    and size[1] >= 14
                    and size[1] <= 50
                    and not (
                        center[0] < 15
                        or center[1] < 15
                        or center[0] > widthImg - 15
                        or center[1] > heightImg - 15
                    )
                    and not (
                        (center[0] > 700 and center[0] < 1220)
                        or (center[1] > 380 and center[1] < 750)
                    )
                ):
                    size1 = (int(np.round(size[0] * 0.5)), int(np.round(size[1] * 0.5)))

                    cv2.ellipse(
                        inputImage, center, size1, angle, 0, 360, (255, 255, 0), 1
                    )
                    algo1CircleCenterAndRadius = np.append(
                        algo1CircleCenterAndRadius, np.append(center, np.mean(size) / 2)
                    )
        # endregion
        algo1CircleCenterAndRadius = algo1CircleCenterAndRadius.reshape(-1, 3)

        # region - algorithm 2 to detect circle with MSER
        algo2CircleCenterAndRadius = np.array([])
        regions, _ = cv2.MSER_create().detectRegions(originalImage)

        for cnt in [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]:
            approxContourFit = cv2.approxPolyDP(
                cnt, 0.03 * cv2.arcLength(cnt, True), True
            )

            if len(approxContourFit) >= 8:
                area = cv2.contourArea(cnt)
                M = cv2.moments(cnt)
                centroid = int(M["m10"] / M["m00"])
                centroid = np.append(centroid, int(M["m01"] / M["m00"]))
                equi_diameter = np.sqrt(4 * area / np.pi) / 2
                if (
                    inputGreyImage[(centroid[1], centroid[0])] > 50
                    and area > 50
                    and area < 700
                    and equi_diameter >= 14
                    and equi_diameter <= 50
                    and not (
                        centroid[0] < 15
                        or centroid[1] < 15
                        or centroid[0] > widthImg - 15
                        or centroid[1] > heightImg - 15
                    )
                    and not (
                        (centroid[0] > 700 and centroid[0] < 1220)
                        or (centroid[1] > 380 and centroid[1] < 750)
                    )
                ):
                    algo2CircleCenterAndRadius = np.append(
                        algo2CircleCenterAndRadius,
                        np.append(centroid, equi_diameter / 2),
                    )
                    cv2.drawContours(inputImage, [cnt], 0, (0, 255, 0), -1)
        # endregion
        algo2CircleCenterAndRadius = algo2CircleCenterAndRadius.reshape(-1, 3)

        if np.shape(algo1CircleCenterAndRadius)[0] >= 2:
            pairSlopeDistance = np.empty((0, 8), int)
            YourTreeName = scipy.spatial.cKDTree(
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
                            algo1CircleCenterAndRadius[idx[index], 1] - item[1]
                        ) / (algo1CircleCenterAndRadius[idx[index], 0] - item[0])
                        slopeAngle = np.absolute(np.rad2deg(np.arctan(slopeCalc)))
                        if slopeAngle < 43 and slopeAngle > 23:
                            angleDesign = 33
                            angleRot = angleDesign - slopeAngle + advicedAngle
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
        unique_keys, indices = np.unique(
            pairSlopeDistance[:, 6:8:1], return_index=True, axis=0
        )
        array = np.delete(pairSlopeDistance, indices, 0)

        inputImage = scipy.ndimage.rotate(inputGreyImage, angleRot, reshape=False)
        for i in range(0, 2, 1):
            xr = int(
                np.round(
                    (array[i, 0] - widthImg / 2) * np.cos(np.deg2rad(angleRot))
                    - (array[i, 1] - heightImg / 2) * np.sin(np.deg2rad(angleRot))
                    + widthImg / 2
                )
            )
            yr = int(
                np.round(
                    (array[i, 0] - widthImg / 2) * np.sin(np.deg2rad(angleRot))
                    + (array[i, 1] - heightImg / 2) * np.cos(np.deg2rad(angleRot))
                    + heightImg / 2
                )
            )
            cv2.circle(inputImage, (xr, yr), int(np.round(array[i, 2])), (0, 255, 0), 1)
            xr1 = int(
                np.round(
                    (array[i, 3] - widthImg / 2) * np.cos(np.deg2rad(angleRot))
                    - (array[i, 4] - heightImg / 2) * np.sin(np.deg2rad(angleRot))
                    + widthImg / 2
                )
            )
            yr1 = int(
                np.round(
                    (array[i, 3] - widthImg / 2) * np.sin(np.deg2rad(angleRot))
                    + (array[i, 4] - heightImg / 2) * np.cos(np.deg2rad(angleRot))
                    + heightImg / 2
                )
            )
            cv2.circle(
                inputImage, (xr1, yr1), int(np.round(array[i, 5])), (0, 255, 0), 1
            )
        allRadii = np.sort(
            np.append(pairSlopeDistance[0, 2:6:3], pairSlopeDistance[1, 2:6:3])
        )
        pixToMicronRatio = 500 / allRadii.max()
        sorted_array = pairSlopeDistance[np.argsort(pairSlopeDistance[:, 2])]

        minMaxVertices = [
            int(np.ceil(sorted_array[-1, 0:4:3].min())),
            int(np.ceil(sorted_array[-1, 1:5:3].min() + 1250 / pixToMicronRatio - 10)),
            int(np.round(sorted_array[-1, 0:4:3].max())),
            int(np.round(sorted_array[-1, 1:5:3].max() - 1250 / pixToMicronRatio + 10)),
        ]
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
            minMaxVertices[1] : minMaxVertices[3], minMaxVertices[0] : minMaxVertices[2]
        ]

        cv2.imshow("originalImage", inputImage)
        cv2.imwrite("originalImage2.jpg", originalImage)
        cv2.imwrite("inputImage2.jpg", inputImage)
        cv2.imwrite("croppedImage2.jpg", croppedImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    movieAutoCrop().autoCropInputMovie()
    movieAutoCrop().testWithAString()

