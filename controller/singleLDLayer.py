import sys
from model.dataModels.userInput import userDataInputClass
from model.singlemovie import singlemovieobject


class singleMovieController:
    def __init__(self):
        self.dataAccessModelObject = userDataInputClass()
        self.singleMovieModelObject = singlemovieobject("")

    def testAction(self, text):
        return print(text)
    
    def checkIfMovieNameIsCorrect(self, movieName):
        return self.singleMovieModelObject.checkIfMovieNameIsCorrect(movieName)

    def getEntireMovieData(self):
        return self.singleMovieModelObject.returnEntireMovieData()
    
    def setEntireMovieData(self, uploadededData):
        self.singleMovieModelObject.setEntireMovieData(uploadededData)

    def submitAnnotateToMovie(self, patchesDictionary, pgrBar = None):
        self.singleMovieModelObject.submitAnnotateToMovie(patchesDictionary, pgrBar)

    def moviesInInputFolderByUser(self, inputFolderString):
        return self.dataAccessModelObject.getAllMovieFilesInFolder(inputFolderString)

    def getRotatedImage(self,frame_no =0, newAngle = None ):
        return self.singleMovieModelObject.getUncroppedFrameFromVideoRotated(frame_no, altAngle= newAngle)

    
    def showOriginalUncropImage(self):
        return self.singleMovieModelObject.getUncroppedFrameFromVideoRotated(0)

    def showOriginalUncropImageAtFrame(self, frame_no):
        return self.singleMovieModelObject.getUncroppedFrameFromVideoRotated(frame_no)

    def showAutoCropImage(self, angle):
        self.singleMovieModelObject.getCropCoordinates(
            self.singleMovieModelObject.getUncroppedFrameFromVideo(0), angle, 1
        )
        return self.singleMovieModelObject.overlayCropOnUncroppedFrame(
            self.singleMovieModelObject.getUncroppedFrameFromVideo(0)
        )

    def showCroppedImageAtFrame(self, frame_no):
        return self.singleMovieModelObject.overlayCropOnUncroppedFrame(self.singleMovieModelObject.getUncroppedFrameFromVideo(frame_no))

    def updateManualCropCoordinates(self, newMinMaxCoordinates):
        self.singleMovieModelObject.setCropCoordinates(newMinMaxCoordinates)

    def updateManualCropAngle(self, newAngle):
        self.singleMovieModelObject.setRotationAngle(newAngle)

    def setMovieName(self, newName):
        self.singleMovieModelObject.setMovie(newName)

    def showManualCropImage(self):

        return self.singleMovieModelObject.overlayCropOnUncroppedFrame(
            self.singleMovieModelObject.getUncroppedFrameFromVideo(0)
        )

    def getCroppedImage(self, frame_no):
        return self.singleMovieModelObject.getCroppedFrameFromVideo(
            self.singleMovieModelObject.getUncroppedFrameFromVideo(frame_no)
        )

    def getPixelToUmRatio(self):
        return self.singleMovieModelObject.getPixelToUmRatio()

    def getCleanedImage(self, imageFrame, tempArray):
        return self.singleMovieModelObject.getCleanedImageFromFrame(
            imageFrame, tempArray
        )

    def getThreshedImage(self, imageFrame, tempArray):
        return self.singleMovieModelObject.getThresholdedImageFromFrame(
            imageFrame, tempArray
        )

    def getPropertiesDataFrameFromImage(self, inputImageFrame, tempArray):
        return self.singleMovieModelObject.computePropertiesOfFrame(
            inputImageFrame, tempArray
        )

    def getImageWithBoundingBoxApplied(self, inputImageFrame, propertiesDataFrame):
        return self.singleMovieModelObject.putBoundingBoxesOnFrame(
            inputImageFrame, propertiesDataFrame
        )

    def getArrayOfImagesFromBoundingBoxData(
        self, frameANumber, frameB, sameFrame, indexOfObjects
    ):
        return self.singleMovieModelObject.returnArrayOfImagesForFrame(
            frameANumber, frameB, sameFrame, indexOfObjects
        )

    def estimateLifeBasedOnMode(
        self,
        addSkip,
        firstFrameNo,
        totalFramesToRun,
        changeThreshold,
        pgBarUpdate=None,
        live=False,
        activity=False,
        liveAndActivity=True,
    ):
        return self.singleMovieModelObject.computeOverMultipleFrames(
            addSkip,
            firstFrameNo,
            totalFramesToRun,
            changeThreshold,
            pgBarUpdate,
            live,
            activity,
            liveAndActivity,
        )

    def getAssayImageBasedOnMode(
        self, live=True, activity=True, liveAndActivity=False, frame_no=1,showActivity=True, activityFilterThresh=0, showLive=True, showDead=False
    ):
        return self.singleMovieModelObject.applyCalculatedDictToFrame(
            live, activity, liveAndActivity, frame_no, showActivity, activityFilterThresh, showLive, showDead,
            
        )

    def getThreeAssayImageToCheckResult(
        self, live=True, activity=True, liveAndActivity=False
    ):
        return self.singleMovieModelObject.applyFirstDictEntryToThreeFrames(
            live, activity, liveAndActivity
        )

    def trackBarOnChange(self, value):
        return self.singleMovieModelObject.trackBarOnChange(value)

    def resetmovieObject(self):
        del self.singleMovieModelObject
        self.singleMovieModelObject = singlemovieobject("")

    def getTotalNumberOfFrames(self):
        return self.singleMovieModelObject.getNumberOfFrames()

