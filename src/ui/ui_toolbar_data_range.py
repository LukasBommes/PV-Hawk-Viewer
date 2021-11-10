# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolbar_data_range.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QSpinBox, QWidget)

class Ui_DataRange(object):
    def setupUi(self, DataRange):
        if not DataRange.objectName():
            DataRange.setObjectName(u"DataRange")
        DataRange.resize(258, 26)
        self.horizontalLayout = QHBoxLayout(DataRange)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(DataRange)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.horizontalLayout.addWidget(self.label_2)

        self.minValSpinBox = QSpinBox(DataRange)
        self.minValSpinBox.setObjectName(u"minValSpinBox")
        self.minValSpinBox.setMinimum(-100)
        self.minValSpinBox.setMaximum(200)
        self.minValSpinBox.setValue(30)

        self.horizontalLayout.addWidget(self.minValSpinBox)

        self.label_3 = QLabel(DataRange)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.maxValSpinBox = QSpinBox(DataRange)
        self.maxValSpinBox.setObjectName(u"maxValSpinBox")
        self.maxValSpinBox.setMinimum(-100)
        self.maxValSpinBox.setMaximum(200)
        self.maxValSpinBox.setValue(50)

        self.horizontalLayout.addWidget(self.maxValSpinBox)

        self.dataUnitLabel = QLabel(DataRange)
        self.dataUnitLabel.setObjectName(u"dataUnitLabel")

        self.horizontalLayout.addWidget(self.dataUnitLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.retranslateUi(DataRange)

        QMetaObject.connectSlotsByName(DataRange)
    # setupUi

    def retranslateUi(self, DataRange):
        DataRange.setWindowTitle(QCoreApplication.translate("DataRange", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("DataRange", u"Value Range", None))
        self.label_3.setText(QCoreApplication.translate("DataRange", u"-", None))
        self.dataUnitLabel.setText(QCoreApplication.translate("DataRange", u"\u00b0C", None))
    # retranslateUi

