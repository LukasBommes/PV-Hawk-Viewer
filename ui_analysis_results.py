# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysis_results.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QWidget)

class Ui_AnalysisResults(object):
    def setupUi(self, AnalysisResults):
        if not AnalysisResults.objectName():
            AnalysisResults.setObjectName(u"AnalysisResults")
        AnalysisResults.resize(723, 599)
        self.gridLayout = QGridLayout(AnalysisResults)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(AnalysisResults)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_3 = QPushButton(AnalysisResults)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.analysisResultsTableView = QTableView(AnalysisResults)
        self.analysisResultsTableView.setObjectName(u"analysisResultsTableView")

        self.gridLayout.addWidget(self.analysisResultsTableView, 0, 0, 1, 1)


        self.retranslateUi(AnalysisResults)

        QMetaObject.connectSlotsByName(AnalysisResults)
    # setupUi

    def retranslateUi(self, AnalysisResults):
        AnalysisResults.setWindowTitle(QCoreApplication.translate("AnalysisResults", u"Analysis Results", None))
        self.pushButton.setText(QCoreApplication.translate("AnalysisResults", u"New Analysis...", None))
        self.pushButton_3.setText(QCoreApplication.translate("AnalysisResults", u"Delete", None))
    # retranslateUi

