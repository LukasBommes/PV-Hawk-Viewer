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
        StringEditor.resize(446, 333)
        self.gridLayout_2 = QGridLayout(StringEditor)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 6)
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

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 1, 1, 1, 1)

        self.groupBox = QGroupBox(StringEditor)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_3, 8, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButtonStartDrawing = QPushButton(self.groupBox)
        self.pushButtonStartDrawing.setObjectName(u"pushButtonStartDrawing")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButtonStartDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonStartDrawing.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.pushButtonStartDrawing)

        self.pushButtonPauseDrawing = QPushButton(self.groupBox)
        self.pushButtonPauseDrawing.setObjectName(u"pushButtonPauseDrawing")
        sizePolicy2.setHeightForWidth(self.pushButtonPauseDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonPauseDrawing.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.pushButtonPauseDrawing)

        self.pushButtonEndDrawing = QPushButton(self.groupBox)
        self.pushButtonEndDrawing.setObjectName(u"pushButtonEndDrawing")
        sizePolicy2.setHeightForWidth(self.pushButtonEndDrawing.sizePolicy().hasHeightForWidth())
        self.pushButtonEndDrawing.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.pushButtonEndDrawing)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy1.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.lineEditStringID = QLineEdit(self.groupBox)
        self.lineEditStringID.setObjectName(u"lineEditStringID")
        sizePolicy.setHeightForWidth(self.lineEditStringID.sizePolicy().hasHeightForWidth())
        self.lineEditStringID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditStringID, 8, 1, 1, 1)

        self.lineEditInverterID = QLineEdit(self.groupBox)
        self.lineEditInverterID.setObjectName(u"lineEditInverterID")
        sizePolicy.setHeightForWidth(self.lineEditInverterID.sizePolicy().hasHeightForWidth())
        self.lineEditInverterID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditInverterID, 1, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.pushButtonCancelString = QPushButton(self.groupBox)
        self.pushButtonCancelString.setObjectName(u"pushButtonCancelString")
        sizePolicy.setHeightForWidth(self.pushButtonCancelString.sizePolicy().hasHeightForWidth())
        self.pushButtonCancelString.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButtonCancelString)

        self.pushButtonConfirmString = QPushButton(self.groupBox)
        self.pushButtonConfirmString.setObjectName(u"pushButtonConfirmString")
        sizePolicy.setHeightForWidth(self.pushButtonConfirmString.sizePolicy().hasHeightForWidth())
        self.pushButtonConfirmString.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.pushButtonConfirmString)


        self.gridLayout.addLayout(self.horizontalLayout_5, 9, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)

        self.lineEditArrayID = QLineEdit(self.groupBox)
        self.lineEditArrayID.setObjectName(u"lineEditArrayID")
        sizePolicy.setHeightForWidth(self.lineEditArrayID.sizePolicy().hasHeightForWidth())
        self.lineEditArrayID.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lineEditArrayID, 5, 1, 1, 1)

        self.lineEditTrackerID = QLineEdit(self.groupBox)
        self.lineEditTrackerID.setObjectName(u"lineEditTrackerID")
        sizePolicy.setHeightForWidth(self.lineEditTrackerID.sizePolicy().hasHeightForWidth())
        self.lineEditTrackerID.setSizePolicy(sizePolicy)
        self.lineEditTrackerID.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.lineEditTrackerID, 4, 1, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)


        self.retranslateUi(StringEditor)

        QMetaObject.connectSlotsByName(StringEditor)
    # setupUi

    def retranslateUi(self, StringEditor):
        StringEditor.setWindowTitle(QCoreApplication.translate("StringEditor", u"Form", None))
        self.pushButtonNewString.setText(QCoreApplication.translate("StringEditor", u"New String...", None))
        self.pushButtonDeleteString.setText(QCoreApplication.translate("StringEditor", u"Delete String", None))
        self.groupBox.setTitle(QCoreApplication.translate("StringEditor", u"New String", None))
        self.label_3.setText(QCoreApplication.translate("StringEditor", u"String ID", None))
        self.label_5.setText(QCoreApplication.translate("StringEditor", u"Draw String", None))
        self.pushButtonStartDrawing.setText(QCoreApplication.translate("StringEditor", u"Start", None))
        self.pushButtonPauseDrawing.setText(QCoreApplication.translate("StringEditor", u"Pause", None))
        self.pushButtonEndDrawing.setText(QCoreApplication.translate("StringEditor", u"End", None))
        self.label_4.setText(QCoreApplication.translate("StringEditor", u"Inverter ID", None))
        self.pushButtonCancelString.setText(QCoreApplication.translate("StringEditor", u"Cancel String", None))
        self.pushButtonConfirmString.setText(QCoreApplication.translate("StringEditor", u"Confirm String", None))
        self.label_2.setText(QCoreApplication.translate("StringEditor", u"Array ID", None))
        self.label.setText(QCoreApplication.translate("StringEditor", u"Tracker ID", None))
    # retranslateUi

