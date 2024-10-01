# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDialog,
    QFormLayout, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(614, 191)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(614, 191))
        Dialog.setAutoFillBackground(False)
        Dialog.setSizeGripEnabled(False)
        self.gridLayout_3 = QGridLayout(Dialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 1, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.path_selection = QComboBox(Dialog)
        self.path_selection.setObjectName(u"path_selection")
        self.path_selection.setLayoutDirection(Qt.LeftToRight)

        self.gridLayout_5.addWidget(self.path_selection, 0, 1, 1, 1)

        self.path_label = QLabel(Dialog)
        self.path_label.setObjectName(u"path_label")

        self.gridLayout_5.addWidget(self.path_label, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 2, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.channel_0_label = QLabel(Dialog)
        self.channel_0_label.setObjectName(u"channel_0_label")
        self.channel_0_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.channel_0_label, 0, 0, 1, 1)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFormAlignment(Qt.AlignCenter)
        self.position_0_label = QLabel(Dialog)
        self.position_0_label.setObjectName(u"position_0_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.position_0_label)

        self.position_0 = QSpinBox(Dialog)
        self.position_0.setObjectName(u"position_0")
        self.position_0.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.position_0.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.position_0.setKeyboardTracking(False)
        self.position_0.setMinimum(-1000000000)
        self.position_0.setMaximum(1000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.position_0)


        self.gridLayout_2.addLayout(self.formLayout, 1, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFormAlignment(Qt.AlignCenter)
        self.position_1_label = QLabel(Dialog)
        self.position_1_label.setObjectName(u"position_1_label")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.position_1_label)

        self.position_1 = QSpinBox(Dialog)
        self.position_1.setObjectName(u"position_1")
        self.position_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.position_1.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.position_1.setKeyboardTracking(False)
        self.position_1.setMinimum(-1000000000)
        self.position_1.setMaximum(1000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.position_1)


        self.gridLayout.addLayout(self.formLayout_2, 1, 0, 1, 1)

        self.channel_1_label = QLabel(Dialog)
        self.channel_1_label.setObjectName(u"channel_1_label")
        self.channel_1_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.channel_1_label, 0, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.channel_2_label = QLabel(Dialog)
        self.channel_2_label.setObjectName(u"channel_2_label")
        self.channel_2_label.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.channel_2_label, 0, 0, 1, 1)

        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setFormAlignment(Qt.AlignCenter)
        self.position_2_label = QLabel(Dialog)
        self.position_2_label.setObjectName(u"position_2_label")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.position_2_label)

        self.position_2 = QSpinBox(Dialog)
        self.position_2.setObjectName(u"position_2")
        self.position_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.position_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.position_2.setMinimum(-1000000000)
        self.position_2.setMaximum(1000000000)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.position_2)


        self.gridLayout_4.addLayout(self.formLayout_3, 1, 0, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 4, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.move_button = QPushButton(Dialog)
        self.move_button.setObjectName(u"move_button")

        self.horizontalLayout.addWidget(self.move_button)

        self.abort_button = QPushButton(Dialog)
        self.abort_button.setObjectName(u"abort_button")

        self.horizontalLayout.addWidget(self.abort_button)


        self.gridLayout_3.addLayout(self.horizontalLayout, 3, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.path_selection.setPlaceholderText(QCoreApplication.translate("Dialog", u"No path selected", None))
        self.path_label.setText(QCoreApplication.translate("Dialog", u"Preset Paths", None))
        self.channel_0_label.setText(QCoreApplication.translate("Dialog", u"Channel 0 [X]:", None))
        self.position_0_label.setText(QCoreApplication.translate("Dialog", u"Position [nm]", None))
        self.position_1_label.setText(QCoreApplication.translate("Dialog", u"Position [nm]", None))
        self.channel_1_label.setText(QCoreApplication.translate("Dialog", u"Channel 1 [Y]:", None))
        self.channel_2_label.setText(QCoreApplication.translate("Dialog", u"Channel 2 [Z]:", None))
        self.position_2_label.setText(QCoreApplication.translate("Dialog", u"Position [nm]", None))
        self.move_button.setText(QCoreApplication.translate("Dialog", u"Move", None))
        self.abort_button.setText(QCoreApplication.translate("Dialog", u"Abort", None))
    # retranslateUi

