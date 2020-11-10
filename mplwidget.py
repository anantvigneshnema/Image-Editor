from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sip
import math
from matplotlib.backends.backend_qt5agg import FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Rectangle


class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setParent(None)
        #self.fig =Figure(tight_layout=True)
        self.fig =Figure()
        left = 0.0
        bottom = 0.0
        width = 1
        height = 1
        self.fig.add_axes([left, bottom, width, height])
        self.canvas = FigureCanvas(self.fig)
        self.fig.set_facecolor([0.23,0.23,0.23,0.5])
        self.canvas.axes = self.canvas.figure.gca()

        #self.canvas.figure.tight_layout(pad=0)
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas)
        self.mpl_toolbar = my_toolbar(self.canvas, self)
        self.mpl_toolbar .setParentClass(self)
        self.mpl_toolbar.setMinimumWidth(100)
    
        self.mpl_toolbar.setFixedHeight(26)
        self.mpl_toolbar.setStyleSheet("QToolBar { opacity: 1;border: 0px; background-color: rgb(133, 196, 65); border-bottom: 1px solid #19232D;padding: 2px;  font-weight: bold;spacing: 2px; } ")
        self.mpl_toolbar.setObjectName("myToolBar")

        #self.canvas.mpl_connect("resize_event", self.resize)
        self.vertical_layout.addWidget(self.mpl_toolbar)
        self.setLayout(self.vertical_layout)
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.rect = Rectangle((0, 0), 1, 1)
        self.updateSecondImage = None
        self.patchesTotal = 0
        self.typeOfAnnotation = "autoDetcted"
        self.frameAtString = "Frame 0"
        self.currentSelectedOption = None

        self.AllBoxListDictionary = {"eraseBox" : [],
                                     "oneWormLive" : [],
                                     "multiWormLive" : [],
                                     "oneWormDead" : [], 
                                     "multiWormDead" : [],
                                     "miscBoxes" : [],
                                     "autoDetcted": []}

        self.eraseBoxXYValues = self.AllBoxListDictionary["eraseBox"]
        self.addBoxXYValues = self.AllBoxListDictionary["miscBoxes"]
        self.oneWormLiveBoxXYValues = self.AllBoxListDictionary["oneWormLive"]
        self.multiWormLiveBoxXYValues = self.AllBoxListDictionary["multiWormLive"]
        self.oneWormDeadBoxXYValues = self.AllBoxListDictionary["oneWormDead"]
        self.multiWormDeadBoxXYValues = self.AllBoxListDictionary["multiWormDead"]
        self.autoDetectedBoxXYValues = self.AllBoxListDictionary["autoDetcted"]
        self.tempList = []

    
    def resetAllBoxListDictionary(self):
        self.AllBoxListDictionary = {"eraseBox" : [],
                                     "oneWormLive" : [],
                                     "multiWormLive" : [],
                                     "oneWormDead" : [], 
                                     "multiWormDead" : [],
                                     "miscBoxes" : [],
                                     "autoDetcted": []}

    def updateAllBoxListDictionary(self):
        self.AllBoxListDictionary["eraseBox"] = self.eraseBoxXYValues
        self.AllBoxListDictionary["miscBoxes"] = self.addBoxXYValues
        self.AllBoxListDictionary["oneWormLive"] = self.oneWormLiveBoxXYValues
        self.AllBoxListDictionary["multiWormLive"] = self.multiWormLiveBoxXYValues
        self.AllBoxListDictionary["oneWormDead"] = self.oneWormDeadBoxXYValues
        self.AllBoxListDictionary["multiWormDead"] = self.multiWormDeadBoxXYValues
        self.AllBoxListDictionary["autoDetcted"] = self.autoDetectedBoxXYValues

    def updateAllListFromAllBoxListDictionary(self):
        self.eraseBoxXYValues = self.AllBoxListDictionary["eraseBox"]
        self.addBoxXYValues = self.AllBoxListDictionary["miscBoxes"]
        self.oneWormLiveBoxXYValues = self.AllBoxListDictionary["oneWormLive"]
        self.multiWormLiveBoxXYValues = self.AllBoxListDictionary["multiWormLive"]
        self.oneWormDeadBoxXYValues = self.AllBoxListDictionary["oneWormDead"]
        self.multiWormDeadBoxXYValues = self.AllBoxListDictionary["multiWormDead"]
        self.autoDetectedBoxXYValues = self.AllBoxListDictionary["autoDetcted"]

    def setFrameAtString(self, text):
        self.frameAtString = text
    
    def getFrameAtString(self):
        return self.frameAtString

    def getCurrentSelectedOption(self):
        return self.currentSelectedOption

    def setCurrentSelectedOption(self, option):
        self.currentSelectedOption = option


    def setDarkTheme(self):
        self.mpl_toolbar.setStyleSheet("QToolBar#myToolBar{ border: 0px; background-color: rgb(133, 0,s 65); border-bottom: 1px solid #19232D;padding: 2px;  font-weight: bold;spacing: 2px; } ")
        self.fig.set_facecolor([0.23,0.23,0.23,0.5])
        #self.fig.set_facecolor('grey')
        self.canvas.draw()

    def setGreenTheme(self):
        self.mpl_toolbar.setStyleSheet("QToolBar { border: 0px; background-color: rgb(133, 196, 65); border-bottom: 1px solid #19232D;padding: 2px;  font-weight: bold;spacing: 2px; } ")
        self.fig.set_facecolor('grey')
        self.canvas.draw()

    def setTypeOfAnnotation(self,text):
        self.typeOfAnnotation = text



    def restrictCanvasMinimumSize(self, size):
        self.canvas.setMinimumSize(size)

    def unmountWidgetAndClear(self):
        self.vertical_layout.removeWidget(self.canvas)
        self.vertical_layout.removeWidget(self.scroll)
        self.scroll.setParent(None)
        self.canvas.setParent(None)
        sip.delete(self.scroll)
        del self.canvas
        self.scroll = None
        self.canvas = None
        self.canvas = FigureCanvas(Figure())
        self.canvas.axes = self.canvas.figure.gca()
        #self.canvas.figure.tight_layout()
        self.scroll = QtWidgets.QScrollArea(self)
        self.scroll.setWidgetResizable(True)

    def connectClickListnerToCurrentImageForCrop(self, givenController, updateSecondImage = None, listOfControllers = None, keyForController = None):
        self.cid1 = self.canvas.mpl_connect(
            "button_press_event", self.on_press_for_crop
        )
        self.cid2 = self.canvas.mpl_connect("motion_notify_event", self.onmove_for_crop)
        self.cid3 = self.canvas.mpl_connect(
            "button_release_event", self.on_release_for_crop
        )
        self.givenControllerObject = givenController
        self.updateSecondImage = updateSecondImage
        self.pressevent = None
        self.listOfControllers = listOfControllers
        self.keyForController = keyForController

    def on_press_for_crop(self, event):
        if (self.mpl_toolbar.mode):
           return

        try:
            self.rect.remove()
        except:
            pass
        self.addedPatch = None
        self.x0 = event.xdata
        self.y0 = event.ydata
        self.rect = Rectangle((self.x0, self.y0), 1, 1)
        self.rect._alpha = 0.5
        self.rect._linewidth = 2
        self.rect.set_color("C2")
        self.rect.set
        self.pressevent = 1
        self.addedPatch = self.canvas.axes.add_patch(self.rect)

    def on_release_for_crop(self, event):
        if (self.mpl_toolbar.mode):
           return

        self.pressevent = None

        minMaxVertices = [
            int(np.ceil(min(self.x0, self.x1))),
            int(np.ceil(min(self.y0, self.y1))),
            int(np.round(max(self.x0, self.x1))),
            int(np.round(max(self.y0, self.y1))),
        ]
        self.givenControllerObject.updateManualCropCoordinates(minMaxVertices)
        image = self.givenControllerObject.showManualCropImage()
        self.canvas.axes.clear()
        self.canvas.axes.axis("off")
        self.canvas.axes.imshow(image)
        self.canvas.draw()
        if self.updateSecondImage is not None:
            self.updateSecondImage.canvas.axes.clear()
            self.updateSecondImage.canvas.axes.axis("off")
            self.updateSecondImage.canvas.axes.imshow(self.givenControllerObject.getCroppedImage(0))
            self.updateSecondImage.canvas.draw()
            self.listOfControllers[self.keyForController] = self.givenControllerObject

    def onmove_for_crop(self, event):
        

        if self.pressevent is None:
            return
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.canvas.draw()

    def disconnectClickListnerFromCurrentImageForCrop(self):
        try:
            self.canvas.mpl_disconnect(self.cid1)
            self.canvas.mpl_disconnect(self.cid2)
            self.canvas.mpl_disconnect(self.cid3)
            self.updateSecondImage =None
        except:
            pass

    def getCurrentScrollParam(self):
        self.currentVerticalSliderValue = self.scroll.verticalScrollBar().value()
        self.currentHorizontalSliderValue = self.scroll.horizontalScrollBar().value()

    def resetCurrentScrollParam(self):
        self.scroll.verticalScrollBar().setValue(self.currentVerticalSliderValue)
        self.scroll.horizontalScrollBar().setValue(self.currentHorizontalSliderValue)
    
    def resize(self, event):
         # on resize reposition the navigation toolbar to (0,0) of the axes.
         x,y = self.fig.axes[0].transAxes.transform((0,0))
         figw, figh = self.fig.get_size_inches()
         ynew = figh*self.fig.dpi-y - self.mpl_toolbar.frameGeometry().height()
         self.mpl_toolbar.move(x,ynew)


    def connectClickListnerToCurrentImageForAnnotate(self, givenController, updateSecondImage = None):
        self.cid4 = self.canvas.mpl_connect(
            "button_press_event", self.on_press_for_annotate
        )
        
        self.cid7 = self.canvas.mpl_connect('pick_event', self.onpick)   
        #self.cid7 = self.canvas.mpl_connect('button_press_event', self.right_click_press_for_annotate)   
        self.givenControllerObject = givenController
        self.updateSecondImage = updateSecondImage
        self.pressevent = None


    def autoAnnotateOnOverlay(self, autoDetectedObjects):

        for index, row in autoDetectedObjects.iterrows():
            print(row.bbox3)

            #if self.pressevent is None:
            #    return
            #self.x1 = event.xdata
            #self.y1 = event.ydata
            self.rect.set_width(row.bbox3 - row.bbox1)
            self.rect.set_height(row.bbox2 - row.bbox0)
            self.rect.set_xy((row.bbox1, row.bbox0))


            self.canvas.draw()


            self.rect = Rectangle((row.bbox1, row.bbox0), 1, 1, picker=True )
            self.rect._alpha = 1
            self.rect._edgecolor = (0,1,0,1)
            self.rect._facecolor = (0,0,0,0)

            self.rect._linewidth = 1
            self.rect.set_linestyle('dashed')
            self.rect.addName = self.typeOfAnnotation     
            self.pressevent = 1
            self.canvas.axes.add_patch(self.rect)
            self.patchesTotal =self.patchesTotal+1

            if [row.bbox1, row.bbox0, row.bbox3, row.bbox2] not in self.autoDetectedBoxXYValues:
                self.autoDetectedBoxXYValues.append([row.bbox1, row.bbox0, row.bbox3, row.bbox2])

            # Update latest values
            self.updateAllBoxListDictionary()
            #print(self.typeOfAnnotation)
            '''if self.typeOfAnnotation == "eraseBox":
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])

            if self.typeOfAnnotation not in ["eraseBox", "oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead"]:
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])

            if self.typeOfAnnotation == "oneWormLive":
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])

            if self.typeOfAnnotation == "multiWormLive":
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])

            if self.typeOfAnnotation == "oneWormDead":
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])

            if self.typeOfAnnotation == "multiWormDead":
                if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                    self.tempList.append([self.x0, self.y0, self.x1, self.y1])'''

            #self.canvas.draw()

        #return(self.canvas)

    def on_press_for_annotate(self, event):
        # try:
        #     self.rect.remove()
        # except:
        #     pass
        if (self.mpl_toolbar.mode):
           return

        if event.button == 1 :
            self.cid5 = self.canvas.mpl_connect("motion_notify_event", self.onmove_for_annotate)
            self.cid6 = self.canvas.mpl_connect("button_release_event", self.on_release_for_annotate)

            self.x0 = event.xdata
            self.y0 = event.ydata

            self.rect = Rectangle((self.x0, self.y0), 1, 1, picker=True )
            self.rect._alpha = 1
            if self.typeOfAnnotation not in ["eraseBox", "oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead"]:
               self.rect._edgecolor = (0,1,0,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "autoDetcted":
               self.rect._edgecolor = (0,1,0,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "eraseBox":
               self.rect._edgecolor = (0,0,0,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "oneWormLive":
               self.rect._edgecolor = (0,0,1,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "multiWormLive":
               self.rect._edgecolor = (1,1,0,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "oneWormDead":
               self.rect._edgecolor = (1,0,0,1)
               self.rect._facecolor = (0,0,0,0)
            elif self.typeOfAnnotation == "multiWormDead":
               self.rect._edgecolor = (1,1,1,1)
               self.rect._facecolor = (0,0,0,0)

            
            self.rect._linewidth = 1
            self.rect.set_linestyle('dashed')
            self.rect.addName = self.typeOfAnnotation     
            self.pressevent = 1
            self.canvas.axes.add_patch(self.rect)
            self.patchesTotal =self.patchesTotal+1
        

    def on_release_for_annotate(self, event):
        if (self.mpl_toolbar.mode):
           return

        
        if event.button == 1:
            self.canvas.mpl_disconnect(self.cid5)
            if (self.rect.get_height() == 1) and (self.rect.get_width() == 1):
                self.rect.remove()
            self.pressevent = None
            self.canvas.mpl_disconnect(self.cid6)

        if self.typeOfAnnotation == "eraseBox":
            #print(self.typeOfAnnotation)
            self.eraseBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        if self.typeOfAnnotation not in ["eraseBox", "oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead"]:
            #print(self.typeOfAnnotation)
            self.addBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        if self.typeOfAnnotation == "oneWormLive":
            self.oneWormLiveBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        if self.typeOfAnnotation == "multiWormLive":
            self.multiWormLiveBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        if self.typeOfAnnotation == "oneWormDead":
            self.oneWormDeadBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        if self.typeOfAnnotation == "multiWormDead":
            self.multiWormDeadBoxXYValues.append(self.tempList[-1])
            self.tempList = []

        # updateAllBoxListDictionary(self)
        self.updateAllBoxListDictionary()

        # self.givenControllerObject.updateManualCropCoordinates(minMaxVertices)
        # image = self.givenControllerObject.showManualCropImage()
        # self.canvas.axes.clear()
        # self.canvas.axes.axis("off")
        # self.canvas.axes.imshow(image)
        # self.canvas.draw()
        # if self.updateSecondImage is not None:
        #     self.updateSecondImage.canvas.axes.clear()
        #     self.updateSecondImage.canvas.axes.axis("off")
        #     self.updateSecondImage.canvas.axes.imshow(self.givenControllerObject.getCroppedImage(0))
        #     self.updateSecondImage.canvas.draw()

    def onmove_for_annotate(self, event):
        
        if self.pressevent is None:
            return
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))

        #print(self.typeOfAnnotation)
        if self.typeOfAnnotation == "eraseBox":
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        if self.typeOfAnnotation not in ["eraseBox", "oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead"]:
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        if self.typeOfAnnotation == "oneWormLive":
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        if self.typeOfAnnotation == "multiWormLive":
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        if self.typeOfAnnotation == "oneWormDead":
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        if self.typeOfAnnotation == "multiWormDead":
            if [self.x0, self.y0, self.x1, self.y1] not in self.tempList:
                self.tempList.append([self.x0, self.y0, self.x1, self.y1])

        self.canvas.draw()


    def getEraseBoxXYValues(self):
        return(self.eraseBoxXYValues)

    def getAutoDetctedBoxXYValues(self):
        return(self.autoDetectedBoxXYValues)

    def getAddBoxXYValues(self):
        return(self.addBoxXYValues)

    def getOneWormLiveBoxXYValues(self):
        return(self.oneWormLiveBoxXYValues)

    def getMultiWormLiveBoxXYValues(self):
        return(self.multiWormLiveBoxXYValues)

    def getOneWormDeadBoxXYValues(self):
        return(self.oneWormDeadBoxXYValues)

    def getMultiWormDeadBoxXYValues(self):
        return(self.multiWormDeadBoxXYValues)



    def resetEraseBoxXYValues(self):
        self.eraseBoxXYValues = []

    def resetAutoDetctedBoxXYValues(self):
        self.autoDetectedBoxXYValues = []

    def resetAddBoxXYValues(self):
        self.addBoxXYValues = []

    def resetOneWormLiveBoxXYValues(self):
        self.oneWormLiveBoxXYValues = []

    def resetMultiWormLiveBoxXYValues(self):
        self.multiWormLiveBoxXYValues = []

    def resetOneWormDeadBoxXYValues(self):
        self.oneWormDeadBoxXYValues = []

    def resetMultiWormDeadBoxXYValues(self):
        self.multiWormDeadBoxXYValues = []

    def disconnectClickListnerFromCurrentImageForAnnotate(self):
        try:
            self.canvas.mpl_disconnect(self.cid4)
            
            self.canvas.mpl_disconnect(self.cid7)
            self.updateSecondImage =None
        except:
            pass

    def onpick(self, event):
        #if event.button == 3:       #"3" is the right button
            # print "you click the right button" 
            # print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            # event.button, event.x, event.y, event.xdata, event.ydata)
            #Get the coordinates of the mouse click
            #I create the action
        if (self.mpl_toolbar.mode):
           return    
        if event.mouseevent.button == 3: 
            self.objectPicked= event.artist
            noteAction_1 = QtWidgets.QAction('Delete Box',self)
            noteAction_2 = QtWidgets.QAction('Classify',self)
            #noteAction_5 = QtWidgets.QAction('Add Once',self)
            #noteAction_2 = QtWidgets.QAction('Add Through',self)
            #noteAction_3 = QtWidgets.QAction('Mask Here',self)
            #noteAction_4 = QtWidgets.QAction('Mask Through',self)
            #noteAction_6 = QtWidgets.QAction('Live here',self)
            #noteAction_7 = QtWidgets.QAction('Live all',self)
            #noteAction_8 = QtWidgets.QAction('Dead here',self)
            #noteAction_9 = QtWidgets.QAction('Dead all',self)

            #I create the context menu
            self.popMenu = QtWidgets.QMenu(self)
            self.popMenu.addAction(noteAction_1)
            self.popMenu.addAction(noteAction_2)
            # self.popMenu.addAction(noteAction_2)
            # self.popMenu.addAction(noteAction_3)
            # self.popMenu.addAction(noteAction_4)
            # self.popMenu.addAction(noteAction_5)
            # self.popMenu.addAction(noteAction_6)
            # self.popMenu.addAction(noteAction_7)
            # self.popMenu.addAction(noteAction_8)
            # self.popMenu.addAction(noteAction_9)



            cursor = QtGui.QCursor()
            #self.connect(self.figure_canvas, SIGNAL("clicked()"), self.context_menu)
            #self.popMenu.exec_(self.mapToGlobal(event.globalPos()))
            noteAction_1.triggered.connect(lambda :self.removeThisArea(1))
            noteAction_2.triggered.connect(lambda :self.classifyAsCurrentSelection(1))
            # noteAction_2.triggered.connect(lambda :self.removeThisArea(2))
            # noteAction_3.triggered.connect(lambda :self.removeThisArea(3))
            # noteAction_4.triggered.connect(lambda :self.removeThisArea(4))
            # noteAction_5.triggered.connect(lambda :self.removeThisArea(5))
            # noteAction_6.triggered.connect(lambda :self.removeThisArea(5))
            # noteAction_7.triggered.connect(lambda :self.removeThisArea(2))
            # noteAction_8.triggered.connect(lambda :self.removeThisArea(3))
            # noteAction_9.triggered.connect(lambda :self.removeThisArea(4))



            
            self.popMenu.popup(cursor.pos())
        else:
            return

    def right_click_press_for_annotate(self, event):
        if (self.mpl_toolbar.mode):
           return
        if event.button == 3:       #"3" is the right button
            # print "you click the right button" 
            # print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
            # event.button, event.x, event.y, event.xdata, event.ydata)
            #Get the coordinates of the mouse click
            #I create the action
            noteAction_1 = QtWidgets.QAction('Remove',self)
            noteAction_2 = QtWidgets.QAction('Add',self)
            
            #I create the context menu
            self.popMenu = QtWidgets.QMenu(self)
            self.popMenu.addAction(noteAction_1)
            self.popMenu.addAction(noteAction_2)
            cursor = QtGui.QCursor()
            
            #self.connect(self.figure_canvas, SIGNAL("clicked()"), self.context_menu)
            #self.popMenu.exec_(self.mapToGlobal(event.globalPos()))
            noteAction_1.triggered.connect(lambda eventData = object: self.removeThisArea(eventData))
            noteAction_2.triggered.connect(lambda eventData = object: self.classifyAsCurrentSelection(eventData))
            self.popMenu.popup(cursor.pos())

    def classifyAsCurrentSelection(self, caseNumber):

        # Get all the list values for this frame
        self.updateAllListFromAllBoxListDictionary()

        print("INSIDE classifyAsCurrentSelection")
        
        try:
            if caseNumber  == 1:      # green delete
                print(type(self.objectPicked))
                X0 = self.objectPicked.get_xy()[0]
                Y0 = self.objectPicked.get_xy()[1]
                X1 = X0 + self.objectPicked.get_width()
                Y1 = Y0 + self.objectPicked.get_height()

                selectedBoxCoords = [X0, Y0, X1, Y1]

                if self.currentSelectedOption == "eraseBox":
                    #self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    #self.eraseBoxXYValues.append(selectedBoxCoords)
                    print("Use Delte Option! Right Click -> Delete Box")

                if self.currentSelectedOption == "autoDetcted":
                    #self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    #self.addBoxXYValues.append(selectedBoxCoords)
                    print("Already Selected!")

                if self.currentSelectedOption not in ["oneWormLive", "multiWormLive", "oneWormDead", "multiWormDead", "autoDetcted"]:
                    self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    self.addBoxXYValues.append(selectedBoxCoords)
                    
                    self.rect.set_width(X1 - X0)
                    self.rect.set_height(Y1 - Y0)
                    self.rect.set_xy((X0, Y0))

                    self.rect = Rectangle((X0, Y0), 1, 1, picker=True )
                    self.rect._alpha = 1
                    self.rect._edgecolor = (0,1,0,1)
                    self.rect._facecolor = (0,0,0,0)

                    self.canvas.draw()

                    self.rect._linewidth = 1
                    self.rect.set_linestyle('dashed')
                    self.rect.addName = self.typeOfAnnotation     
                    self.pressevent = 1
                    self.canvas.axes.add_patch(self.rect)


                if self.currentSelectedOption == "oneWormLive" and selectedBoxCoords not in self.oneWormLiveBoxXYValues:
                    
                    self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    self.oneWormLiveBoxXYValues.append(selectedBoxCoords)

                    self.canvas.draw()
                    
                    self.rect.set_width(X1 - X0)
                    self.rect.set_height(Y1 - Y0)
                    self.rect.set_xy((X0, Y0))

                    self.rect = Rectangle((X0, Y0), 1, 1, picker=True )
                    self.rect._alpha = 1
                    self.rect._edgecolor = (0,0,1,1)
                    self.rect._facecolor = (0,0,0,0)

                    self.rect._linewidth = 1
                    self.rect.set_linestyle('dashed')
                    self.rect.addName = self.typeOfAnnotation     
                    self.pressevent = 1
                    self.canvas.axes.add_patch(self.rect)

                    self.canvas.draw()

                if self.currentSelectedOption == "multiWormLive" and selectedBoxCoords not in self.multiWormLiveBoxXYValues:
                    self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    self.multiWormLiveBoxXYValues.append(selectedBoxCoords)

                    self.rect.set_width(X1 - X0)
                    self.rect.set_height(Y1 - Y0)
                    self.rect.set_xy((X0, Y0))

                    self.rect = Rectangle((X0, Y0), 1, 1, picker=True )
                    self.rect._alpha = 1
                    self.rect._edgecolor = (1,1,0,1)
                    self.rect._facecolor = (0,0,0,0)

                    self.canvas.draw()

                    self.rect._linewidth = 1
                    self.rect.set_linestyle('dashed')
                    self.rect.addName = self.typeOfAnnotation     
                    self.pressevent = 1
                    self.canvas.axes.add_patch(self.rect)

                if self.currentSelectedOption == "oneWormDead" and selectedBoxCoords not in self.oneWormDeadBoxXYValues:

                    self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    self.oneWormDeadBoxXYValues.append(selectedBoxCoords)

                    self.rect.set_width(X1 - X0)
                    self.rect.set_height(Y1 - Y0)
                    self.rect.set_xy((X0, Y0))

                    self.rect = Rectangle((X0, Y0), 1, 1, picker=True )
                    self.rect._alpha = 1
                    self.rect._edgecolor = (1,0,0,1)
                    self.rect._facecolor = (0,0,0,0)

                    self.canvas.draw()

                    self.rect._linewidth = 1
                    self.rect.set_linestyle('dashed')
                    self.rect.addName = self.typeOfAnnotation     
                    self.pressevent = 1
                    self.canvas.axes.add_patch(self.rect)

                if self.currentSelectedOption == "multiWormDead" and selectedBoxCoords not in self.multiWormDeadBoxXYValues:
                    self.autoDetectedBoxXYValues.remove(selectedBoxCoords)
                    self.multiWormDeadBoxXYValues.append(selectedBoxCoords)

                    self.rect.set_width(X1 - X0)
                    self.rect.set_height(Y1 - Y0)
                    self.rect.set_xy((X0, Y0))

                    self.rect = Rectangle((X0, Y0), 1, 1, picker=True )
                    self.rect._alpha = 1
                    self.rect._edgecolor = (1,1,1,1)
                    self.rect._facecolor = (0,0,0,0)

                    self.canvas.draw()

                    self.rect._linewidth = 1
                    self.rect.set_linestyle('dashed')
                    self.rect.addName = self.typeOfAnnotation     
                    self.pressevent = 1
                    self.canvas.axes.add_patch(self.rect)

        except:
            print("Delete and Redraw!")
        # updateAllBoxListDictionary(self)
        self.updateAllBoxListDictionary()


    def removeThisArea(self, caseNumber):
        
        # Get all the list values for this frame
        self.updateAllListFromAllBoxListDictionary()

        if caseNumber  == 1:      # green delete
            print(type(self.objectPicked))
            X0 = self.objectPicked.get_xy()[0]
            Y0 = self.objectPicked.get_xy()[1]
            X1 = X0 + self.objectPicked.get_width()
            Y1 = Y0 + self.objectPicked.get_height()

            removeBoxCoords = [X0, Y0, X1, Y1]
            #print(removeBoxCoords)
            self.objectPicked.remove()
            self.patchesTotal = self.patchesTotal-1

            try:
                if removeBoxCoords in self.eraseBoxXYValues:
                    self.eraseBoxXYValues.remove(removeBoxCoords)

                if removeBoxCoords in self.addBoxXYValues:
                    self.addBoxXYValues.remove(removeBoxCoords)

                if removeBoxCoords in self.oneWormLiveBoxXYValues:
                    #print(self.oneWormLiveBoxXYValues)
                    self.oneWormLiveBoxXYValues.remove(removeBoxCoords)
                    #print(self.oneWormLiveBoxXYValues)

                if removeBoxCoords in self.multiWormLiveBoxXYValues:
                    self.multiWormLiveBoxXYValues.remove(removeBoxCoords)

                if removeBoxCoords in self.oneWormDeadBoxXYValues:
                    self.oneWormDeadBoxXYValues.remove(removeBoxCoords)

                if removeBoxCoords in self.multiWormDeadBoxXYValues:
                    self.multiWormDeadBoxXYValues.remove(removeBoxCoords)

                if removeBoxCoords in self.autoDetectedBoxXYValues:
                    print(len(self.autoDetectedBoxXYValues))
                    self.autoDetectedBoxXYValues.remove(removeBoxCoords)
                    print(len(self.autoDetectedBoxXYValues))
            except:
                pass

        # elif caseNumber == 2:     # orange add all
        #     self.objectPicked._facecolor = (1.0, 0.64, 0.0,0.5)
        #     self.objectPicked._alpha  = 0.5
        #     self.objectPicked.addName ="addAll"
        # elif caseNumber == 3:     # black 
        #     self.objectPicked._facecolor = (0,0, 0, 0.8)
        #     self.objectPicked._alpha = 0.8
        #     self.objectPicked.addName ="eraseBox"
        # elif caseNumber == 4:
        #     self.objectPicked._facecolor = ( 0, 0, 0, 0.2)
        #     self.objectPicked._alpha = 0.2
        #     self.objectPicked.addName ="deleteAll"
        # elif caseNumber == 5:
        #     self.objectPicked.set_color("C2")
        #     self._edgecolor = (0, 0, 0, 0)
        #     self.objectPicked.addName ="addBox"
        
        
        self.canvas.draw()
        #print(len(self.canvas.axes.patches))
            #self.canvas.draw()
            #self.on_release_for_annotate(None)
            
    def initializeAnnotationDictionary(self):
        self.currentAnnotationFrame = None
        self.annotationRecordDictionary = {}

    def updateAnnotationDictionary(self):
        
        # When you move away from current Frame call this
        previousFrame = self.currentAnnotationFrame
        if previousFrame is not None:
          self.annotationRecordDictionary[str(previousFrame)] = self.canvas.axes.patches

    def getAnnotationDictionary(self):
        return self.annotationRecordDictionary
    
    def applyAnnotationDictionary(self, frameNumber):
        self.currentAnnotationFrame = frameNumber
        self.canvas.axes.patches = []
        if str(frameNumber) in self.annotationRecordDictionary.keys():           
            for patch in self.annotationRecordDictionary[str(frameNumber)]:
                self.canvas.axes.add_patch(patch)



    def setAnnotationDictionary(self):
        pass

class my_toolbar(NavigationToolbar):

      def setParentClass(self, parentClass ):
          self.parentClass = parentClass

      def set_message(self, s):
          self.message.emit(s)
          if self.coordinates and (s == ""):
             self.locLabel.setText(str(self.parentClass.getFrameAtString())+" "+s)
          else:
             self.locLabel.setText(s)