# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QWidget)

class Ui_Analysis(object):
    def setupUi(self, Analysis):
        if not Analysis.objectName():
            Analysis.setObjectName(u"Analysis")
        Analysis.resize(442, 315)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Analysis.sizePolicy().hasHeightForWidth())
        Analysis.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(Analysis)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.label_2 = QLabel(Analysis)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.progressBar = QProgressBar(Analysis)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout_2.addWidget(self.progressBar, 3, 0, 1, 2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 1, 1, 1)

        self.progressLabel = QLabel(Analysis)
        self.progressLabel.setObjectName(u"progressLabel")

        self.gridLayout_2.addWidget(self.progressLabel, 2, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonCancel = QPushButton(Analysis)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        self.pushButtonCancel.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonCancel)

        self.pushButtonCompute = QPushButton(Analysis)
        self.pushButtonCompute.setObjectName(u"pushButtonCompute")

        self.horizontalLayout.addWidget(self.pushButtonCompute)

        self.pushButtonOk = QPushButton(Analysis)
        self.pushButtonOk.setObjectName(u"pushButtonOk")

        self.horizontalLayout.addWidget(self.pushButtonOk)


        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 1, 1, 1)

        self.tabWidget = QTabWidget(Analysis)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tabSunFilter = QWidget()
        self.tabSunFilter.setObjectName(u"tabSunFilter")
        self.gridLayout = QGridLayout(self.tabSunFilter)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.tabSunFilter)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.spinBoxThresholdTemp = QDoubleSpinBox(self.tabSunFilter)
        self.spinBoxThresholdTemp.setObjectName(u"spinBoxThresholdTemp")

        self.gridLayout.addWidget(self.spinBoxThresholdTemp, 1, 1, 1, 1)

        self.label_5 = QLabel(self.tabSunFilter)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)

        self.spinBoxThresholdLoc = QDoubleSpinBox(self.tabSunFilter)
        self.spinBoxThresholdLoc.setObjectName(u"spinBoxThresholdLoc")

        self.gridLayout.addWidget(self.spinBoxThresholdLoc, 4, 1, 1, 1)

        self.spinBoxThresholdChangepoint = QDoubleSpinBox(self.tabSunFilter)
        self.spinBoxThresholdChangepoint.setObjectName(u"spinBoxThresholdChangepoint")

        self.gridLayout.addWidget(self.spinBoxThresholdChangepoint, 5, 1, 1, 1)

        self.label_6 = QLabel(self.tabSunFilter)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)

        self.spinBoxSegmentLengthThreshold = QDoubleSpinBox(self.tabSunFilter)
        self.spinBoxSegmentLengthThreshold.setObjectName(u"spinBoxSegmentLengthThreshold")
        self.spinBoxSegmentLengthThreshold.setMaximum(1.000000000000000)
        self.spinBoxSegmentLengthThreshold.setSingleStep(0.100000000000000)

        self.gridLayout.addWidget(self.spinBoxSegmentLengthThreshold, 6, 1, 1, 1)

        self.label_7 = QLabel(self.tabSunFilter)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.tabWidget.addTab(self.tabSunFilter, "")
        self.tabModuleTemperatures = QWidget()
        self.tabModuleTemperatures.setObjectName(u"tabModuleTemperatures")
        self.formLayout = QFormLayout(self.tabModuleTemperatures)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.tabModuleTemperatures)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.spinBoxTruncateWidth = QSpinBox(self.tabModuleTemperatures)
        self.spinBoxTruncateWidth.setObjectName(u"spinBoxTruncateWidth")
        self.spinBoxTruncateWidth.setMaximum(100)
        self.spinBoxTruncateWidth.setValue(5)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.spinBoxTruncateWidth)

        self.label_3 = QLabel(self.tabModuleTemperatures)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.spinBoxNeighborRadius = QSpinBox(self.tabModuleTemperatures)
        self.spinBoxNeighborRadius.setObjectName(u"spinBoxNeighborRadius")
        self.spinBoxNeighborRadius.setMinimum(1)
        self.spinBoxNeighborRadius.setMaximum(100)
        self.spinBoxNeighborRadius.setValue(7)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBoxNeighborRadius)

        self.checkBoxIgnoreSunReflections = QCheckBox(self.tabModuleTemperatures)
        self.checkBoxIgnoreSunReflections.setObjectName(u"checkBoxIgnoreSunReflections")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.checkBoxIgnoreSunReflections)

        self.tabWidget.addTab(self.tabModuleTemperatures, "")

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 2)

        self.nameLineEdit = QLineEdit(Analysis)
        self.nameLineEdit.setObjectName(u"nameLineEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.nameLineEdit.sizePolicy().hasHeightForWidth())
        self.nameLineEdit.setSizePolicy(sizePolicy2)
        self.nameLineEdit.setMaxLength(256)

        self.gridLayout_2.addWidget(self.nameLineEdit, 0, 1, 1, 1)


        self.retranslateUi(Analysis)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Analysis)
    # setupUi

    def retranslateUi(self, Analysis):
        Analysis.setWindowTitle(QCoreApplication.translate("Analysis", u"Analysis", None))
        self.label_2.setText(QCoreApplication.translate("Analysis", u"Name", None))
        self.progressLabel.setText("")
        self.pushButtonCancel.setText(QCoreApplication.translate("Analysis", u"Cancel", None))
        self.pushButtonCompute.setText(QCoreApplication.translate("Analysis", u"Compute", None))
        self.pushButtonOk.setText(QCoreApplication.translate("Analysis", u"Ok", None))
        self.label_4.setText(QCoreApplication.translate("Analysis", u"Temperature Threshold (K)", None))
        self.label_5.setText(QCoreApplication.translate("Analysis", u"Location Threshold (px)", None))
        self.label_6.setText(QCoreApplication.translate("Analysis", u"Changepoint Threshold", None))
        self.label_7.setText(QCoreApplication.translate("Analysis", u"Segment Length Threshold", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSunFilter), QCoreApplication.translate("Analysis", u"Sun  Reflection Filter", None))
        self.label.setText(QCoreApplication.translate("Analysis", u"Truncate image borders (percent of image width)", None))
        self.label_3.setText(QCoreApplication.translate("Analysis", u"Local neighborhood radius (meters)", None))
        self.checkBoxIgnoreSunReflections.setText(QCoreApplication.translate("Analysis", u"Ignore images with sun reflections", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabModuleTemperatures), QCoreApplication.translate("Analysis", u"Module Temperatures", None))
        self.nameLineEdit.setPlaceholderText("")
    # retranslateUi

