# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'music.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, 
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(703, 639)
        font = QFont()
        font.setBold(False)
        Form.setFont(font)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font1 = QFont()
        font1.setBold(True)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_srch = QPushButton(Form)
        self.btn_srch.setObjectName(u"btn_srch")
        self.btn_srch.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_srch)

        self.btn_nextpg = QPushButton(Form)
        self.btn_nextpg.setObjectName(u"btn_nextpg")
        self.btn_nextpg.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_nextpg)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_clear = QPushButton(Form)
        self.btn_clear.setObjectName(u"btn_clear")
        self.btn_clear.setFont(font1)

        self.horizontalLayout_2.addWidget(self.btn_clear)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u97f3\u4e50\u4e0b\u8f7d\u5668", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8bf7\u8f93\u5165\u8981\u4e0b\u8f7d\u7684\u97f3\u4e50", None))
        self.btn_srch.setText(QCoreApplication.translate("Form", u"\u641c\u7d22", None))
        self.btn_nextpg.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u9875", None))
        self.btn_clear.setText(QCoreApplication.translate("Form", u"\u6e05\u7a7a", None))
    # retranslateUi

