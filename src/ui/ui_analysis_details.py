# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis_details.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QWidget)

class Ui_AnalysisDetails(object):
    def setupUi(self, AnalysisDetails):
        if not AnalysisDetails.objectName():
            AnalysisDetails.setObjectName(u"AnalysisDetails")
        AnalysisDetails.resize(625, 336)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AnalysisDetails.sizePolicy().hasHeightForWidth())
        AnalysisDetails.setSizePolicy(sizePolicy)
        self.formLayout = QFormLayout(AnalysisDetails)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(AnalysisDetails)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEditAnalysisType = QLineEdit(AnalysisDetails)
        self.lineEditAnalysisType.setObjectName(u"lineEditAnalysisType")
        self.lineEditAnalysisType.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEditAnalysisType)

        self.label_2 = QLabel(AnalysisDetails)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEditTimestamp = QLineEdit(AnalysisDetails)
        self.lineEditTimestamp.setObjectName(u"lineEditTimestamp")
        self.lineEditTimestamp.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEditTimestamp)

        self.label_3 = QLabel(AnalysisDetails)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEditDatasetPath = QLineEdit(AnalysisDetails)
        self.lineEditDatasetPath.setObjectName(u"lineEditDatasetPath")
        self.lineEditDatasetPath.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEditDatasetPath)

        self.label_4 = QLabel(AnalysisDetails)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.listWidgetHyperparameters = QListWidget(AnalysisDetails)
        self.listWidgetHyperparameters.setObjectName(u"listWidgetHyperparameters")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.listWidgetHyperparameters)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButtonClose = QPushButton(AnalysisDetails)
        self.pushButtonClose.setObjectName(u"pushButtonClose")

        self.horizontalLayout.addWidget(self.pushButtonClose)


        self.formLayout.setLayout(4, QFormLayout.FieldRole, self.horizontalLayout)


        self.retranslateUi(AnalysisDetails)

        QMetaObject.connectSlotsByName(AnalysisDetails)
    # setupUi

    def retranslateUi(self, AnalysisDetails):
        AnalysisDetails.setWindowTitle(QCoreApplication.translate("AnalysisDetails", u"Analysis Details", None))
        self.label.setText(QCoreApplication.translate("AnalysisDetails", u"Analysis Type:", None))
        self.label_2.setText(QCoreApplication.translate("AnalysisDetails", u"Timestamp:", None))
        self.label_3.setText(QCoreApplication.translate("AnalysisDetails", u"Dataset Path:", None))
        self.label_4.setText(QCoreApplication.translate("AnalysisDetails", u"Hyperparameters:", None))
        self.pushButtonClose.setText(QCoreApplication.translate("AnalysisDetails", u"Close", None))
    # retranslateUi

