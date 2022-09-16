# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'source_frame_rgb.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_SourceFrame(object):
    def setupUi(self, SourceFrame):
        if not SourceFrame.objectName():
            SourceFrame.setObjectName(u"SourceFrame")
        SourceFrame.resize(675, 455)
        self.gridLayout = QGridLayout(SourceFrame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.sourceFrameLabel = QLabel(SourceFrame)
        self.sourceFrameLabel.setObjectName(u"sourceFrameLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sourceFrameLabel.sizePolicy().hasHeightForWidth())
        self.sourceFrameLabel.setSizePolicy(sizePolicy)
        self.sourceFrameLabel.setMinimumSize(QSize(50, 50))
        self.sourceFrameLabel.setScaledContents(False)

        self.gridLayout.addWidget(self.sourceFrameLabel, 0, 0, 1, 1)


        self.retranslateUi(SourceFrame)

        QMetaObject.connectSlotsByName(SourceFrame)
    # setupUi

    def retranslateUi(self, SourceFrame):
        SourceFrame.setWindowTitle(QCoreApplication.translate("SourceFrame", u"Form", None))
        self.sourceFrameLabel.setText("")
    # retranslateUi

