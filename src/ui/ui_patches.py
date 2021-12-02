# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'patches.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QScrollArea, QSizePolicy,
    QWidget)

class Ui_Patches(object):
    def setupUi(self, Patches):
        if not Patches.objectName():
            Patches.setObjectName(u"Patches")
        Patches.resize(614, 370)
        self.horizontalLayout = QHBoxLayout(Patches)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.scrollArea = QScrollArea(Patches)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 594, 350))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)


        self.retranslateUi(Patches)

        QMetaObject.connectSlotsByName(Patches)
    # setupUi

    def retranslateUi(self, Patches):
        Patches.setWindowTitle(QCoreApplication.translate("Patches", u"Patches", None))
    # retranslateUi

