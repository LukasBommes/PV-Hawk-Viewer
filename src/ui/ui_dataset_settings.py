# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dataset_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_DatasetSettings(object):
    def setupUi(self, DatasetSettings):
        if not DatasetSettings.objectName():
            DatasetSettings.setObjectName(u"DatasetSettings")
        DatasetSettings.resize(311, 171)
        self.gridLayout = QGridLayout(DatasetSettings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(DatasetSettings)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 2)

        self.label_2 = QLabel(DatasetSettings)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.gainSpinBox = QDoubleSpinBox(DatasetSettings)
        self.gainSpinBox.setObjectName(u"gainSpinBox")
        self.gainSpinBox.setDecimals(4)
        self.gainSpinBox.setMinimum(-100.000000000000000)
        self.gainSpinBox.setMaximum(100.000000000000000)
        self.gainSpinBox.setSingleStep(0.010000000000000)
        self.gainSpinBox.setValue(0.040000000000000)

        self.gridLayout.addWidget(self.gainSpinBox, 1, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonCancel = QPushButton(DatasetSettings)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonSave = QPushButton(DatasetSettings)
        self.pushButtonSave.setObjectName(u"pushButtonSave")

        self.horizontalLayout.addWidget(self.pushButtonSave)


        self.gridLayout.addLayout(self.horizontalLayout, 4, 1, 1, 1)

        self.offsetSpinBox = QDoubleSpinBox(DatasetSettings)
        self.offsetSpinBox.setObjectName(u"offsetSpinBox")
        self.offsetSpinBox.setMinimum(-1000.000000000000000)
        self.offsetSpinBox.setMaximum(1000.000000000000000)
        self.offsetSpinBox.setValue(-273.149999999999977)

        self.gridLayout.addWidget(self.offsetSpinBox, 2, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 2, 1, 1)

        self.label = QLabel(DatasetSettings)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_2, 3, 1, 1, 1)


        self.retranslateUi(DatasetSettings)

        QMetaObject.connectSlotsByName(DatasetSettings)
    # setupUi

    def retranslateUi(self, DatasetSettings):
        DatasetSettings.setWindowTitle(QCoreApplication.translate("DatasetSettings", u"Dataset Settings", None))
        self.label_3.setText(QCoreApplication.translate("DatasetSettings", u"<html><head/><body><p>Conversion of raw image values to Celsius:<br/>I<span style=\" vertical-align:sub;\">celsius</span> = I<span style=\" vertical-align:sub;\">raw</span> * gain + offset</p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("DatasetSettings", u"Offset", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("DatasetSettings", u"Cancel", None))
        self.pushButtonSave.setText(QCoreApplication.translate("DatasetSettings", u"Save", None))
        self.label.setText(QCoreApplication.translate("DatasetSettings", u"Gain", None))
    # retranslateUi

