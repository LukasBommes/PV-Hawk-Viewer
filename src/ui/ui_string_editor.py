# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'string_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QWidget)

class Ui_StringEditor(object):
    def setupUi(self, StringEditor):
        if not StringEditor.objectName():
            StringEditor.setObjectName(u"StringEditor")
        StringEditor.resize(487, 351)
        self.gridLayout = QGridLayout(StringEditor)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonConfirmString = QPushButton(StringEditor)
        self.pushButtonConfirmString.setObjectName(u"pushButtonConfirmString")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonConfirmString.sizePolicy().hasHeightForWidth())
        self.pushButtonConfirmString.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonConfirmString, 6, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 7, 1, 1, 1)

        self.pushButtonNewString = QPushButton(StringEditor)
        self.pushButtonNewString.setObjectName(u"pushButtonNewString")
        sizePolicy.setHeightForWidth(self.pushButtonNewString.sizePolicy().hasHeightForWidth())
        self.pushButtonNewString.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonNewString, 0, 0, 1, 1)

        self.pushButtonCancelString = QPushButton(StringEditor)
        self.pushButtonCancelString.setObjectName(u"pushButtonCancelString")
        sizePolicy.setHeightForWidth(self.pushButtonCancelString.sizePolicy().hasHeightForWidth())
        self.pushButtonCancelString.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonCancelString, 6, 0, 1, 1)

        self.label = QLabel(StringEditor)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.pushButtonStartDrawing = QPushButton(StringEditor)
        self.pushButtonStartDrawing.setObjectName(u"pushButtonStartDrawing")
        sizePolicy.setHeightForWidth(self.pushButtonStartDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonStartDrawing.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonStartDrawing, 1, 0, 1, 1)

        self.lineEditTrackerID = QLineEdit(StringEditor)
        self.lineEditTrackerID.setObjectName(u"lineEditTrackerID")
        sizePolicy.setHeightForWidth(self.lineEditTrackerID.sizePolicy().hasHeightForWidth())
        self.lineEditTrackerID.setSizePolicy(sizePolicy)
        self.lineEditTrackerID.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.lineEditTrackerID, 2, 1, 1, 1)

        self.pushButtonEndDrawing = QPushButton(StringEditor)
        self.pushButtonEndDrawing.setObjectName(u"pushButtonEndDrawing")
        sizePolicy.setHeightForWidth(self.pushButtonEndDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonEndDrawing.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonEndDrawing, 1, 1, 1, 2)

        self.lineEditStringID = QLineEdit(StringEditor)
        self.lineEditStringID.setObjectName(u"lineEditStringID")
        sizePolicy.setHeightForWidth(self.lineEditStringID.sizePolicy().hasHeightForWidth())
        self.lineEditStringID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditStringID, 5, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 4, 2, 1, 1)

        self.label_2 = QLabel(StringEditor)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)

        self.lineEditArrayID = QLineEdit(StringEditor)
        self.lineEditArrayID.setObjectName(u"lineEditArrayID")
        sizePolicy.setHeightForWidth(self.lineEditArrayID.sizePolicy().hasHeightForWidth())
        self.lineEditArrayID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditArrayID, 3, 1, 1, 1)

        self.label_3 = QLabel(StringEditor)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.lineEditInverterID = QLineEdit(StringEditor)
        self.lineEditInverterID.setObjectName(u"lineEditInverterID")
        sizePolicy.setHeightForWidth(self.lineEditInverterID.sizePolicy().hasHeightForWidth())
        self.lineEditInverterID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditInverterID, 4, 1, 1, 1)

        self.label_4 = QLabel(StringEditor)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)


        self.retranslateUi(StringEditor)

        QMetaObject.connectSlotsByName(StringEditor)
    # setupUi

    def retranslateUi(self, StringEditor):
        StringEditor.setWindowTitle(QCoreApplication.translate("StringEditor", u"Form", None))
        self.pushButtonConfirmString.setText(QCoreApplication.translate("StringEditor", u"Confirm String", None))
        self.pushButtonNewString.setText(QCoreApplication.translate("StringEditor", u"New String...", None))
        self.pushButtonCancelString.setText(QCoreApplication.translate("StringEditor", u"Cancel String", None))
        self.label.setText(QCoreApplication.translate("StringEditor", u"Tracker ID", None))
        self.pushButtonStartDrawing.setText(QCoreApplication.translate("StringEditor", u"Start Drawing", None))
        self.pushButtonEndDrawing.setText(QCoreApplication.translate("StringEditor", u"End Drawing", None))
        self.label_2.setText(QCoreApplication.translate("StringEditor", u"Array ID", None))
        self.label_3.setText(QCoreApplication.translate("StringEditor", u"String ID", None))
        self.label_4.setText(QCoreApplication.translate("StringEditor", u"Inverter ID", None))
    # retranslateUi

