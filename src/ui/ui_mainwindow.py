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
    QMenuBar, QSizePolicy, QStatusBar, QWidget)

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
        self.actionNew_Defect_Annotation = QAction(MainWindow)
        self.actionNew_Defect_Annotation.setObjectName(u"actionNew_Defect_Annotation")
        self.actionNew_Defect_Annotation.setEnabled(False)
        self.actionSave_Defect_Annotation = QAction(MainWindow)
        self.actionSave_Defect_Annotation.setObjectName(u"actionSave_Defect_Annotation")
        self.actionSave_Defect_Annotation.setEnabled(False)
        self.actionLoad_Defect_Annotation = QAction(MainWindow)
        self.actionLoad_Defect_Annotation.setObjectName(u"actionLoad_Defect_Annotation")
        self.actionLoad_Defect_Annotation.setEnabled(False)
        self.actionNew_Analysis = QAction(MainWindow)
        self.actionNew_Analysis.setObjectName(u"actionNew_Analysis")
        self.actionNew_Analysis.setEnabled(False)
        self.actionAnnotate_Strings = QAction(MainWindow)
        self.actionAnnotate_Strings.setObjectName(u"actionAnnotate_Strings")
        self.actionAnnotate_Strings.setEnabled(False)
        self.actionClose_String_Annotation = QAction(MainWindow)
        self.actionClose_String_Annotation.setObjectName(u"actionClose_String_Annotation")
        self.actionClose_String_Annotation.setEnabled(False)
        self.actionSave_String_Annotation = QAction(MainWindow)
        self.actionSave_String_Annotation.setObjectName(u"actionSave_String_Annotation")
        self.actionSave_String_Annotation.setEnabled(False)
        self.actionDiscard_Defect_Annotation = QAction(MainWindow)
        self.actionDiscard_Defect_Annotation.setObjectName(u"actionDiscard_Defect_Annotation")
        self.actionDiscard_Defect_Annotation.setEnabled(False)
        self.actionDiscard_String_Annotation = QAction(MainWindow)
        self.actionDiscard_String_Annotation.setObjectName(u"actionDiscard_String_Annotation")
        self.actionDiscard_String_Annotation.setEnabled(False)
        self.actionClose_Defect_Annotation = QAction(MainWindow)
        self.actionClose_Defect_Annotation.setObjectName(u"actionClose_Defect_Annotation")
        self.actionClose_Defect_Annotation.setEnabled(False)
        self.actionExport_String_Annotation = QAction(MainWindow)
        self.actionExport_String_Annotation.setObjectName(u"actionExport_String_Annotation")
        self.actionExport_String_Annotation.setEnabled(False)
        self.actionDataset_Settings = QAction(MainWindow)
        self.actionDataset_Settings.setObjectName(u"actionDataset_Settings")
        self.actionDataset_Settings.setEnabled(False)
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
        self.menuAnnotation = QMenu(self.menubar)
        self.menuAnnotation.setObjectName(u"menuAnnotation")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnnotation.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_Dataset)
        self.menuFile.addAction(self.actionDataset_Settings)
        self.menuFile.addAction(self.actionClose_Dataset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuAnalysis.addAction(self.actionNew_Analysis)
        self.menuAnnotation.addAction(self.actionNew_Defect_Annotation)
        self.menuAnnotation.addAction(self.actionLoad_Defect_Annotation)
        self.menuAnnotation.addAction(self.actionSave_Defect_Annotation)
        self.menuAnnotation.addAction(self.actionClose_Defect_Annotation)
        self.menuAnnotation.addSeparator()
        self.menuAnnotation.addAction(self.actionAnnotate_Strings)
        self.menuAnnotation.addAction(self.actionExport_String_Annotation)
        self.menuAnnotation.addAction(self.actionClose_String_Annotation)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"PV Hawk Viewer", None))
        self.actionOpen_Dataset.setText(QCoreApplication.translate("MainWindow", u"Open Dataset...", None))
        self.actionClose_Dataset.setText(QCoreApplication.translate("MainWindow", u"Close Dataset", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionAnnotation_Editor.setText(QCoreApplication.translate("MainWindow", u"Annotation Editor", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionNew_Defect_Annotation.setText(QCoreApplication.translate("MainWindow", u"New Defect Annotation...", None))
        self.actionSave_Defect_Annotation.setText(QCoreApplication.translate("MainWindow", u"Save Defect Annotation", None))
        self.actionLoad_Defect_Annotation.setText(QCoreApplication.translate("MainWindow", u"Load Defect Annotation...", None))
        self.actionNew_Analysis.setText(QCoreApplication.translate("MainWindow", u"New Analysis...", None))
        self.actionAnnotate_Strings.setText(QCoreApplication.translate("MainWindow", u"Annotate Strings...", None))
        self.actionClose_String_Annotation.setText(QCoreApplication.translate("MainWindow", u"Close String Annotation", None))
        self.actionSave_String_Annotation.setText(QCoreApplication.translate("MainWindow", u"Save String Annotation", None))
        self.actionDiscard_Defect_Annotation.setText(QCoreApplication.translate("MainWindow", u"Discard Defect Annotation", None))
        self.actionDiscard_String_Annotation.setText(QCoreApplication.translate("MainWindow", u"Discard String Annotation", None))
        self.actionClose_Defect_Annotation.setText(QCoreApplication.translate("MainWindow", u"Close Defect Annotation", None))
        self.actionExport_String_Annotation.setText(QCoreApplication.translate("MainWindow", u"Export String Annotation...", None))
        self.actionDataset_Settings.setText(QCoreApplication.translate("MainWindow", u"Dataset Settings", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuAnalysis.setTitle(QCoreApplication.translate("MainWindow", u"Analysis", None))
        self.menuAnnotation.setTitle(QCoreApplication.translate("MainWindow", u"Annotation", None))
    # retranslateUi

