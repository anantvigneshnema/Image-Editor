# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImageEditorUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from controller.singleLDLayer import singleMovieController
from controller.dataAccessLayer import dataInputOutputClass
import os

import cv2 as cv
import numpy as np

from PIL import Image, ImageEnhance


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(748, 621)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../.designer/08032020/Resources/100_100_downscaled.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setToolTip("")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(0, 20))
        self.splitter.setStyleSheet("QSplitter::handle:vertical {\n"
"background:qlineargradient(x1:0, y1:0, x2:1, y2:1,\n"
"    stop:0 #eee, stop:1 #ccc) ;\n"
"border: 2px solid #777;\n"
"width: 13px;\n"
"margin-top: 2px;\n"
"margin-bottom: 2px;\n"
"border-radius: 4px;\n"
"}\n"
"")
        self.splitter.setFrameShape(QtWidgets.QFrame.Box)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(True)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.verticalLayout_35 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout()
        self.verticalLayout_33.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.cleanImage = MplWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cleanImage.sizePolicy().hasHeightForWidth())
        self.cleanImage.setSizePolicy(sizePolicy)
        self.cleanImage.setMinimumSize(QtCore.QSize(70, 20))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(251, 245, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(209, 204, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(111, 109, 113))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(211, 209, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(251, 245, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(209, 204, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(111, 109, 113))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(211, 209, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(251, 245, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(209, 204, 212))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(111, 109, 113))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(83, 81, 85))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(167, 163, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.cleanImage.setPalette(palette)
        self.cleanImage.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.cleanImage.setAcceptDrops(True)
        self.cleanImage.setAutoFillBackground(False)
        self.cleanImage.setStyleSheet("")
        self.cleanImage.setObjectName("cleanImage")
        self.verticalLayout_33.addWidget(self.cleanImage)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalScrollBar.sizePolicy().hasHeightForWidth())
        self.horizontalScrollBar.setSizePolicy(sizePolicy)
        self.horizontalScrollBar.setMinimumSize(QtCore.QSize(20, 20))
        self.horizontalScrollBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.horizontalScrollBar.setStyleSheet("background-color: rgb(127, 127, 127);")
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.verticalLayout_33.addWidget(self.horizontalScrollBar)
        self.verticalLayout_35.addLayout(self.verticalLayout_33)
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout_14.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_9 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_9.setMinimumSize(QtCore.QSize(300, 509))
        self.dockWidget_9.setMaximumSize(QtCore.QSize(300, 524287))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../.designer/backup/Resources/100_100_downscaled.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dockWidget_9.setWindowIcon(icon1)
        self.dockWidget_9.setStatusTip("")
        self.dockWidget_9.setStyleSheet("")
        self.dockWidget_9.setFloating(False)
        self.dockWidget_9.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.dockWidget_9.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidget_9.setObjectName("dockWidget_9")
        self.dockWidgetContents_16 = QtWidgets.QWidget()
        self.dockWidgetContents_16.setObjectName("dockWidgetContents_16")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.dockWidgetContents_16)
        self.verticalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_32.setSpacing(0)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.tabWidget = QtWidgets.QTabWidget(self.dockWidgetContents_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setToolTip("")
        self.tabWidget.setStyleSheet("\n"
"background-color: rgb(217, 217, 217);\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.dockWidget_2 = QtWidgets.QDockWidget(self.tab)
        self.dockWidget_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_2.sizePolicy().hasHeightForWidth())
        self.dockWidget_2.setSizePolicy(sizePolicy)
        self.dockWidget_2.setMinimumSize(QtCore.QSize(300, 426))
        self.dockWidget_2.setMaximumSize(QtCore.QSize(300, 524287))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        self.dockWidget_2.setPalette(palette)
        self.dockWidget_2.setStyleSheet("QDockWidget::title\n"
"{background: rgb(217, 217, 217);};\n"
"background-color: rgb(217, 217, 217);\n"
"\n"
"border-color: rgb(0, 0, 0);\n"
"\n"
"\n"
"")
        self.dockWidget_2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.dockWidget_2.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.dockWidget_2.setWindowTitle("")
        self.dockWidget_2.setObjectName("dockWidget_2")
        self.dockWidgetContents_3 = QtWidgets.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.layoutWidget_12 = QtWidgets.QWidget(self.dockWidgetContents_3)
        self.layoutWidget_12.setGeometry(QtCore.QRect(10, 70, 281, 201))
        self.layoutWidget_12.setObjectName("layoutWidget_12")
        self.verticalLayout2_3 = QtWidgets.QVBoxLayout(self.layoutWidget_12)
        self.verticalLayout2_3.setContentsMargins(1, 10, 1, 10)
        self.verticalLayout2_3.setObjectName("verticalLayout2_3")
        self.listWidget_7 = QtWidgets.QListWidget(self.layoutWidget_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget_7.sizePolicy().hasHeightForWidth())
        self.listWidget_7.setSizePolicy(sizePolicy)
        self.listWidget_7.setMinimumSize(QtCore.QSize(150, 100))
        self.listWidget_7.setAccessibleDescription("")
        self.listWidget_7.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.listWidget_7.setMidLineWidth(-6)
        self.listWidget_7.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listWidget_7.setAlternatingRowColors(False)
        self.listWidget_7.setTextElideMode(QtCore.Qt.ElideLeft)
        self.listWidget_7.setLayoutMode(QtWidgets.QListView.Batched)
        self.listWidget_7.setObjectName("listWidget_7")
        self.verticalLayout2_3.addWidget(self.listWidget_7)
        self.pushButton_19 = QtWidgets.QPushButton(self.dockWidgetContents_3)
        self.pushButton_19.setGeometry(QtCore.QRect(90, 480, 142, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_19.sizePolicy().hasHeightForWidth())
        self.pushButton_19.setSizePolicy(sizePolicy)
        self.pushButton_19.setMaximumSize(QtCore.QSize(142, 38))
        self.pushButton_19.setStyleSheet("QPushButton {\n"
"color: black;\n"
"background-color: rgb(133, 196, 65);\n"
"border-width: 1px;\n"
"border-color: rgb(0,0,0);\n"
"border-style: solid;\n"
"border-radius: 7;\n"
"padding: 3px;\n"
"font-size: 15px;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"min-width: 130px;\n"
"max-width: 130px;\n"
"min-height: 30px;\n"
"max-height: 30px;\n"
"}\n"
"\n"
"")
        self.pushButton_19.setObjectName("pushButton_19")
        self.layoutWidget = QtWidgets.QWidget(self.dockWidgetContents_3)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 272, 281, 203))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.hiPassFilterLabel_35 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hiPassFilterLabel_35.sizePolicy().hasHeightForWidth())
        self.hiPassFilterLabel_35.setSizePolicy(sizePolicy)
        self.hiPassFilterLabel_35.setMinimumSize(QtCore.QSize(0, 20))
        self.hiPassFilterLabel_35.setMaximumSize(QtCore.QSize(16777215, 20))
        self.hiPassFilterLabel_35.setObjectName("hiPassFilterLabel_35")
        self.verticalLayout_5.addWidget(self.hiPassFilterLabel_35)
        self.horizontalSlider_2 = QtWidgets.QSlider(self.layoutWidget)
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.verticalLayout_5.addWidget(self.horizontalSlider_2)
        self.hiPassFilterLabel_36 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hiPassFilterLabel_36.sizePolicy().hasHeightForWidth())
        self.hiPassFilterLabel_36.setSizePolicy(sizePolicy)
        self.hiPassFilterLabel_36.setMinimumSize(QtCore.QSize(0, 20))
        self.hiPassFilterLabel_36.setMaximumSize(QtCore.QSize(16777215, 20))
        self.hiPassFilterLabel_36.setObjectName("hiPassFilterLabel_36")
        self.verticalLayout_5.addWidget(self.hiPassFilterLabel_36)
        self.horizontalSlider_3 = QtWidgets.QSlider(self.layoutWidget)
        self.horizontalSlider_3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_3.setObjectName("horizontalSlider_3")
        self.verticalLayout_5.addWidget(self.horizontalSlider_3)
        self.hiPassFilterLabel_31 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hiPassFilterLabel_31.sizePolicy().hasHeightForWidth())
        self.hiPassFilterLabel_31.setSizePolicy(sizePolicy)
        self.hiPassFilterLabel_31.setMinimumSize(QtCore.QSize(0, 20))
        self.hiPassFilterLabel_31.setMaximumSize(QtCore.QSize(16777215, 20))
        self.hiPassFilterLabel_31.setObjectName("hiPassFilterLabel_31")
        self.verticalLayout_5.addWidget(self.hiPassFilterLabel_31)
        self.horizontalSlider = QtWidgets.QSlider(self.layoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_5.addWidget(self.horizontalSlider)
        #self.pushButton_21 = QtWidgets.QPushButton(self.layoutWidget)
        '''self.pushButton_21.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"color: black;\n"
"background-color: rgb(255, 255, 255);\n"
"border-width: 1px;\n"
"border-color: rgb(0, 0, 0);;\n"
"border-style: solid;\n"
"border-radius: 7;\n"
"padding: 3px;\n"
"font-size: 15px;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"min-width: 60px;\n"
"max-width: 60px;\n"
"min-height: 13px;\n"
"max-height: 17px;\n"
"}\n"
"\n"
"")'''
        #self.pushButton_21.setObjectName("pushButton_21")
        #self.verticalLayout_5.addWidget(self.pushButton_21)
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.dockWidgetContents_3)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(10, 0, 281, 71))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout1_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout1_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout1_3.setObjectName("verticalLayout1_3")
        self.formLayout_28 = QtWidgets.QFormLayout()
        self.formLayout_28.setContentsMargins(-1, 10, -1, 10)
        self.formLayout_28.setObjectName("formLayout_28")
        self.pushButton_18 = QtWidgets.QPushButton(self.verticalLayoutWidget_4)
        self.pushButton_18.setStyleSheet("\n"
"\n"
"QPushButton {\n"
"color: black;\n"
"background-color: rgb(255, 255, 255);\n"
"border-width: 1px;\n"
"border-color: rgb(0,0,0);\n"
"border-style: solid;\n"
"border-radius: 7;\n"
"padding: 3px;\n"
"font-size: 15px;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"min-width: 60px;\n"
"max-width: 60px;\n"
"min-height: 13px;\n"
"max-height: 13px;\n"
"}\n"
"\n"
"")
        self.pushButton_18.setCheckable(False)
        self.pushButton_18.setFlat(False)
        self.pushButton_18.setObjectName("pushButton_18")
        self.formLayout_28.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.pushButton_18)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.verticalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(100, 0))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.lineEdit_3.setStyleSheet("\n"
"\n"
"QLineEdit { border-width: 1px; border-style: solid; border-color:  rgb(217, 217, 217)  rgb(217, 217, 217) black  rgb(217, 217, 217); }\n"
"")
        self.lineEdit_3.setFrame(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout_28.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.verticalLayout1_3.addLayout(self.formLayout_28)
        self.dockWidget_2.setWidget(self.dockWidgetContents_3)
        self.verticalLayout_25.addWidget(self.dockWidget_2)
        self.tabWidget.addTab(self.tab, "")
        self.verticalLayout_32.addWidget(self.tabWidget)
        self.dockWidget_9.setWidget(self.dockWidgetContents_16)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_9)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 748, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.menubar.setPalette(palette)
        self.menubar.setStyleSheet("QMenuBar::item:selected{\n"
"  background-color: grey;\n"
"}\n"
"\n"
"\n"
"QMenuBar{\n"
"background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.menubar.setNativeMenuBar(True)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.actionMain_Menu = QtWidgets.QAction(MainWindow)
        self.actionMain_Menu.setObjectName("actionMain_Menu")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionDropBox = QtWidgets.QAction(MainWindow)
        self.actionDropBox.setObjectName("actionDropBox")
        self.actionGoogleDrive = QtWidgets.QAction(MainWindow)
        self.actionGoogleDrive.setObjectName("actionGoogleDrive")
        self.actionOneDrive = QtWidgets.QAction(MainWindow)
        self.actionOneDrive.setObjectName("actionOneDrive")
        self.actionDark = QtWidgets.QAction(MainWindow)
        self.actionDark.setObjectName("actionDark")
        self.actionDark_2 = QtWidgets.QAction(MainWindow)
        self.actionDark_2.setObjectName("actionDark_2")
        self.actionGreen = QtWidgets.QAction(MainWindow)
        self.actionGreen.setObjectName("actionGreen")
        self.actionResult_file = QtWidgets.QAction(MainWindow)
        self.actionResult_file.setObjectName("actionResult_file")
        self.actionNavigate = QtWidgets.QAction(MainWindow)
        self.actionNavigate.setObjectName("actionNavigate")
        self.actionExport_result = QtWidgets.QAction(MainWindow)
        self.actionExport_result.setObjectName("actionExport_result")
        self.actionNavigate_2 = QtWidgets.QAction(MainWindow)
        self.actionNavigate_2.setObjectName("actionNavigate_2")
        self.actionProcess_Videos = QtWidgets.QAction(MainWindow)
        self.actionProcess_Videos.setObjectName("actionProcess_Videos")
        self.actionStoryboard = QtWidgets.QAction(MainWindow)
        self.actionStoryboard.setObjectName("actionStoryboard")
        self.actionData_Analysis = QtWidgets.QAction(MainWindow)
        self.actionData_Analysis.setObjectName("actionData_Analysis")
        self.actionChinese = QtWidgets.QAction(MainWindow)
        self.actionChinese.setObjectName("actionChinese")
        self.actionJapanese = QtWidgets.QAction(MainWindow)
        self.actionJapanese.setObjectName("actionJapanese")
        self.actionArabic = QtWidgets.QAction(MainWindow)
        self.actionArabic.setObjectName("actionArabic")
        self.actionRussian = QtWidgets.QAction(MainWindow)
        self.actionRussian.setObjectName("actionRussian")
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionHebrew = QtWidgets.QAction(MainWindow)
        self.actionHebrew.setObjectName("actionHebrew")
        self.actionBengali = QtWidgets.QAction(MainWindow)
        self.actionBengali.setObjectName("actionBengali")
        self.actionStoryboard_2 = QtWidgets.QAction(MainWindow)
        self.actionStoryboard_2.setObjectName("actionStoryboard_2")
        self.actionProcess_Videos_2 = QtWidgets.QAction(MainWindow)
        self.actionProcess_Videos_2.setObjectName("actionProcess_Videos_2")
        self.actionData_Analysis_2 = QtWidgets.QAction(MainWindow)
        self.actionData_Analysis_2.setObjectName("actionData_Analysis_2")
        self.actionResult = QtWidgets.QAction(MainWindow)
        self.actionResult.setObjectName("actionResult")
        self.actionTop_Frame = QtWidgets.QAction(MainWindow)
        self.actionTop_Frame.setObjectName("actionTop_Frame")
        self.actionBottom_Frame = QtWidgets.QAction(MainWindow)
        self.actionBottom_Frame.setObjectName("actionBottom_Frame")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.establishConnections()
        self.initialSetup()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Editor"))
        self.horizontalScrollBar.setToolTip(_translate("MainWindow", "<html><head/><body><p>Use this slider to scroll media above</p></body></html>"))
        self.dockWidget_9.setToolTip(_translate("MainWindow", "Optimize arena, object and motion detection"))
        self.dockWidget_9.setWindowTitle(_translate("MainWindow", "Toolbox"))
        self.dockWidget_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Test cropping for movie(s)</p></body></html>"))
        self.listWidget_7.setToolTip(_translate("MainWindow", "<html><head/><body><p>Movie list : Auto populated from chosen directory. </p><p>You can also drag and drop files here.</p></body></html>"))
        self.pushButton_19.setToolTip(_translate("MainWindow", "<html><head/><body><p>Apply selected option to crop the image</p></body></html>"))
        self.pushButton_19.setText(_translate("MainWindow", "Submit"))
        self.hiPassFilterLabel_35.setText(_translate("MainWindow", "Brightness"))
        self.hiPassFilterLabel_36.setText(_translate("MainWindow", "Contrast"))
        self.hiPassFilterLabel_31.setText(_translate("MainWindow", "Threshold"))
        #self.pushButton_21.setToolTip(_translate("MainWindow", "<html><head/><body><p>Apply selected action and update result(s)</p></body></html>"))
        #self.pushButton_21.setText(_translate("MainWindow", "Update"))
        self.pushButton_18.setToolTip(_translate("MainWindow", "<html><head/><body><p>Browse to the directory with media file(s)</p></body></html>"))
        self.pushButton_18.setText(_translate("MainWindow", "Browse "))
        self.lineEdit_3.setToolTip(_translate("MainWindow", "<html><head/><body><p>Path of media file(s)</p></body></html>"))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Directory path"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Image Editing Options"))
        self.actionMain_Menu.setText(_translate("MainWindow", "Main Menu"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionDropBox.setText(_translate("MainWindow", "DropBox"))
        self.actionGoogleDrive.setText(_translate("MainWindow", "GoogleDrive"))
        self.actionOneDrive.setText(_translate("MainWindow", "OneDrive"))
        self.actionDark.setText(_translate("MainWindow", "Dark"))
        self.actionDark_2.setText(_translate("MainWindow", "Dark"))
        self.actionGreen.setText(_translate("MainWindow", "Green"))
        self.actionResult_file.setText(_translate("MainWindow", "Result file"))
        self.actionNavigate.setText(_translate("MainWindow", "Navigate"))
        self.actionExport_result.setText(_translate("MainWindow", "Export result"))
        self.actionNavigate_2.setText(_translate("MainWindow", "Navigate"))
        self.actionProcess_Videos.setText(_translate("MainWindow", "Process Videos"))
        self.actionStoryboard.setText(_translate("MainWindow", "Storyboard"))
        self.actionData_Analysis.setText(_translate("MainWindow", "Data Analysis"))
        self.actionChinese.setText(_translate("MainWindow", "Chinese"))
        self.actionJapanese.setText(_translate("MainWindow", "Japanese"))
        self.actionArabic.setText(_translate("MainWindow", "Arabic"))
        self.actionRussian.setText(_translate("MainWindow", "Russian"))
        self.actionEnglish.setText(_translate("MainWindow", "English"))
        self.actionHebrew.setText(_translate("MainWindow", "Hebrew"))
        self.actionBengali.setText(_translate("MainWindow", "Bengali"))
        self.actionStoryboard_2.setText(_translate("MainWindow", "Storyboard"))
        self.actionProcess_Videos_2.setText(_translate("MainWindow", "Process Videos"))
        self.actionData_Analysis_2.setText(_translate("MainWindow", "Data Analysis"))
        self.actionResult.setText(_translate("MainWindow", "Result"))
        self.actionTop_Frame.setText(_translate("MainWindow", "Top Frame"))
        self.actionBottom_Frame.setText(_translate("MainWindow", "Bottom Frame"))

    def initialSetup(self):
        # functions
        #self.enableFieldValidation()
        self.sliderNamesArray = [self.horizontalScrollBar] #,self.horizontalScrollBar_2]
        #self.splitter.setSizes([1, 0])
        #self.timer_id = -1
        self.lineEdit_3.setDisabled(True)
        self.imagePair = [None,None,None,None]
        self.showImage(0,None,None)
        #self.showImage(1,None,None)
        self.currentBBList = None
        self.propertiesDataFrame = None
        self.FinalPropertiesDictionary = {}
        self.CurrentFrame = None
        self.currentVideoFrame = 0
        self.currentImage = None
        self.contrastImage = None
        self.brightImage = None

        self.NewFrameAlert = True


        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(255)

        self.horizontalSlider_2.setMinimum(10)
        self.horizontalSlider_2.setMaximum(100)

        self.horizontalSlider_3.setMinimum(10)
        self.horizontalSlider_3.setMaximum(50)

        #self.loadParametersFromFileAtStart()
        #self.loadColormap()


    def establishConnections(self):
        self.dataAccessObject = dataInputOutputClass()
        self.singleMovieControlleObject = singleMovieController()
        self.pushButton_18.clicked.connect(self.browseToInputFolderByUSerAndShowMovies)
        self.listWidget_7.itemDoubleClicked.connect(self.showIfCropExists)

        self.horizontalSlider.sliderReleased.connect(lambda : self.callSegmentationFunction())
        self.horizontalSlider_2.sliderReleased.connect(lambda : self.editImage(self.singleMovieControlleObject.showOriginalUncropImage()))
        self.horizontalSlider_3.sliderReleased.connect(lambda : self.editImage(self.singleMovieControlleObject.showOriginalUncropImage()))
        #self.pushButton_25.clicked.connect(lambda : self.startAnnotatingMovie(mode = "submit"))

        #self.pushButton_21.clicked.connect(lambda : self.editImage(self.singleMovieControlleObject.showOriginalUncropImage()))
        #self.pushButton_21.clicked.connect(lambda : self.editImage(self.singleMovieControlleObject.showOriginalUncropImage()))
        
        #self.doubleSpinBox_5.setKeyboardTracking(False)
        #self.doubleSpinBox_5.valueChanged.connect(self.rotatedImageShow)
        
        # controller buttons
        #self.horizontalScrollBar.valueChanged.connect(lambda event: self.playCurrentVideo(event,barNum =0))
        #self.horizontalScrollBar_2.valueChanged.connect(lambda event: self.playCurrentVideo(event,barNum= 1))

    ## handles updation of image and metadata related to image
    def showImage(self,frameNum,image,type, frameNo=None):
        self.imagePair[frameNum] = type
        if frameNum ==0:
            frame = self.cleanImage
        elif frameNum == 1:
            #frame = self.threshImage
            pass

        if type in ["actAnnotate"]:
              frame.updateAnnotationDictionary()

        frame.canvas.axes.clear()
        frame.canvas.axes.axis("off")
        if image is not None:
           if type in ["thresh","clean"]:
              frame.canvas.axes.imshow(image, cmap="gray", vmin=0, vmax=255)
           else:
              frame.canvas.axes.imshow(image)

        if type in ["actAnnotate"]:
              frame.applyAnnotationDictionary(frameNo)
        
        frame.canvas.draw()

    def setCurrentFrameForDictionary(self, frame_no):
        self.CurrentFrame = 'frame_no_'+str(frame_no)
        #print(self.CurrentFrame)

    def setFrameNumberForMplWidget(self, figNum, frame_no, countString =""):
        frameAt = str(frame_no) +" "+countString
        if figNum ==0:
            frame = self.cleanImage
        elif figNum == 1:
            #frame = self.threshImage
            pass
        frame.setFrameAtString(frameAt)

    def browseToInputFolderByUSerAndShowMovies(self, headless = None):
        # GETpath to controller
        self.listWidget_7.clear()
    
        if (headless is not None) and (headless != False):
            self.dirName = headless
            if not os.path.isdir(self.dirName):
                return
        else:
            self.dirName = QtWidgets.QFileDialog().getExistingDirectory(
                None, "Select a directory of raw worm movies data (*.mov, *.avi, *.mp4)",options=QtWidgets.QFileDialog.DontUseNativeDialog
            )

        #self.FinalPropertiesDictionary = self.openExistingPickleDump(self.dirName)
            
        try:
            movieNames = self.dataAccessObject.moviesInInputFolderByUser(self.dirName)
            for name in movieNames:
                item = QtWidgets.QListWidgetItem()
                item.setText(QtWidgets.QApplication.translate("Dialog", name, None))
                self.listWidget_7.addItem(item)
            self.listWidget_7.setCurrentItem(self.listWidget_7.item(0))
            self.listWidget_7.item(0).setSelected(True)
            self.lineEdit_3.setText(self.dirName)
            self.lineEdit_3.setToolTip(self.dirName)
        except:
            self.lineEdit_3.setToolTip('Path of media file(s)')
            self.lineEdit_3.setText(None)
            if (headless is None):
                self.throwThisMessage(
                    "Invalid Folder", "Please choose folder with media files"
                ) 

    def showIfCropExists(self):
        
        # if a current movie has been thresholded but we want to revisit their crop 
        def pullUpFirstFrameFromMovie():
                    #print("Inside pullUpFirstFrameFromMovie")
                    self.setCurrentFrameForDictionary(0)
                    #self.setCurrentFrameForDictionary(self.currentVideoFrame)
                    self.singleMovieControlleObject.resetmovieObject()
                    self.cleanImage.disconnectClickListnerFromCurrentImageForCrop()
                    self.singleMovieControlleObject.setMovieName(self.dirName + os.sep + self.listWidget_7.currentItem().text())
                    
                    self.showImage(0,self.singleMovieControlleObject.showOriginalUncropImage(),"reset")

                    self.NewFrameAlert = True
                  
        if self.singleMovieControlleObject.checkIfMovieNameIsCorrect(self.listWidget_7.currentItem().text()):
            try:
                    self.showImage(0,self.singleMovieControlleObject.showManualCropImage(),"manual")

                    self.NewFrameAlert = True
            except:
                pullUpFirstFrameFromMovie()
        else:
                pullUpFirstFrameFromMovie()
        
        self.updateSlider(0)
        self.currentImage = self.singleMovieControlleObject.showOriginalUncropImage()
        print("Inside showIfCropExists")
        print(type(self.currentImage))
        self.brightImage = self.currentImage
        self.contrastImage = self.currentImage

    def updateSlider(self,sliderNum):
        
        self.sliderNamesArray[sliderNum].setValue(0)
        if self.imagePair[sliderNum] in ["crop","thresh","clean","manual","reset","auto","overlay1"]:   
            #print(self.singleMovieControlleObject.getTotalNumberOfFrames())
            self.sliderNamesArray[sliderNum].setMaximum(self.singleMovieControlleObject.getTotalNumberOfFrames()-1)

        elif self.imagePair[sliderNum] in ["live","livethresh"]:
            self.sliderNamesArray[sliderNum].setMaximum(len(range(self.startFrames,self.runTotalFrames,self.skipFrame))-1)

    '''def editImage(self, image):

        if image is None:
            print('Could not open or find the image: ', args.input)
            exit(0)
        ## [basic-linear-transform-load]
        
        ## [basic-linear-transform-output]
        new_image = np.zeros(image.shape, image.dtype)
        ## [basic-linear-transform-output]
        
        ## [basic-linear-transform-parameters]
        #alpha = 1.0 # Simple contrast control
        #beta = 0    # Simple brightness control
        
        # Initialize values
        print('Editing...')
        #print('-------------------------')
        try:
            alpha = float(int(self.horizontalSlider_3.value())/10)
            beta = int(self.horizontalSlider_2.value())
        except ValueError:
            print('Error, not a number')


        print(int(self.horizontalSlider.value()))
        print(alpha)
        print(beta)
        ## [basic-linear-transform-parameters]
        
        # Do the operation new_image(i,j) = alpha*image(i,j) + beta
        # Instead of these 'for' loops we could have used simply:
        # new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
        # but we wanted to show you how to access the pixels :)
        ## [basic-linear-transform-operation]
        
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                for c in range(image.shape[2]):
                    new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)

        # Show Edited Image
        self.showImage(0,new_image,"reset")
        print("Editing Completed!")
        pass'''

    def editImage(self, image):
        brightnessValue = float(self.horizontalSlider_2.value())/10
        contrastValue = float(self.horizontalSlider_3.value())/10

        print(brightnessValue)
        print(contrastValue)

        PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
        
        # Alter Brightness
        brightness = ImageEnhance.Brightness(PIL_image)
        editedImage = brightness.enhance(brightnessValue)

        #Alter Contrast
        contrast = ImageEnhance.Contrast(editedImage)
        editedImage = contrast.enhance(contrastValue)

        # Show Edited Image
        self.showImage(0,editedImage,"reset")

        self.currentImage = editedImage

        print("Inside showIfCropExists")
        print(type(self.currentImage))
        print("Edited Image!")

    def editBrightness(self, image):
        brightnessValue = float(self.horizontalSlider_2.value())/10
        
        PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
        print(brightnessValue)
        im3 = ImageEnhance.Brightness(PIL_image)

        # Show Edited Image
        self.showImage(0,im3.enhance(brightnessValue),"reset")
        self.brightImage = im3.enhance(brightnessValue)
        print("Brightened Image!")

    def editContrast(self, image):
        contrastValue = float(self.horizontalSlider_3.value())/10
        
        PIL_image = Image.fromarray(np.uint8(image)).convert('RGB')
        print(contrastValue)
        im3 = ImageEnhance.Contrast(PIL_image)
        
        # Show Edited Image
        self.showImage(0,im3.enhance(contrastValue),"reset")
        self.contrastImage = im3.enhance(contrastValue)
        print("Contrasted Image!")

    # return an image overlayed with modified objects
    def overlayBBboxOnImage(self, image2, frame_no = 0):
        print("overlayBBboxOnImage "+str(frame_no))
        
        self.propertiesDataFrame = self.singleMovieControlleObject.getPropertiesDataFrameFromImage(
            image2, ([30, 300])
        )

        newImage = self.singleMovieControlleObject.getImageWithBoundingBoxApplied(
            np.array(self.currentImage),
            self.propertiesDataFrame,
        )

        self.showImage(0,newImage,"reset")
        #return newImage


    ## Just directs the flow of the thresh pane
    def callSegmentationFunction(self):
        #print("callSegmentationFunction "+str(self.currentVideoFrame))
        image1, image2, frame_no = self.getCleanedAndThreshedImages(frame_no = 0)
        try:
            self.overlayBBboxOnImage(image2, frame_no = 0)
        except:
            self.throwThisMessage(
                        "Optimization",
                        "Operation failed please check inputs and try again",
                        "warn",
                    )

    def getCleanedAndThreshedImages(self, frame_no = 0):
        if ( False
                    #int(self.lineEdit_16.text()) <= int(self.lineEdit_15.text())
                    #or int(self.illuminationAdjLineEdit_10.text())
                    #<= int(self.hiPassFilterLineEdit_14.text())
                    #or int(self.hiPassFilterLineEdit_13.text())
                    #<= int(self.illuminationAdjLineEdit_9.text())
                ):
                    self.throwThisMessage(
                        "Optimization",
                        "Parameters illconditioned, template may be black",
                        "warn",
                    )
        self.tempArray1 = [
            int(self.horizontalSlider.value()),
            int(255), #self.hiPassFilterLineEdit_13.text()) Always 255,
            int(0), #self.radioButton_32.isChecked()) Always 0,
            int(0), #self.hiPassFilterLineEdit_14.text()) Alway 0,
            int(255), #self.illuminationAdjLineEdit_10.text()) Always 255,
            0,
            0,
        ]
        self.tempArray2 = [
            -50,
            0,
            30,
            300,
            0,
            3,
        ]
        
        image1 = self.singleMovieControlleObject.getCleanedImage(np.array(self.currentImage), self.tempArray1)
        image2 = self.singleMovieControlleObject.getThreshedImage(image1, self.tempArray2)
        
        '''cv2.namedWindow("Image 1", cv2.WINDOW_NORMAL)
        cv2.imshow("Image 1", image1)
        cv2.waitKey(0)
        cv2.namedWindow("Image 2", cv2.WINDOW_NORMAL)
        cv2.imshow("Image 2", self.singleMovieControlleObject.showOriginalUncropImageAtFrame(frame_no))
        cv2.waitKey(0)'''
        
        return image1, image2, frame_no


from mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())