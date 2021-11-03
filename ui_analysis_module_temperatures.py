# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis_module_temperatures.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QSizePolicy, QSpinBox, QWidget)

class Ui_ModuleTemperatures(object):
    def setupUi(self, ModuleTemperatures):
        if not ModuleTemperatures.objectName():
            ModuleTemperatures.setObjectName(u"ModuleTemperatures")
        ModuleTemperatures.resize(431, 189)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ModuleTemperatures.sizePolicy().hasHeightForWidth())
        ModuleTemperatures.setSizePolicy(sizePolicy)
        self.label = QLabel(ModuleTemperatures)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(9, 9, 341, 26))
        self.truncateWidthSpinBox = QSpinBox(ModuleTemperatures)
        self.truncateWidthSpinBox.setObjectName(u"truncateWidthSpinBox")
        self.truncateWidthSpinBox.setGeometry(QRect(360, 9, 61, 26))
        self.truncateWidthSpinBox.setMaximum(100)
        self.truncateWidthSpinBox.setValue(5)
        self.progressBar = QProgressBar(ModuleTemperatures)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(9, 106, 411, 25))
        self.progressBar.setValue(0)
        self.progressLabel = QLabel(ModuleTemperatures)
        self.progressLabel.setObjectName(u"progressLabel")
        self.progressLabel.setGeometry(QRect(9, 83, 87, 17))
        self.label_3 = QLabel(ModuleTemperatures)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(9, 41, 248, 17))
        self.neighborRadiusSpinBox = QSpinBox(ModuleTemperatures)
        self.neighborRadiusSpinBox.setObjectName(u"neighborRadiusSpinBox")
        self.neighborRadiusSpinBox.setGeometry(QRect(360, 40, 61, 26))
        self.neighborRadiusSpinBox.setMinimum(1)
        self.neighborRadiusSpinBox.setMaximum(100)
        self.neighborRadiusSpinBox.setValue(7)
        self.horizontalLayoutWidget = QWidget(ModuleTemperatures)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(170, 150, 254, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButtonCancel = QPushButton(self.horizontalLayoutWidget)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonCompute = QPushButton(self.horizontalLayoutWidget)
        self.pushButtonCompute.setObjectName(u"pushButtonCompute")

        self.horizontalLayout.addWidget(self.pushButtonCompute)

        self.pushButtonOk = QPushButton(self.horizontalLayoutWidget)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.retranslateUi(ModuleTemperatures)

        QMetaObject.connectSlotsByName(ModuleTemperatures)
    # setupUi

    def retranslateUi(self, ModuleTemperatures):
        ModuleTemperatures.setWindowTitle(QCoreApplication.translate("ModuleTemperatures", u"Module Temperatures", None))
        self.label.setText(QCoreApplication.translate("ModuleTemperatures", u"Truncate Image Borders (percent of image width)", None))
        self.progressLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("ModuleTemperatures", u"Local Neighborhood Radius (meters)", None))
        self.pushButtonCancel.setText(QCoreApplication.translate("ModuleTemperatures", u"Cancel", None))
        self.pushButtonCompute.setText(QCoreApplication.translate("ModuleTemperatures", u"Compute", None))
        self.pushButtonOk.setText(QCoreApplication.translate("ModuleTemperatures", u"Ok", None))
    # retranslateUi

