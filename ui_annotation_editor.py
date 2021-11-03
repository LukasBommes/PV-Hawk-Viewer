# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotation_editor.ui'
##
## Created by: Qt User Interface Compiler version 6.2.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QScrollArea, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_AnnotationEditor(object):
    def setupUi(self, AnnotationEditor):
        if not AnnotationEditor.objectName():
            AnnotationEditor.setObjectName(u"AnnotationEditor")
        AnnotationEditor.resize(308, 583)
        self.gridLayout = QGridLayout(AnnotationEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(AnnotationEditor)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 306, 581))
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)


        self.retranslateUi(AnnotationEditor)

        QMetaObject.connectSlotsByName(AnnotationEditor)
    # setupUi

    def retranslateUi(self, AnnotationEditor):
        AnnotationEditor.setWindowTitle(QCoreApplication.translate("AnnotationEditor", u"Annotation Editor", None))
    # retranslateUi

