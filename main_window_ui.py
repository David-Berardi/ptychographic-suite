# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowxocdrj.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFormLayout,
    QGridLayout, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStatusBar, QTabWidget,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(805, 512)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.actuator_properties_tab = QWidget()
        self.actuator_properties_tab.setObjectName(u"actuator_properties_tab")
        self.verticalLayout = QVBoxLayout(self.actuator_properties_tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.top_layout = QHBoxLayout()
        self.top_layout.setObjectName(u"top_layout")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.top_layout.addItem(self.horizontalSpacer_6)

        self.devices_layout = QHBoxLayout()
        self.devices_layout.setObjectName(u"devices_layout")
        self.devices_label = QLabel(self.actuator_properties_tab)
        self.devices_label.setObjectName(u"devices_label")

        self.devices_layout.addWidget(self.devices_label)

        self.devices = QComboBox(self.actuator_properties_tab)
        self.devices.setObjectName(u"devices")
        self.devices.setEnabled(True)

        self.devices_layout.addWidget(self.devices)


        self.top_layout.addLayout(self.devices_layout)

        self.refresh_layout = QHBoxLayout()
        self.refresh_layout.setObjectName(u"refresh_layout")
        self.refresh_button = QPushButton(self.actuator_properties_tab)
        self.refresh_button.setObjectName(u"refresh_button")
        self.refresh_button.setCheckable(False)

        self.refresh_layout.addWidget(self.refresh_button)

        self.error_label = QLabel(self.actuator_properties_tab)
        self.error_label.setObjectName(u"error_label")

        self.refresh_layout.addWidget(self.error_label)


        self.top_layout.addLayout(self.refresh_layout)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.top_layout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.top_layout)

        self.label_9 = QLabel(self.actuator_properties_tab)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout.addWidget(self.label_9)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_7 = QLabel(self.actuator_properties_tab)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 0, 2, 1, 1)

        self.move_button = QPushButton(self.actuator_properties_tab)
        self.move_button.setObjectName(u"move_button")
        self.move_button.setEnabled(False)

        self.gridLayout_2.addWidget(self.move_button, 4, 5, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.minus_1_button = QPushButton(self.actuator_properties_tab)
        self.minus_1_button.setObjectName(u"minus_1_button")
        self.minus_1_button.setEnabled(False)

        self.gridLayout_4.addWidget(self.minus_1_button, 1, 1, 1, 1)

        self.plus_1_button = QPushButton(self.actuator_properties_tab)
        self.plus_1_button.setObjectName(u"plus_1_button")
        self.plus_1_button.setEnabled(False)

        self.gridLayout_4.addWidget(self.plus_1_button, 1, 0, 1, 1)

        self.step_size_1_label = QLabel(self.actuator_properties_tab)
        self.step_size_1_label.setObjectName(u"step_size_1_label")

        self.gridLayout_4.addWidget(self.step_size_1_label, 0, 0, 1, 1)

        self.step_size_1 = QSpinBox(self.actuator_properties_tab)
        self.step_size_1.setObjectName(u"step_size_1")
        self.step_size_1.setEnabled(False)
        self.step_size_1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.step_size_1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.step_size_1.setMinimum(1)
        self.step_size_1.setMaximum(1000000000)

        self.gridLayout_4.addWidget(self.step_size_1, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_4, 2, 3, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 6, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.move_mode_label = QLabel(self.actuator_properties_tab)
        self.move_mode_label.setObjectName(u"move_mode_label")
        self.move_mode_label.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.move_mode_label)

        self.move_mode_select = QComboBox(self.actuator_properties_tab)
        self.move_mode_select.setObjectName(u"move_mode_select")
        self.move_mode_select.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.move_mode_select)


        self.gridLayout_2.addLayout(self.horizontalLayout_10, 4, 1, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.minus_0_button = QPushButton(self.actuator_properties_tab)
        self.minus_0_button.setObjectName(u"minus_0_button")
        self.minus_0_button.setEnabled(False)

        self.gridLayout_3.addWidget(self.minus_0_button, 1, 1, 1, 1)

        self.plus_0_button = QPushButton(self.actuator_properties_tab)
        self.plus_0_button.setObjectName(u"plus_0_button")
        self.plus_0_button.setEnabled(False)

        self.gridLayout_3.addWidget(self.plus_0_button, 1, 0, 1, 1)

        self.step_size_0_label = QLabel(self.actuator_properties_tab)
        self.step_size_0_label.setObjectName(u"step_size_0_label")

        self.gridLayout_3.addWidget(self.step_size_0_label, 0, 0, 1, 1)

        self.step_size_0 = QSpinBox(self.actuator_properties_tab)
        self.step_size_0.setObjectName(u"step_size_0")
        self.step_size_0.setEnabled(False)
        self.step_size_0.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.step_size_0.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.step_size_0.setMinimum(1)
        self.step_size_0.setMaximum(1000000000)

        self.gridLayout_3.addWidget(self.step_size_0, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_3, 2, 1, 1, 1)

        self.label_5 = QLabel(self.actuator_properties_tab)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 1, 6, 1, 1)

        self.channel_1_layout = QFormLayout()
        self.channel_1_layout.setObjectName(u"channel_1_layout")
        self.channel_1_label = QLabel(self.actuator_properties_tab)
        self.channel_1_label.setObjectName(u"channel_1_label")
        self.channel_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.channel_1_layout.setWidget(0, QFormLayout.SpanningRole, self.channel_1_label)

        self.position_1_label = QLabel(self.actuator_properties_tab)
        self.position_1_label.setObjectName(u"position_1_label")

        self.channel_1_layout.setWidget(1, QFormLayout.LabelRole, self.position_1_label)

        self.position_1 = QSpinBox(self.actuator_properties_tab)
        self.position_1.setObjectName(u"position_1")
        self.position_1.setEnabled(False)
        self.position_1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.position_1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.position_1.setMinimum(-1000000000)
        self.position_1.setMaximum(1000000000)

        self.channel_1_layout.setWidget(1, QFormLayout.FieldRole, self.position_1)

        self.velocity_1_label = QLabel(self.actuator_properties_tab)
        self.velocity_1_label.setObjectName(u"velocity_1_label")

        self.channel_1_layout.setWidget(2, QFormLayout.LabelRole, self.velocity_1_label)

        self.velocity_1 = QSpinBox(self.actuator_properties_tab)
        self.velocity_1.setObjectName(u"velocity_1")
        self.velocity_1.setEnabled(False)
        self.velocity_1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.velocity_1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.velocity_1.setKeyboardTracking(False)
        self.velocity_1.setMaximum(1000000000)

        self.channel_1_layout.setWidget(2, QFormLayout.FieldRole, self.velocity_1)

        self.acceleration_1_label = QLabel(self.actuator_properties_tab)
        self.acceleration_1_label.setObjectName(u"acceleration_1_label")

        self.channel_1_layout.setWidget(3, QFormLayout.LabelRole, self.acceleration_1_label)

        self.acceleration_1 = QSpinBox(self.actuator_properties_tab)
        self.acceleration_1.setObjectName(u"acceleration_1")
        self.acceleration_1.setEnabled(False)
        self.acceleration_1.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.acceleration_1.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.acceleration_1.setKeyboardTracking(False)
        self.acceleration_1.setMaximum(1000000000)

        self.channel_1_layout.setWidget(3, QFormLayout.FieldRole, self.acceleration_1)


        self.gridLayout_2.addLayout(self.channel_1_layout, 0, 3, 1, 1)

        self.label_8 = QLabel(self.actuator_properties_tab)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 0, 4, 1, 1)

        self.channel_2_layout = QFormLayout()
        self.channel_2_layout.setObjectName(u"channel_2_layout")
        self.channel_2_label = QLabel(self.actuator_properties_tab)
        self.channel_2_label.setObjectName(u"channel_2_label")
        self.channel_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.channel_2_layout.setWidget(0, QFormLayout.SpanningRole, self.channel_2_label)

        self.position_2_label = QLabel(self.actuator_properties_tab)
        self.position_2_label.setObjectName(u"position_2_label")

        self.channel_2_layout.setWidget(1, QFormLayout.LabelRole, self.position_2_label)

        self.position_2 = QSpinBox(self.actuator_properties_tab)
        self.position_2.setObjectName(u"position_2")
        self.position_2.setEnabled(False)
        self.position_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.position_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.position_2.setMinimum(-1000000000)
        self.position_2.setMaximum(1000000000)

        self.channel_2_layout.setWidget(1, QFormLayout.FieldRole, self.position_2)

        self.velocity_2_label = QLabel(self.actuator_properties_tab)
        self.velocity_2_label.setObjectName(u"velocity_2_label")

        self.channel_2_layout.setWidget(2, QFormLayout.LabelRole, self.velocity_2_label)

        self.velocity_2 = QSpinBox(self.actuator_properties_tab)
        self.velocity_2.setObjectName(u"velocity_2")
        self.velocity_2.setEnabled(False)
        self.velocity_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.velocity_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.velocity_2.setMinimum(0)
        self.velocity_2.setMaximum(1000000000)

        self.channel_2_layout.setWidget(2, QFormLayout.FieldRole, self.velocity_2)

        self.acceleration_2_label = QLabel(self.actuator_properties_tab)
        self.acceleration_2_label.setObjectName(u"acceleration_2_label")

        self.channel_2_layout.setWidget(3, QFormLayout.LabelRole, self.acceleration_2_label)

        self.acceleration_2 = QSpinBox(self.actuator_properties_tab)
        self.acceleration_2.setObjectName(u"acceleration_2")
        self.acceleration_2.setEnabled(False)
        self.acceleration_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.acceleration_2.setReadOnly(False)
        self.acceleration_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.acceleration_2.setMinimum(0)
        self.acceleration_2.setMaximum(1000000000)

        self.channel_2_layout.setWidget(3, QFormLayout.FieldRole, self.acceleration_2)


        self.gridLayout_2.addLayout(self.channel_2_layout, 0, 5, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.minus_2_button = QPushButton(self.actuator_properties_tab)
        self.minus_2_button.setObjectName(u"minus_2_button")
        self.minus_2_button.setEnabled(False)

        self.gridLayout_5.addWidget(self.minus_2_button, 1, 1, 1, 1)

        self.plus_2_button = QPushButton(self.actuator_properties_tab)
        self.plus_2_button.setObjectName(u"plus_2_button")
        self.plus_2_button.setEnabled(False)

        self.gridLayout_5.addWidget(self.plus_2_button, 1, 0, 1, 1)

        self.step_size_2_label = QLabel(self.actuator_properties_tab)
        self.step_size_2_label.setObjectName(u"step_size_2_label")

        self.gridLayout_5.addWidget(self.step_size_2_label, 0, 0, 1, 1)

        self.step_size_2 = QSpinBox(self.actuator_properties_tab)
        self.step_size_2.setObjectName(u"step_size_2")
        self.step_size_2.setEnabled(False)
        self.step_size_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.step_size_2.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.step_size_2.setMinimum(1)
        self.step_size_2.setMaximum(1000000000)

        self.gridLayout_5.addWidget(self.step_size_2, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout_5, 2, 5, 1, 1)

        self.label_6 = QLabel(self.actuator_properties_tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 3, 1, 1, 1)

        self.rc_layout = QHBoxLayout()
        self.rc_layout.setObjectName(u"rc_layout")
        self.reference_button = QPushButton(self.actuator_properties_tab)
        self.reference_button.setObjectName(u"reference_button")
        self.reference_button.setEnabled(False)

        self.rc_layout.addWidget(self.reference_button)

        self.calibrate_button = QPushButton(self.actuator_properties_tab)
        self.calibrate_button.setObjectName(u"calibrate_button")
        self.calibrate_button.setEnabled(False)

        self.rc_layout.addWidget(self.calibrate_button)


        self.gridLayout_2.addLayout(self.rc_layout, 4, 3, 1, 1)

        self.channel_0_layout = QFormLayout()
        self.channel_0_layout.setObjectName(u"channel_0_layout")
        self.channel_0_label = QLabel(self.actuator_properties_tab)
        self.channel_0_label.setObjectName(u"channel_0_label")
        self.channel_0_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.channel_0_layout.setWidget(0, QFormLayout.SpanningRole, self.channel_0_label)

        self.position_0_label = QLabel(self.actuator_properties_tab)
        self.position_0_label.setObjectName(u"position_0_label")

        self.channel_0_layout.setWidget(1, QFormLayout.LabelRole, self.position_0_label)

        self.position_0 = QSpinBox(self.actuator_properties_tab)
        self.position_0.setObjectName(u"position_0")
        self.position_0.setEnabled(False)
        self.position_0.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.position_0.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.position_0.setKeyboardTracking(False)
        self.position_0.setMinimum(-1000000000)
        self.position_0.setMaximum(1000000000)
        self.position_0.setStepType(QAbstractSpinBox.StepType.DefaultStepType)

        self.channel_0_layout.setWidget(1, QFormLayout.FieldRole, self.position_0)

        self.velocity_0_label = QLabel(self.actuator_properties_tab)
        self.velocity_0_label.setObjectName(u"velocity_0_label")

        self.channel_0_layout.setWidget(2, QFormLayout.LabelRole, self.velocity_0_label)

        self.velocity_0 = QSpinBox(self.actuator_properties_tab)
        self.velocity_0.setObjectName(u"velocity_0")
        self.velocity_0.setEnabled(False)
        self.velocity_0.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.velocity_0.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.velocity_0.setKeyboardTracking(False)
        self.velocity_0.setMaximum(1000000000)

        self.channel_0_layout.setWidget(2, QFormLayout.FieldRole, self.velocity_0)

        self.acceleration_0_label = QLabel(self.actuator_properties_tab)
        self.acceleration_0_label.setObjectName(u"acceleration_0_label")

        self.channel_0_layout.setWidget(3, QFormLayout.LabelRole, self.acceleration_0_label)

        self.acceleration_0 = QSpinBox(self.actuator_properties_tab)
        self.acceleration_0.setObjectName(u"acceleration_0")
        self.acceleration_0.setEnabled(False)
        self.acceleration_0.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.acceleration_0.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.acceleration_0.setKeyboardTracking(False)
        self.acceleration_0.setMaximum(1000000000)

        self.channel_0_layout.setWidget(3, QFormLayout.FieldRole, self.acceleration_0)


        self.gridLayout_2.addLayout(self.channel_0_layout, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.actuator_properties_tab, "")
        self.camera_properties_tab = QWidget()
        self.camera_properties_tab.setObjectName(u"camera_properties_tab")
        self.gridLayout = QGridLayout(self.camera_properties_tab)
        self.gridLayout.setObjectName(u"gridLayout")
        self.live_feed = QLabel(self.camera_properties_tab)
        self.live_feed.setObjectName(u"live_feed")
        self.live_feed.setEnabled(True)
        self.live_feed.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.live_feed, 0, 1, 1, 1)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.camera_properties_tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.cameras = QComboBox(self.camera_properties_tab)
        self.cameras.setObjectName(u"cameras")

        self.horizontalLayout_6.addWidget(self.cameras)

        self.refresh_camera_button = QPushButton(self.camera_properties_tab)
        self.refresh_camera_button.setObjectName(u"refresh_camera_button")

        self.horizontalLayout_6.addWidget(self.refresh_camera_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.select_label = QLabel(self.camera_properties_tab)
        self.select_label.setObjectName(u"select_label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_label.sizePolicy().hasHeightForWidth())
        self.select_label.setSizePolicy(sizePolicy)

        self.gridLayout_7.addWidget(self.select_label, 0, 0, 1, 1)

        self.directory_label = QLabel(self.camera_properties_tab)
        self.directory_label.setObjectName(u"directory_label")

        self.gridLayout_7.addWidget(self.directory_label, 0, 1, 1, 1)

        self.directory_button = QToolButton(self.camera_properties_tab)
        self.directory_button.setObjectName(u"directory_button")

        self.gridLayout_7.addWidget(self.directory_button, 0, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_7)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.exposure_label = QLabel(self.camera_properties_tab)
        self.exposure_label.setObjectName(u"exposure_label")

        self.gridLayout_6.addWidget(self.exposure_label, 0, 0, 1, 1)

        self.exposure = QSpinBox(self.camera_properties_tab)
        self.exposure.setObjectName(u"exposure")
        self.exposure.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.exposure.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.exposure.setKeyboardTracking(False)

        self.gridLayout_6.addWidget(self.exposure, 0, 1, 1, 1)

        self.frames_label = QLabel(self.camera_properties_tab)
        self.frames_label.setObjectName(u"frames_label")

        self.gridLayout_6.addWidget(self.frames_label, 1, 0, 1, 1)

        self.frames = QSpinBox(self.camera_properties_tab)
        self.frames.setObjectName(u"frames")
        self.frames.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.frames.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.frames.setKeyboardTracking(False)
        self.frames.setMinimum(1)
        self.frames.setMaximum(100)

        self.gridLayout_6.addWidget(self.frames, 1, 1, 1, 1)

        self.capture_button = QPushButton(self.camera_properties_tab)
        self.capture_button.setObjectName(u"capture_button")

        self.gridLayout_6.addWidget(self.capture_button, 2, 0, 1, 1)

        self.stop_button = QPushButton(self.camera_properties_tab)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy1)
        self.stop_button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.gridLayout_6.addWidget(self.stop_button, 2, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_6)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.camera_properties_tab, "")
        self.acquisition_tab = QWidget()
        self.acquisition_tab.setObjectName(u"acquisition_tab")
        self.gridLayout_9 = QGridLayout(self.acquisition_tab)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.acquisition_layout = QHBoxLayout()
        self.acquisition_layout.setObjectName(u"acquisition_layout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.center_z_label = QLabel(self.acquisition_tab)
        self.center_z_label.setObjectName(u"center_z_label")

        self.gridLayout_10.addWidget(self.center_z_label, 3, 0, 1, 1)

        self.trajectory_select = QComboBox(self.acquisition_tab)
        self.trajectory_select.setObjectName(u"trajectory_select")

        self.gridLayout_10.addWidget(self.trajectory_select, 0, 1, 1, 1)

        self.trajectory_center_x = QSpinBox(self.acquisition_tab)
        self.trajectory_center_x.setObjectName(u"trajectory_center_x")
        self.trajectory_center_x.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.trajectory_center_x.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.trajectory_center_x.setMinimum(-1000000000)
        self.trajectory_center_x.setMaximum(1000000000)

        self.gridLayout_10.addWidget(self.trajectory_center_x, 1, 1, 1, 1)

        self.trajectory_center_z = QSpinBox(self.acquisition_tab)
        self.trajectory_center_z.setObjectName(u"trajectory_center_z")
        self.trajectory_center_z.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.trajectory_center_z.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.trajectory_center_z.setMinimum(-1000000000)
        self.trajectory_center_z.setMaximum(1000000000)

        self.gridLayout_10.addWidget(self.trajectory_center_z, 3, 1, 1, 1)

        self.center_y_label = QLabel(self.acquisition_tab)
        self.center_y_label.setObjectName(u"center_y_label")

        self.gridLayout_10.addWidget(self.center_y_label, 2, 0, 1, 1)

        self.trajectory_label = QLabel(self.acquisition_tab)
        self.trajectory_label.setObjectName(u"trajectory_label")

        self.gridLayout_10.addWidget(self.trajectory_label, 0, 0, 1, 1)

        self.trajectory_stop_button = QPushButton(self.acquisition_tab)
        self.trajectory_stop_button.setObjectName(u"trajectory_stop_button")
        self.trajectory_stop_button.setEnabled(False)

        self.gridLayout_10.addWidget(self.trajectory_stop_button, 6, 1, 1, 1)

        self.start_trajectory_button = QPushButton(self.acquisition_tab)
        self.start_trajectory_button.setObjectName(u"start_trajectory_button")
        self.start_trajectory_button.setEnabled(False)

        self.gridLayout_10.addWidget(self.start_trajectory_button, 6, 0, 1, 1)

        self.center_x_label = QLabel(self.acquisition_tab)
        self.center_x_label.setObjectName(u"center_x_label")

        self.gridLayout_10.addWidget(self.center_x_label, 1, 0, 1, 1)

        self.trajectory_center_y = QSpinBox(self.acquisition_tab)
        self.trajectory_center_y.setObjectName(u"trajectory_center_y")
        self.trajectory_center_y.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.trajectory_center_y.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.trajectory_center_y.setMinimum(-1000000000)
        self.trajectory_center_y.setMaximum(1000000000)

        self.gridLayout_10.addWidget(self.trajectory_center_y, 2, 1, 1, 1)

        self.trajectory_generate_button = QPushButton(self.acquisition_tab)
        self.trajectory_generate_button.setObjectName(u"trajectory_generate_button")

        self.gridLayout_10.addWidget(self.trajectory_generate_button, 5, 0, 1, 2)

        self.radius_label = QLabel(self.acquisition_tab)
        self.radius_label.setObjectName(u"radius_label")

        self.gridLayout_10.addWidget(self.radius_label, 4, 0, 1, 1)

        self.trajectory_radius = QSpinBox(self.acquisition_tab)
        self.trajectory_radius.setObjectName(u"trajectory_radius")
        self.trajectory_radius.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.trajectory_radius.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.trajectory_radius.setMinimum(0)
        self.trajectory_radius.setMaximum(1000000000)

        self.gridLayout_10.addWidget(self.trajectory_radius, 4, 1, 1, 1)


        self.verticalLayout_5.addLayout(self.gridLayout_10)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)


        self.acquisition_layout.addLayout(self.verticalLayout_5)


        self.gridLayout_9.addLayout(self.acquisition_layout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.acquisition_tab, "")
        self.algorithm_tab = QWidget()
        self.algorithm_tab.setObjectName(u"algorithm_tab")
        self.tabWidget.addTab(self.algorithm_tab, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 805, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.devices_label.setText(QCoreApplication.translate("MainWindow", u"Devices", None))
        self.devices.setPlaceholderText(QCoreApplication.translate("MainWindow", u"No devices found", None))
        self.refresh_button.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.error_label.setText("")
        self.label_9.setText("")
        self.label_7.setText("")
        self.move_button.setText(QCoreApplication.translate("MainWindow", u"Move", None))
        self.minus_1_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.plus_1_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.step_size_1_label.setText(QCoreApplication.translate("MainWindow", u"Step Size [nm]", None))
        self.move_mode_label.setText(QCoreApplication.translate("MainWindow", u"Move Mode", None))
        self.move_mode_select.setPlaceholderText(QCoreApplication.translate("MainWindow", u"No mode selected", None))
        self.minus_0_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.plus_0_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.step_size_0_label.setText(QCoreApplication.translate("MainWindow", u"Step Size [nm]", None))
        self.label_5.setText("")
        self.channel_1_label.setText(QCoreApplication.translate("MainWindow", u"Channel 1 [Y]:", None))
        self.position_1_label.setText(QCoreApplication.translate("MainWindow", u"Position [nm]", None))
        self.velocity_1_label.setText(QCoreApplication.translate("MainWindow", u"Velocity [nm/s]", None))
        self.acceleration_1_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acceleration [nm/s<span style=\" vertical-align:super;\">2</span>]</p></body></html>", None))
        self.label_8.setText("")
        self.channel_2_label.setText(QCoreApplication.translate("MainWindow", u"Channel 2 [Z]", None))
        self.position_2_label.setText(QCoreApplication.translate("MainWindow", u"Position [nm]", None))
        self.velocity_2_label.setText(QCoreApplication.translate("MainWindow", u"Velocity [nm/s]", None))
        self.acceleration_2_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acceleration [nm/s<span style=\" vertical-align:super;\">2</span>]</p></body></html>", None))
        self.minus_2_button.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.plus_2_button.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.step_size_2_label.setText(QCoreApplication.translate("MainWindow", u"Step Size [nm]", None))
        self.label_6.setText("")
        self.reference_button.setText(QCoreApplication.translate("MainWindow", u"Reference", None))
        self.calibrate_button.setText(QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.channel_0_label.setText(QCoreApplication.translate("MainWindow", u"Channel 0 [X]:", None))
        self.position_0_label.setText(QCoreApplication.translate("MainWindow", u"Position [nm]", None))
        self.velocity_0_label.setText(QCoreApplication.translate("MainWindow", u"Velocity [nm/s]", None))
        self.acceleration_0_label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acceleration [nm/s<span style=\" vertical-align:super;\">2</span>]</p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.actuator_properties_tab), QCoreApplication.translate("MainWindow", u"Actuator Properties", None))
        self.live_feed.setText(QCoreApplication.translate("MainWindow", u"Live feed", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Camera", None))
#if QT_CONFIG(accessibility)
        self.cameras.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.cameras.setPlaceholderText(QCoreApplication.translate("MainWindow", u"No devices found", None))
        self.refresh_camera_button.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.select_label.setText(QCoreApplication.translate("MainWindow", u"Select Directory", None))
        self.directory_label.setText("")
        self.directory_button.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.exposure_label.setText(QCoreApplication.translate("MainWindow", u"Exposure Time [\u03bcs]", None))
        self.frames_label.setText(QCoreApplication.translate("MainWindow", u"Number of Frames", None))
        self.capture_button.setText(QCoreApplication.translate("MainWindow", u"Capture", None))
        self.stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.camera_properties_tab), QCoreApplication.translate("MainWindow", u"Camera Properties", None))
        self.center_z_label.setText(QCoreApplication.translate("MainWindow", u"Center Z [nm]", None))
        self.center_y_label.setText(QCoreApplication.translate("MainWindow", u"Center Y [nm]", None))
        self.trajectory_label.setText(QCoreApplication.translate("MainWindow", u"Trajectory", None))
        self.trajectory_stop_button.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.start_trajectory_button.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.center_x_label.setText(QCoreApplication.translate("MainWindow", u"Center X [nm]", None))
        self.trajectory_generate_button.setText(QCoreApplication.translate("MainWindow", u"Generate", None))
        self.radius_label.setText(QCoreApplication.translate("MainWindow", u"Radius [nm]", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.acquisition_tab), QCoreApplication.translate("MainWindow", u"Ptychographic Acquisition", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.algorithm_tab), QCoreApplication.translate("MainWindow", u"Ptychographic Algorithm", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

