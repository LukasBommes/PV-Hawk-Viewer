# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'source_frame.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QSpinBox, QWidget)

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

        self.gridLayout.addWidget(self.sourceFrameLabel, 1, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(SourceFrame)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_2)

        self.minTempSpinBox = QSpinBox(SourceFrame)
        self.minTempSpinBox.setObjectName(u"minTempSpinBox")
        self.minTempSpinBox.setMinimum(-100)
        self.minTempSpinBox.setMaximum(200)
        self.minTempSpinBox.setValue(30)

        self.horizontalLayout.addWidget(self.minTempSpinBox)

        self.label_3 = QLabel(SourceFrame)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_3)

        self.maxTempSpinBox = QSpinBox(SourceFrame)
        self.maxTempSpinBox.setObjectName(u"maxTempSpinBox")
        self.maxTempSpinBox.setMinimum(-100)
        self.maxTempSpinBox.setMaximum(200)
        self.maxTempSpinBox.setValue(50)

        self.horizontalLayout.addWidget(self.maxTempSpinBox)

        self.label_4 = QLabel(SourceFrame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_4)

        self.line = QFrame(SourceFrame)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.label_5 = QLabel(SourceFrame)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.label_5)

        self.colormapComboBox = QComboBox(SourceFrame)
        self.colormapComboBox.setObjectName(u"colormapComboBox")

        self.horizontalLayout.addWidget(self.colormapComboBox)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.retranslateUi(SourceFrame)

        QMetaObject.connectSlotsByName(SourceFrame)
    # setupUi

    def retranslateUi(self, SourceFrame):
        SourceFrame.setWindowTitle(QCoreApplication.translate("SourceFrame", u"Form", None))
        self.sourceFrameLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("SourceFrame", u"Temp Range", None))
        self.label_3.setText(QCoreApplication.translate("SourceFrame", u"-", None))
        self.label_4.setText(QCoreApplication.translate("SourceFrame", u"\u00b0C", None))
        self.label_5.setText(QCoreApplication.translate("SourceFrame", u"Colormap", None))
    # retranslateUi

