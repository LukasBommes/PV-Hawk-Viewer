# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(800, 600)
        self.actionOpen_Dataset = QAction(MainWindow)
        self.actionOpen_Dataset.setObjectName(u"actionOpen_Dataset")
        self.actionClose_Dataset = QAction(MainWindow)
        self.actionClose_Dataset.setObjectName(u"actionClose_Dataset")
        self.actionClose_Dataset.setEnabled(False)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAnnotation_Editor = QAction(MainWindow)
        self.actionAnnotation_Editor.setObjectName(u"actionAnnotation_Editor")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionNew_Annotation = QAction(MainWindow)
        self.actionNew_Annotation.setObjectName(u"actionNew_Annotation")
        self.actionSave_Annotation = QAction(MainWindow)
        self.actionSave_Annotation.setObjectName(u"actionSave_Annotation")
        self.actionSave_Annotation.setEnabled(False)
        self.actionLoad_Annotation = QAction(MainWindow)
        self.actionLoad_Annotation.setObjectName(u"actionLoad_Annotation")
        self.actionModule_Temperatures = QAction(MainWindow)
        self.actionModule_Temperatures.setObjectName(u"actionModule_Temperatures")
        self.actionModule_Temperatures.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWebEngineView(self.centralwidget)
        self.widget.setObjectName(u"widget")

        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuAnalysis = QMenu(self.menubar)
        self.menuAnalysis.setObjectName(u"menuAnalysis")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Dataset)
        self.menuFile.addAction(self.actionClose_Dataset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionNew_Annotation)
        self.menuFile.addAction(self.actionLoad_Annotation)
        self.menuFile.addAction(self.actionSave_Annotation)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuFile.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuAnalysis.addAction(self.actionModule_Temperatures)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PV Defect Mapper", None))
        self.actionOpen_Dataset.setText(QCoreApplication.translate("MainWindow", u"Open Dataset...", None))
        self.actionClose_Dataset.setText(QCoreApplication.translate("MainWindow", u"Close Dataset", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionAnnotation_Editor.setText(QCoreApplication.translate("MainWindow", u"Annotation Editor", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionNew_Annotation.setText(QCoreApplication.translate("MainWindow", u"New Annotation...", None))
        self.actionSave_Annotation.setText(QCoreApplication.translate("MainWindow", u"Save Annotation", None))
        self.actionLoad_Annotation.setText(QCoreApplication.translate("MainWindow", u"Load Annotation...", None))
        self.actionModule_Temperatures.setText(QCoreApplication.translate("MainWindow", u"Module Temperatures", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuAnalysis.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
    # retranslateUi

