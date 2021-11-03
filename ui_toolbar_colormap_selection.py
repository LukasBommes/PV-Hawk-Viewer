# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toolbar_colormap_selection.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QWidget)

class Ui_ColormapSelection(object):
    def setupUi(self, ColormapSelection):
        if not ColormapSelection.objectName():
            ColormapSelection.setObjectName(u"ColormapSelection")
        ColormapSelection.resize(159, 25)
        self.horizontalLayout = QHBoxLayout(ColormapSelection)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(ColormapSelection)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.comboBox = QComboBox(ColormapSelection)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout.addWidget(self.comboBox)


        self.retranslateUi(ColormapSelection)

        QMetaObject.connectSlotsByName(ColormapSelection)
    # setupUi

    def retranslateUi(self, ColormapSelection):
        ColormapSelection.setWindowTitle(QCoreApplication.translate("ColormapSelection", u"Form", None))
        self.label.setText(QCoreApplication.translate("ColormapSelection", u"Colormap", None))
    # retranslateUi

