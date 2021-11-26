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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_StringEditor(object):
    def setupUi(self, StringEditor):
        if not StringEditor.objectName():
            StringEditor.setObjectName(u"StringEditor")
        StringEditor.resize(426, 370)
        self.gridLayout_2 = QGridLayout(StringEditor)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButtonNewString = QPushButton(StringEditor)
        self.pushButtonNewString.setObjectName(u"pushButtonNewString")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonNewString.sizePolicy().hasHeightForWidth())
        self.pushButtonNewString.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonNewString)

        self.pushButtonDeleteString = QPushButton(StringEditor)
        self.pushButtonDeleteString.setObjectName(u"pushButtonDeleteString")
        sizePolicy.setHeightForWidth(self.pushButtonDeleteString.sizePolicy().hasHeightForWidth())
        self.pushButtonDeleteString.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.pushButtonDeleteString)


        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.groupBox = QGroupBox(StringEditor)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButtonStartDrawing = QPushButton(self.groupBox)
        self.pushButtonStartDrawing.setObjectName(u"pushButtonStartDrawing")
        sizePolicy.setHeightForWidth(self.pushButtonStartDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonStartDrawing.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonStartDrawing, 0, 0, 1, 1)

        self.pushButtonEndDrawing = QPushButton(self.groupBox)
        self.pushButtonEndDrawing.setObjectName(u"pushButtonEndDrawing")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonEndDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonEndDrawing.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pushButtonEndDrawing, 0, 1, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.lineEditTrackerID = QLineEdit(self.groupBox)
        self.lineEditTrackerID.setObjectName(u"lineEditTrackerID")
        sizePolicy2.setHeightForWidth(self.lineEditTrackerID.sizePolicy().hasHeightForWidth())
        self.lineEditTrackerID.setSizePolicy(sizePolicy2)
        self.lineEditTrackerID.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.lineEditTrackerID, 1, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.lineEditArrayID = QLineEdit(self.groupBox)
        self.lineEditArrayID.setObjectName(u"lineEditArrayID")
        sizePolicy.setHeightForWidth(self.lineEditArrayID.sizePolicy().hasHeightForWidth())
        self.lineEditArrayID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditArrayID, 2, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.lineEditInverterID = QLineEdit(self.groupBox)
        self.lineEditInverterID.setObjectName(u"lineEditInverterID")
        sizePolicy.setHeightForWidth(self.lineEditInverterID.sizePolicy().hasHeightForWidth())
        self.lineEditInverterID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditInverterID, 3, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)

        self.lineEditStringID = QLineEdit(self.groupBox)
        self.lineEditStringID.setObjectName(u"lineEditStringID")
        sizePolicy.setHeightForWidth(self.lineEditStringID.sizePolicy().hasHeightForWidth())
        self.lineEditStringID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditStringID, 4, 1, 1, 1)

        self.pushButtonCancelString = QPushButton(self.groupBox)
        self.pushButtonCancelString.setObjectName(u"pushButtonCancelString")
        sizePolicy.setHeightForWidth(self.pushButtonCancelString.sizePolicy().hasHeightForWidth())
        self.pushButtonCancelString.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.pushButtonCancelString, 5, 0, 1, 1)

        self.pushButtonConfirmString = QPushButton(self.groupBox)
        self.pushButtonConfirmString.setObjectName(u"pushButtonConfirmString")
        sizePolicy2.setHeightForWidth(self.pushButtonConfirmString.sizePolicy().hasHeightForWidth())
        self.pushButtonConfirmString.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pushButtonConfirmString, 5, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)


        self.retranslateUi(StringEditor)

        QMetaObject.connectSlotsByName(StringEditor)
    # setupUi

    def retranslateUi(self, StringEditor):
        StringEditor.setWindowTitle(QCoreApplication.translate("StringEditor", u"Form", None))
        self.pushButtonNewString.setText(QCoreApplication.translate("StringEditor", u"New String...", None))
        self.pushButtonDeleteString.setText(QCoreApplication.translate("StringEditor", u"Delete String", None))
        self.groupBox.setTitle(QCoreApplication.translate("StringEditor", u"New String", None))
        self.pushButtonStartDrawing.setText(QCoreApplication.translate("StringEditor", u"Start Drawing", None))
        self.pushButtonEndDrawing.setText(QCoreApplication.translate("StringEditor", u"End Drawing", None))
        self.label.setText(QCoreApplication.translate("StringEditor", u"Tracker ID", None))
        self.label_2.setText(QCoreApplication.translate("StringEditor", u"Array ID", None))
        self.label_4.setText(QCoreApplication.translate("StringEditor", u"Inverter ID", None))
        self.label_3.setText(QCoreApplication.translate("StringEditor", u"String ID", None))
        self.pushButtonCancelString.setText(QCoreApplication.translate("StringEditor", u"Cancel String", None))
        self.pushButtonConfirmString.setText(QCoreApplication.translate("StringEditor", u"Confirm String", None))
    # retranslateUi

