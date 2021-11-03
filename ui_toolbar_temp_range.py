# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolbar_temp_range.ui'
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
    QSpinBox, QWidget)

class Ui_TempRange(object):
    def setupUi(self, TempRange):
        if not TempRange.objectName():
            TempRange.setObjectName(u"TempRange")
        TempRange.resize(252, 26)
        self.horizontalLayout = QHBoxLayout(TempRange)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(TempRange)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)

        self.horizontalLayout.addWidget(self.label_2)

        self.minTempSpinBox = QSpinBox(TempRange)
        self.minTempSpinBox.setObjectName(u"minTempSpinBox")
        self.minTempSpinBox.setMinimum(-100)
        self.minTempSpinBox.setMaximum(200)
        self.minTempSpinBox.setValue(30)

        self.horizontalLayout.addWidget(self.minTempSpinBox)

        self.label_3 = QLabel(TempRange)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.maxTempSpinBox = QSpinBox(TempRange)
        self.maxTempSpinBox.setObjectName(u"maxTempSpinBox")
        self.maxTempSpinBox.setMinimum(-100)
        self.maxTempSpinBox.setMaximum(200)
        self.maxTempSpinBox.setValue(50)

        self.horizontalLayout.addWidget(self.maxTempSpinBox)

        self.label_4 = QLabel(TempRange)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)


        self.retranslateUi(TempRange)

        QMetaObject.connectSlotsByName(TempRange)
    # setupUi

    def retranslateUi(self, TempRange):
        TempRange.setWindowTitle(QCoreApplication.translate("TempRange", u"Form", None))
        self.label_2.setText(QCoreApplication.translate("TempRange", u"Temp Range", None))
        self.label_3.setText(QCoreApplication.translate("TempRange", u"-", None))
        self.label_4.setText(QCoreApplication.translate("TempRange", u"\u00b0C", None))
    # retranslateUi

