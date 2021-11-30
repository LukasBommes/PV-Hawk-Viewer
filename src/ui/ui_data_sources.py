# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_sources.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_DataSources(object):
    def setupUi(self, DataSources):
        if not DataSources.objectName():
            DataSources.setObjectName(u"DataSources")
        DataSources.resize(723, 599)
        self.gridLayout = QGridLayout(DataSources)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonNewAnalysis = QPushButton(DataSources)
        self.pushButtonNewAnalysis.setObjectName(u"pushButtonNewAnalysis")
        self.pushButtonNewAnalysis.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonNewAnalysis)

        self.pushButtonDetails = QPushButton(DataSources)
        self.pushButtonDetails.setObjectName(u"pushButtonDetails")
        self.pushButtonDetails.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonDetails)

        self.pushButtonDelete = QPushButton(DataSources)
        self.pushButtonDelete.setObjectName(u"pushButtonDelete")
        self.pushButtonDelete.setEnabled(False)

        self.horizontalLayout.addWidget(self.pushButtonDelete)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.dataSourcesListWidget = QListWidget(DataSources)
        self.dataSourcesListWidget.setObjectName(u"dataSourcesListWidget")

        self.gridLayout.addWidget(self.dataSourcesListWidget, 0, 0, 1, 1)


        self.retranslateUi(DataSources)

        QMetaObject.connectSlotsByName(DataSources)
    # setupUi

    def retranslateUi(self, DataSources):
        DataSources.setWindowTitle(QCoreApplication.translate("DataSources", u"Data Sources", None))
        self.pushButtonNewAnalysis.setText(QCoreApplication.translate("DataSources", u"New Analysis...", None))
        self.pushButtonDetails.setText(QCoreApplication.translate("DataSources", u"Details", None))
        self.pushButtonDelete.setText(QCoreApplication.translate("DataSources", u"Delete", None))
    # retranslateUi

