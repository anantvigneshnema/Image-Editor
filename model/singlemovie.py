import sys
import cv2
import numpy as np
import os
import math
import scipy.spatial
import scipy.ndimage
import matplotlib.pyplot as plt
from model.analysismodules.autocrop1 import movieAutoCrop
from model.analysismodules.intensityadjustment import cleanInputImage
from model.analysismodules.thresholdImage import thresholdImage
from model.analysismodules.objectDetectFromFrame import objectDetectFromThresholdedImage
import scipy.ndimage
from model.analysismodules.computeLiveDead import estimateLiveDead
from model.analysismodules.computeActivity import estimateActivity
from PyQt5.QtWidgets import QApplication
import pandas as pd


class singlemovieobject:
    def __init__(self, moviename):
        self.movie_name = moviename
        self.video_object = cv2.VideoCapture(self.movie_name)
        self.video_object.set(cv2.CAP_PROP_BUFFERSIZE, 2)
        self.number_of_frames = self.video_object.get(cv2.CAP_PROP_FRAME_COUNT)
        self.angleRot = 0
        self.cropImageFrame = None
        self.threshParamArray = None
        self.cleanParamArray = None
        self.minMaxVertices = None
        self.currentFrameAt = None

    def getNumberOfFrames(self):
        self.number_of_frames = self.video_object.get(cv2.CAP_PROP_FRAME_COUNT)
        return self.number_of_frames

    def getCropCoordinates(self, inputImageFrame, adviced_angle, algoChoice):
        inputImage, self.minMaxVertices, self.angleRot, self.pixToMicronRatio = movieAutoCrop().autoCropInputMovie(
            inputImageFrame, adviced_angle, algoChoice
        )
        return inputImage

    def getUncroppedFrameFromVideo(self, frame_no):
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        _, uncropped_image = self.video_object.read()
        return uncropped_image

    def getUncroppedFrameFromVideoRotated(self, frame_no, altAngle = None):
      if altAngle == None:
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        _, uncropped_image = self.video_object.read()
        rotated_image_frame = scipy.ndimage.rotate(
            uncropped_image, self.angleRot, reshape=False
        )
      else :
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        _, uncropped_image = self.video_object.read()
        rotated_image_frame = scipy.ndimage.rotate(
            uncropped_image, altAngle, reshape=False
        )
      return rotated_image_frame


    def setRotationAngle(self, adviced_angle):
        self.angleRot = adviced_angle

    def getPixelToUmRatio(self):
        minMaxVertices = self.minMaxVertices
        return np.mean(
            [
                35000 / np.absolute(minMaxVertices[0] - minMaxVertices[2]),
                20245 / np.absolute(minMaxVertices[1] - minMaxVertices[3]),
            ]
        )

    def overlayCropOnUncroppedFrame(self, inputImageFrame):
        rotated_image_frame = scipy.ndimage.rotate(
            inputImageFrame, self.angleRot, reshape=False
        )
        minMaxVertices = self.minMaxVertices
        cv2.line(
            rotated_image_frame,
            (minMaxVertices[0], minMaxVertices[1]),
            (minMaxVertices[2], minMaxVertices[1]),
            [0, 255, 0],
            2,
        )
        cv2.line(
            rotated_image_frame,
            (minMaxVertices[0], minMaxVertices[1]),
            (minMaxVertices[0], minMaxVertices[3]),
            [0, 255, 0],
            2,
        )
        cv2.line(
            rotated_image_frame,
            (minMaxVertices[0], minMaxVertices[3]),
            (minMaxVertices[2], minMaxVertices[3]),
            [0, 255, 0],
            2,
        )
        cv2.line(
            rotated_image_frame,
            (minMaxVertices[2], minMaxVertices[1]),
            (minMaxVertices[2], minMaxVertices[3]),
            [0, 255, 0],
            2,
        )
        return rotated_image_frame

    def getCroppedFrameFromVideo(self, inputImageFrame):

        minMaxVertices = self.minMaxVertices
        croppedImage = scipy.ndimage.rotate(
            inputImageFrame, self.angleRot, reshape=False
        )
        self.cropImageFrame = croppedImage[
            minMaxVertices[1] : minMaxVertices[3], minMaxVertices[0] : minMaxVertices[2]
        ]
        return self.cropImageFrame

    def getCleanedImageFromFrame(
        self, inputImageFrame, tempArray
    ):
        
        self.cleanParamArray = tempArray
        return cleanInputImage().cleanInputMovie(inputImageFrame, tempArray)

    def getThresholdedImageFromFrame(
        self, inputImageFrame, tempArray
    ):
        self.threshParamArray = tempArray
        return thresholdImage().thresholdInputMovie(inputImageFrame, tempArray)

    def computePropertiesOfFrame(self, inputImageFrame, tempArray):
        return objectDetectFromThresholdedImage().returnPropertiesOfThresholdedImageObjects(
            inputImageFrame, tempArray
        )

    # Original Function
    '''def putBoundingBoxesOnFrame(self, inputImageFrame, propertiesDataFrame):
        if len(inputImageFrame.shape) == 3:
            colorInputImage = inputImageFrame.copy()
        else:
            colorInputImage = cv2.cvtColor(inputImageFrame, cv2.COLOR_GRAY2RGB)

        for index, row in propertiesDataFrame.iterrows():
            cv2.rectangle(
                colorInputImage,
                (row.bbox1, row.bbox0),
                (row.bbox3, row.bbox2),
                (0, 255, 0),
                2,
            )
        return colorInputImage'''

    def putBoundingBoxesOnFrame(self, inputImageFrame, propertiesDataFrame):
        if len(inputImageFrame.shape) == 3:
            colorInputImage = inputImageFrame.copy()
        else:
            colorInputImage = cv2.cvtColor(inputImageFrame, cv2.COLOR_GRAY2RGB)

        for index, row in propertiesDataFrame.iterrows():
            if str(row.solidity) == "oneWormLive":
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (0, 0, 255),
                    2,
                )
            if str(row.solidity) == "multiWormLive":
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (255, 255, 0),
                    2,
                )
            if str(row.solidity) == "oneWormDead":
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (255, 0, 0),
                    2,
                )
            if str(row.solidity) == "multiWormDead":
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (255, 255, 255),
                    2,
                )

            if str(row.solidity) == "autoDetcted":
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (0, 255, 0),
                    2,
                )

            if str(row.solidity) not in ["oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead", "autoDetcted"]:
                cv2.rectangle(
                    colorInputImage,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    (0, 255, 0),
                    2,
                )
                
        return colorInputImage

    def returnArrayOfImagesForFrame(
        self, frameANumber, frameB, sameFrame, indexOfObjects
    ):
        perCycleNumber = 9  # total -1
        boundingBoxData = self.lastCalculatedDictOfLDADF[
            "frame_no_" + str(frameANumber)
        ].iloc[indexOfObjects : (indexOfObjects + perCycleNumber), :]
        # .iloc[indexOfObjects : indexOfObjects + 5, :]
        seriesOfImages = pd.Series()
        for index, row in boundingBoxData.iterrows():
            
            imageSnip = frameB[row.bbox0 : row.bbox2, row.bbox1 : row.bbox3]
            seriesOfImages.at[index] = imageSnip
        return seriesOfImages

    def computeLDBetweenTwoFrames(self, frameA, frameB, dataFrame1, changeThreshold):
        return estimateLiveDead().countAndFindLiveDead(
            frameA, frameB, dataFrame1, changeThreshold
        )

    def computeOverMultipleFrames(
        self,
        addSkip,
        firstFrameNo,
        totalFramesToRun,
        changeThreshold,
        pgBarUpdate=None,
        live=True,
        activity=False,
        liveAndActivity=False
    ):
        sizeArray = [self.threshParamArray[2], self.threshParamArray[3]]
            
        # self.number_of_frames = self.video_object.get(cv2.CAP_PROP_POS_FRAMES)
        dictOfLDADF = {}  # dict of live dead activity data frame
        # int(np.minimum(totalFramesToRun, self.number_of_frames))
        totalIters = len(range(int(firstFrameNo), int(totalFramesToRun), int(addSkip)))
        self.lastSkip = int(addSkip)
        
        self.lastFirstFrame = int(firstFrameNo)
        for currentIndex, frame_no in enumerate(range(int(firstFrameNo), int(totalFramesToRun), int(addSkip))):

            if pgBarUpdate is not None:
                pgBarUpdate.setValue(((currentIndex) * 100) // (totalIters - 1))
                QApplication.processEvents()

           
            if frame_no == firstFrameNo:
                actFrameA =  self.getCleanedImageFromFrame(
                        self.getCroppedFrameFromVideo(
                            self.getUncroppedFrameFromVideo(frame_no)
                        ),
                        self.cleanParamArray,
                    )
                frameA = self.getThresholdedImageFromFrame(actFrameA, self.threshParamArray)

            else:
                # slightly ieffecient
                self.lastTotalFramesToRun = frame_no
                actFrameA = actFrameB
                frameA = frameB
            
            actFrameB = self.getCleanedImageFromFrame(
                    self.getCroppedFrameFromVideo(
                        self.getUncroppedFrameFromVideo(frame_no + addSkip)
                    ),
                    self.cleanParamArray,
                )
            frameB = self.getThresholdedImageFromFrame(actFrameB,self.threshParamArray)

            if liveAndActivity:
                # change to a single loop later
                ldOnlyTable = estimateLiveDead().countAndFindLiveDead(
                    frameA,
                    frameB,
                    self.computePropertiesOfFrame(frameA, sizeArray),
                    changeThreshold,
                )
                activityandLDTable = estimateActivity().countActivity(
                    actFrameA, actFrameB, ldOnlyTable
                )
                dictOfLDADF["frame_no_" + str(frame_no)] = activityandLDTable
            elif activity:
                activityOnlyTable = estimateActivity().countActivity(
                    actFrameA, actFrameB, self.computePropertiesOfFrame(frameA, sizeArray)
                )
                dictOfLDADF["frame_no_" + str(frame_no)] = activityOnlyTable
            elif live:
                ldOnlyTable = estimateLiveDead().countAndFindLiveDead(
                    frameA,
                    frameB,
                    self.computePropertiesOfFrame(frameA, sizeArray),
                    changeThreshold,
                )
                dictOfLDADF["frame_no_" + str(frame_no)] = ldOnlyTable

        self.lastCalculatedDictOfLDADF = dictOfLDADF
        return self.lastCalculatedDictOfLDADF
    
    def checkIfMovieNameIsCorrect(self, movieName):
        return os.path.basename(self.movie_name) == movieName

    def applyCalculatedDictToFrame(
        self, live=None, activity=None, liveAndActivity=None, frame_no=None, showActivity=None, activityFilterThresh=None, showLive=None, showDead=None, 
    ):
        if frame_no == None:
            frame_no=1
        if live == None:
            live = True
        if activity == None:
            activity = False
        if liveAndActivity == None:
            liveAndActivity=False
        if showActivity == None:
            showActivity=True
        if activityFilterThresh == None:
            activityFilterThresh=0.0
        if showLive == None:
            showLive = True
        if showDead == None:
            showDead = False

        choiceMode = 1 # Body color, boxes
        inputImageFrame = self.getCroppedFrameFromVideo(
            self.getUncroppedFrameFromVideo(frame_no)
        )
        if len(inputImageFrame.shape) == 3:
            colorInputImage = inputImageFrame.copy()
        else:
            colorInputImage = cv2.cvtColor(inputImageFrame, cv2.COLOR_GRAY2RGB)
        count = 0
        for index, row in self.lastCalculatedDictOfLDADF[
            "frame_no_" + str(frame_no)
        ].iterrows():
         if choiceMode == 0:
            if activity or liveAndActivity:
                try:
                    cv2.rectangle(
                        colorInputImage,
                        (row.bbox1, row.bbox0),
                        (row.bbox3, row.bbox2),
                        plt.cm.jet(row.activityStatus)[:, :3][0] * 255,
                        2,
                    )
                    cv2.putText(colorInputImage,str(index), (row.bbox1,row.bbox0), cv2.FONT_HERSHEY_SIMPLEX, 0.4,[255,255,255] )
                    cv2.putText(colorInputImage,"["+str(round(row.activityStatus[0],2)).strip("0")+"]", (row.bbox3,row.bbox2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, plt.cm.jet(row.activityStatus)[:, :3][0] * 255)

                except:
                    pass
            if live or liveAndActivity:
                if row.ldStatus == True:
                    count = count+1
                    cv2.circle(colorInputImage, (row.centroid1, row.centroid0), 4, (0, 0, 255,0.5), -1) 
                    
                else:
                    cv2.circle(colorInputImage, (row.centroid1, row.centroid0), 4, (255, 0, 0), -1) 
         elif choiceMode == 1:
            if (activity or liveAndActivity) and showActivity:
                try:
                    if row.activityStatus >= activityFilterThresh:
                         colorInputImage[row.coords[:,0],row.coords[:,1],] = [0,0,0]   
                         colorInputImage[row.coords[:,0],row.coords[:,1]] = plt.cm.jet(row.activityStatus)[:, :3][0] * 255  
                         cv2.putText(colorInputImage,str(index), (row.bbox1,row.bbox0), cv2.FONT_HERSHEY_SIMPLEX, 0.4,[255,255,255] )
                         cv2.putText(colorInputImage,"["+str(round(row.activityStatus[0],2)).strip("0")+"]", (row.bbox3,row.bbox2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, plt.cm.jet(row.activityStatus)[:, :3][0] * 255)

                    else:
                        print(row.activityStatus) 
                except:
                    pass

            if live or liveAndActivity:
                if (row.ldStatus == True) and showLive:
                    count = count+1
                    cv2.rectangle(
                        colorInputImage,
                        (row.bbox1, row.bbox0),
                        (row.bbox3, row.bbox2),
                        (0, 0, 255,0.5),
                        1,
                    )
                    #cv2.circle(colorInputImage, (row.centroid1, row.centroid0), 4, (0, 0, 255,0.5), -1) 
                    
                if (row.ldStatus == False) and showDead:
                    cv2.rectangle(
                        colorInputImage,
                        (row.bbox1, row.bbox0),
                        (row.bbox3, row.bbox2),
                        (255, 0, 0,0.5),
                        1,
                    )
                    #cv2.circle(colorInputImage, (row.centroid1, row.centroid0), 4, (255, 0, 0), -1) 
  

        if live or liveAndActivity:
           count = "Live objects: "+str(count)+" Total objects: "+str(index+1)
        else:
           count = "Total objects: "+str((index+1))

        return colorInputImage, count

    def applyFirstDictEntryToThreeFrames(
        self, live=True, activity=False, liveAndActivity=False
    ):
        input_list = range(
            int(self.lastFirstFrame), int(self.lastTotalFramesToRun), int(self.lastSkip)
        )
        numberOfElements = len(input_list)
        middle = float(numberOfElements) / 2
        if middle % 2 != 0:
            middleFrame = input_list[int(middle - 0.5)]
        else:
            middleFrame = input_list[int(middle)]

        inputImageFrame1 = self.getCroppedFrameFromVideo(
            self.getUncroppedFrameFromVideo(self.lastFirstFrame)
        )
        inputImageFrame2 = self.getCroppedFrameFromVideo(
            self.getUncroppedFrameFromVideo(middleFrame)
        )
        inputImageFrame3 = self.getCroppedFrameFromVideo(
            self.getUncroppedFrameFromVideo(self.lastTotalFramesToRun)
        )

        if len(inputImageFrame1.shape) == 3:
            colorInputImage1 = inputImageFrame1.copy()
            colorInputImage2 = inputImageFrame2.copy()
            colorInputImage3 = inputImageFrame3.copy()
        else:
            colorInputImage1 = cv2.cvtColor(inputImageFrame1, cv2.COLOR_GRAY2RGB)
            colorInputImage2 = cv2.cvtColor(inputImageFrame2, cv2.COLOR_GRAY2RGB)
            colorInputImage3 = cv2.cvtColor(inputImageFrame3, cv2.COLOR_GRAY2RGB)

        for index, row in self.lastCalculatedDictOfLDADF[
            "frame_no_" + str(self.lastFirstFrame)
        ].iterrows():
            if activity or liveAndActivity:
                cv2.rectangle(
                    colorInputImage1,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    plt.cm.jet(row.activityStatus)[:, :3][0] * 255,
                    2,
                )
                cv2.rectangle(
                    colorInputImage2,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    plt.cm.jet(row.activityStatus)[:, :3][0] * 255,
                    2,
                )
                cv2.rectangle(
                    colorInputImage3,
                    (row.bbox1, row.bbox0),
                    (row.bbox3, row.bbox2),
                    plt.cm.jet(row.activityStatus)[:, :3][0] * 255,
                    2,
                )
            if live or liveAndActivity:
                if row.ldStatus is True:
                    cv2.drawMarker(
                        colorInputImage1,
                        (row.centroid1, row.centroid0),
                        (255, 255, 0),
                        1,
                    )
                    cv2.drawMarker(
                        colorInputImage2,
                        (row.centroid1, row.centroid0),
                        (255, 255, 0),
                        1,
                    )
                    cv2.drawMarker(
                        colorInputImage3,
                        (row.centroid1, row.centroid0),
                        (255, 255, 0),
                        1,
                    )
                else:
                    cv2.drawMarker(
                        colorInputImage1,
                        (row.centroid1, row.centroid0),
                        (255, 0, 255),
                        1,
                    )
                    cv2.drawMarker(
                        colorInputImage2,
                        (row.centroid1, row.centroid0),
                        (255, 0, 255),
                        1,
                    )
                    cv2.drawMarker(
                        colorInputImage3,
                        (row.centroid1, row.centroid0),
                        (255, 0, 255),
                        1,
                    )

        return colorInputImage1, colorInputImage2, colorInputImage3

    def computeActivityBetweenTwoFrames(self, frameA, frameB, dataFrame1):
        return estimateActivity().countActivity(frameA, frameB, dataFrame1)

    def returnFirstCroppedImage(self):
        pass

    def submitAnnotateToMovie(self, patchesDictionary, pgrBar = None):
        

        def filterBasedOn(patches,value):
            arrayOfPatches = []
            for patch in patches:
                if patch.addName == value:     # orange add all
                   arrayOfPatches.append(patch)
            return arrayOfPatches


        # delete overlapping patches from self
        addAll ={}
        addOnce ={}
        deleteAll ={}
        deleteOnce ={}
        deadOnce ={}

        for key, patches in patchesDictionary.items():
            #addAll[key] = filterBasedOn(patches,"addAll")
            deadOnce[key] = filterBasedOn(patches,"deadOnce")
            deleteOnce[key] = filterBasedOn(patches,"deleteOnce")
            #deleteAll[key] = filterBasedOn(patches,"deleteAll")
            addOnce[key]   = filterBasedOn(patches,"addOnce")   
         
        # then first delete from all frames
        def deleteUsingList(deleteFrom, deleteBasedOn, everyWhere = False):
            for key, patches in deleteBasedOn.items():
                if len(patches) ==0:
                    continue
                
                for patch in patches:
                    patch_left_x   = min(patch._x0,patch._x1)
                    patch_right_x  = max(patch._x0,patch._x1)
                    patch_top_y    = min(patch._y0,patch._y1)
                    patch_bottom_y = max(patch._y0,patch._y1)  
                    
                    if not everyWhere:
                        key1 = "frame_no_" + str(key)
                        left_x = deleteFrom[key1].bbox1
                        right_x = deleteFrom[key1].bbox3
                        top_y = deleteFrom[key1].bbox0
                        bottom_y = deleteFrom[key1].bbox2
                        try:
                           doIntersect = ~ ((patch_left_x >= right_x) | (patch_right_x <= left_x) | (patch_top_y >= bottom_y) | (patch_bottom_y <= top_y))
                           deleteFrom[key1].drop(deleteFrom[key1][doIntersect.values].index,inplace=True)
                        except:
                            pass
                    if everyWhere:
                        for key1, dataSeries in deleteFrom.items():   
                            doIntersect =[] 
                            left_x = deleteFrom[key1].bbox1
                            right_x = deleteFrom[key1].bbox3
                            top_y = deleteFrom[key1].bbox0
                            bottom_y = deleteFrom[key1].bbox2
                            doIntersect = ~ ((patch_left_x > right_x) | (patch_right_x < left_x) | (patch_top_y > bottom_y) | (patch_bottom_y < top_y))
                            deleteFrom[key1].drop(dataSeries[doIntersect.values].index,inplace=True)
            return deleteFrom


        #self.lastCalculatedDictOfLDADF= deleteUsingList(self.lastCalculatedDictOfLDADF,deleteAll,True)

        self.lastCalculatedDictOfLDADF= deleteUsingList(self.lastCalculatedDictOfLDADF,deleteOnce)
        #self.lastCalculatedDictOfLDADF= deleteUsingList(self.lastCalculatedDictOfLDADF,addAll,True)
        #self.lastCalculatedDictOfLDADF= deleteUsingList(self.lastCalculatedDictOfLDADF,addOnce)
        #self.lastCalculatedDictOfLDADF= deleteUsingList(self.lastCalculatedDictOfLDADF,deadOnce)
        
        commonDictionaryForSingleLoop ={}
        for key in set().union(addOnce, deadOnce):
            if key in addOnce: commonDictionaryForSingleLoop.setdefault(key, []).extend(addOnce[key])
            if key in deadOnce: commonDictionaryForSingleLoop.setdefault(key, []).extend(deadOnce[key])

        try:
           annotatedDictOnce = self.addMeasureBasedOnMode(commonDictionaryForSingleLoop, pgBarUpdate = pgrBar)
           for key, values in annotatedDictOnce.items():
            self.lastCalculatedDictOfLDADF[key] = self.lastCalculatedDictOfLDADF[key].append(annotatedDictOnce[key], ignore_index = True) 
        except:
            pass

        # try:
        #    annotatedDictDeadOnce = self.addMeasureBasedOnMode(deadOnce, pgBarUpdate = pgrBar)
        #    for key, values in annotatedDictDeadOnce.items():
        #     annotatedDictDeadOnce[key].ldStatus = False
        #     self.lastCalculatedDictOfLDADF[key] = self.lastCalculatedDictOfLDADF[key].append(annotatedDictDeadOnce[key], ignore_index = True) 
        # except:
        #     pass
        

        # arrayOfAddAllPatches = sum(addAll.values(), []) 
        # addAllDict ={}
        # for key, values in self.lastCalculatedDictOfLDADF.items():
        #     addAllDict[key.replace('frame_no_','')]= arrayOfAddAllPatches
        
        #annotatedDictAll = self.addMeasureBasedOnMode(addAllDict)
        
        

        


        #for key, values in annotatedDictAll.items():
         #  self.lastCalculastedDictOfLDADF[key] = self.lastCalculatedDictOfLDADF[key].append(annotatedDictAll[key], ignore_index = True) 

 
    def addMeasureBasedOnMode(self, addUsing, liveAndActivity = False, activity = True, live = False, pgBarUpdate = None):
        firstFrameNo = int(list(self.lastCalculatedDictOfLDADF.keys())[0].replace('frame_no_',''))
        totalFramesToRun = int(list(self.lastCalculatedDictOfLDADF.keys())[-1].replace('frame_no_',''))
        addSkip = int(list(self.lastCalculatedDictOfLDADF.keys())[1].replace('frame_no_',''))-int(list(self.lastCalculatedDictOfLDADF.keys())[0].replace('frame_no_',''))
        totalIters = len(addUsing.keys())
        dictOfLDADF = {}  # dict of live dead activity data frame)
        for index, (key, patches) in enumerate(addUsing.items()):

                if len(patches) == 0:
                    continue
                frame_no = int(key)
                dataSeries = pd.DataFrame(data=None, columns=self.lastCalculatedDictOfLDADF[list(self.lastCalculatedDictOfLDADF.keys())[1]].columns)
                
                threshParamArray = self.threshParamArray
                threshParamArray[2] = 0
                threshParamArray[3] = 2147483647 # maximum C long
                frameA = thresholdImage().thresholdInputMovie(self.getCleanedImageFromFrame(
                                    self.getCroppedFrameFromVideo(
                                        self.getUncroppedFrameFromVideo(frame_no)
                                    ),
                                    self.cleanParamArray,
                                ),  threshParamArray)
                
                actFrameA = self.getCleanedImageFromFrame(
                                    self.getCroppedFrameFromVideo(
                                        self.getUncroppedFrameFromVideo(frame_no)
                                    ),
                                    self.cleanParamArray,
                                )
                frameB = thresholdImage().thresholdInputMovie(self.getCleanedImageFromFrame(
                                    self.getCroppedFrameFromVideo(
                                        self.getUncroppedFrameFromVideo(frame_no + addSkip)
                                    ),
                                    self.cleanParamArray,
                                ),  threshParamArray)

                actFrameB = self.getCleanedImageFromFrame(
                                        self.getCroppedFrameFromVideo(
                                            self.getUncroppedFrameFromVideo(frame_no + addSkip)
                                        ),
                                        self.cleanParamArray,
                                    )
                for patch in patches:
                    xs = range(int(np.ceil(min(patch._x0,patch._x1))),int(np.floor(max(patch._x0,patch._x1)))) 
                    ys = range(int(np.ceil(min(patch._y0,patch._y1))),int(np.floor(max(patch._y0,patch._y1))))
                    dataSeries = dataSeries.append(pd.Series(), ignore_index=True)
                    dataSeries.bbox1[len(dataSeries)-1]  = int(np.ceil(min(patch._x0,patch._x1)))
                    dataSeries.bbox3[len(dataSeries)-1]  = int(np.floor(max(patch._x0,patch._x1)))
                    dataSeries.bbox0[len(dataSeries)-1]  = int(np.ceil(min(patch._y0,patch._y1)))
                    dataSeries.bbox2[len(dataSeries)-1]  = int(np.floor(max(patch._y0,patch._y1)))  
                    dataSeries.centroid0[len(dataSeries)-1]  = int(np.floor((patch._y0+patch._y1)/2))  
                    dataSeries.centroid1[len(dataSeries)-1]  = int(np.floor((patch._x0+patch._x1)/2))  


                    patchCoordinates = np.array([[y,x] for x in xs for y in ys])
                    objectCoordinates = patchCoordinates[frameA[patchCoordinates[:,0],patchCoordinates[:,1]] > 254]
                    if objectCoordinates.shape[0]  < 10 :
                       if patchCoordinates.shape[0] > 100:
                          objectCoordinates = patchCoordinates[1:95]
                       else:
                          objectCoordinates = patchCoordinates

                    
                    dataSeries.coords[len(dataSeries)-1] =  objectCoordinates

                    if patch.addName == "addOnce":
                       dataSeries.ldStatus[len(dataSeries)-1] = True
                    elif patch.addName == "deadOnce":
                       dataSeries.ldStatus[len(dataSeries)-1] = False 
                    
    
                    
                
                if liveAndActivity:
                    # change to a single loop later
                    ldOnlyTable = estimateLiveDead().countAndFindLiveDead(
                        frameA,
                        frameB,
                        dataSeries,
                        changeThreshold,
                    )
                    activityandLDTable = estimateActivity().countActivity(
                        actFrameA, actFrameB, ldOnlyTable
                    )
                    dictOfLDADF["frame_no_" + str(frame_no)] = activityandLDTable
                elif activity:
                    activityOnlyTable = estimateActivity().countActivity(
                        actFrameA, actFrameB, dataSeries
                    )
                    dictOfLDADF["frame_no_" + str(frame_no)] = activityOnlyTable
                elif live:
                    ldOnlyTable = estimateLiveDead().countAndFindLiveDead(
                        frameA,
                        frameB,
                        dataSeries,
                        changeThreshold,
                    )

                    dictOfLDADF["frame_no_" + str(frame_no)] = ldOnlyTable
                if pgBarUpdate is not None:
                        pgBarUpdate.setValue(((index+1) * 100) // (totalIters))
                        QApplication.processEvents()
        
        return dictOfLDADF            
                         




        # then delete from one frame
        # add to one frame
        # add to all frames


    def setMovie(self, moviename):
        self.movie_name = moviename
        self.video_object = cv2.VideoCapture(self.movie_name)

    def setCropCoordinates(self, newMnMaxVertices):
        self.minMaxVertices = newMnMaxVertices
        self.pixToMicronRatio =  (35000/np.abs(self.minMaxVertices[0]-self.minMaxVertices[2])+20245/np.abs(self.minMaxVertices[1]-self.minMaxVertices[3]))/2
        
        

    def trackBarOnChange(self, value):
        self.video_object.set(cv2.CAP_PROP_POS_FRAMES, value)
        err, img = self.video_object.read()
        return img
        
    def returnEntireMovieData(self):
        return {"movieName": self.movie_name,"result": self.lastCalculatedDictOfLDADF,"pixelToUmRatio": self.pixToMicronRatio,"totalFrames": self.number_of_frames,"minMaxVertices": self.minMaxVertices,"angleAverage": self.angleRot, "threshArray": self.threshParamArray, "cleanArray": self.cleanParamArray}
    
     




    def setEntireMovieData(self,uploadededData):
        self.movie_name = uploadededData["movieName"]
        self.setMovie(self.movie_name)
        self.lastCalculatedDictOfLDADF = uploadededData["result"]
        self.pixToMicronRatio = uploadededData["pixelToUmRatio"]
        self.number_of_frames = uploadededData["totalFrames"]
        self.minMaxVertices = uploadededData["minMaxVertices"]
        self.angleRot = uploadededData["angleAverage"]
        self.threshParamArray = uploadededData["threshArray"]
        self.cleanParamArray = uploadededData["cleanArray"]

if __name__ == "__main__":
    frame_no = 0
    advicedAngle = 0
    algoChoice = 1
    movObject = singlemovieobject(r"C:\Users\Sid\Desktop\iPOD 1 (right)\12l.MOV")
    movObject.getCropCoordinates(
        movObject.getUncroppedFrameFromVideo(frame_no), advicedAngle, algoChoice
    )
    movObject.overlayCropOnUncroppedFrame(
        movObject.getUncroppedFrameFromVideo(frame_no)
    )
    newImage = movObject.getCroppedFrameFromVideo(
        movObject.getUncroppedFrameFromVideo(frame_no)
    )
    newImage2 = movObject.getCleanedImageFromFrame(
        newImage.copy(), [180, 255, 0, 100, 250, 0, 0]
    )
    newImage3 = movObject.getThresholdedImageFromFrame(
        newImage2.copy(), [-50, 0, 60, 300, 0, 3]
    )
    rawRegionPropsDF = movObject.computePropertiesOfFrame(newImage3, [30, 250])
    # THRESHED IMAGE SHOULD GO IN
    newTableLiveDead = movObject.computeLDBetweenTwoFrames(
        newImage,
        movObject.getCroppedFrameFromVideo(movObject.getUncroppedFrameFromVideo(100)),
        rawRegionPropsDF,
        2,
    )

    colorInputImage = newImage.copy()
    for index, row in newTableLiveDead.iterrows():
        if newTableLiveDead["ldStatus"][index] == True:
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

    newTableLiveDead = movObject.computeActivityBetweenTwoFrames(
        newImage,
        movObject.getCroppedFrameFromVideo(movObject.getUncroppedFrameFromVideo(100)),
        rawRegionPropsDF,
    )

    colorInputImage = newImage.copy()
    for index, row in newTableLiveDead.iterrows():
        cv2.rectangle(
            colorInputImage,
            (row.bbox1, row.bbox0),
            (row.bbox3, row.bbox2),
            plt.cm.jet(row.activityStatus)[:, :3][0] * 255,
            2,
        )

    cv2.imshow("withObjects", colorInputImage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
