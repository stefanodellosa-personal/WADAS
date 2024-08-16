# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QSizePolicy, QSpacerItem, QStatusBar,
    QToolBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1090, 815)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionSelect_Mode = QAction(MainWindow)
        self.actionSelect_Mode.setObjectName(u"actionSelect_Mode")
        icon = QIcon(QIcon.fromTheme(u"camera-video"))
        self.actionSelect_Mode.setIcon(icon)
        self.actionSelect_Mode.setMenuRole(QAction.MenuRole.NoRole)
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName(u"actionRun")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.actionRun.setIcon(icon1)
        self.actionRun.setMenuRole(QAction.MenuRole.NoRole)
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName(u"actionStop")
        icon2 = QIcon(QIcon.fromTheme(u"media-playback-stop"))
        self.actionStop.setIcon(icon2)
        self.actionStop.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_image = QLabel(self.centralwidget)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setEnabled(True)
        self.label_image.setGeometry(QRect(10, 10, 800, 600))
        self.plainTextEdit_log = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_log.setObjectName(u"plainTextEdit_log")
        self.plainTextEdit_log.setGeometry(QRect(10, 650, 1071, 81))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plainTextEdit_log.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_log.setSizePolicy(sizePolicy1)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(830, 10, 251, 631))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_op_mode_title = QLabel(self.verticalLayoutWidget)
        self.label_op_mode_title.setObjectName(u"label_op_mode_title")
        font = QFont()
        font.setBold(True)
        self.label_op_mode_title.setFont(font)

        self.verticalLayout.addWidget(self.label_op_mode_title)

        self.label_op_mode = QLabel(self.verticalLayoutWidget)
        self.label_op_mode.setObjectName(u"label_op_mode")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_op_mode.sizePolicy().hasHeightForWidth())
        self.label_op_mode.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_op_mode)

        self.label_last_detection_title = QLabel(self.verticalLayoutWidget)
        self.label_last_detection_title.setObjectName(u"label_last_detection_title")
        self.label_last_detection_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_detection_title)

        self.label_last_detection = QLabel(self.verticalLayoutWidget)
        self.label_last_detection.setObjectName(u"label_last_detection")
        sizePolicy2.setHeightForWidth(self.label_last_detection.sizePolicy().hasHeightForWidth())
        self.label_last_detection.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_detection)

        self.label_last_classification_title = QLabel(self.verticalLayoutWidget)
        self.label_last_classification_title.setObjectName(u"label_last_classification_title")
        self.label_last_classification_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_classification_title)

        self.label_last_classification = QLabel(self.verticalLayoutWidget)
        self.label_last_classification.setObjectName(u"label_last_classification")
        sizePolicy2.setHeightForWidth(self.label_last_classification.sizePolicy().hasHeightForWidth())
        self.label_last_classification.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_classification)

        self.label_classified_animal_title = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal_title.setObjectName(u"label_classified_animal_title")
        self.label_classified_animal_title.setFont(font)

        self.verticalLayout.addWidget(self.label_classified_animal_title)

        self.label_classified_animal = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal.setObjectName(u"label_classified_animal")

        self.verticalLayout.addWidget(self.label_classified_animal)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1090, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.toolBar.addAction(self.actionSelect_Mode)
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStop)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"WADAS", None))
        self.actionSelect_Mode.setText(QCoreApplication.translate("MainWindow", u"Select Mode", None))
#if QT_CONFIG(tooltip)
        self.actionSelect_Mode.setToolTip(QCoreApplication.translate("MainWindow", u"Select operating mode", None))
#endif // QT_CONFIG(tooltip)
        self.actionRun.setText(QCoreApplication.translate("MainWindow", u"Run", None))
#if QT_CONFIG(tooltip)
        self.actionRun.setToolTip(QCoreApplication.translate("MainWindow", u"Run detection", None))
#endif // QT_CONFIG(tooltip)
        self.actionStop.setText(QCoreApplication.translate("MainWindow", u"Stop ", None))
#if QT_CONFIG(tooltip)
        self.actionStop.setToolTip(QCoreApplication.translate("MainWindow", u"Stop detection", None))
#endif // QT_CONFIG(tooltip)
        self.label_image.setText(QCoreApplication.translate("MainWindow", u"Detecion viewer", None))
        self.label_op_mode_title.setText(QCoreApplication.translate("MainWindow", u"Operation mode:", None))
        self.label_op_mode.setText("")
        self.label_last_detection_title.setText(QCoreApplication.translate("MainWindow", u"Last detection:", None))
        self.label_last_detection.setText("")
        self.label_last_classification_title.setText(QCoreApplication.translate("MainWindow", u"Last classification:", None))
        self.label_last_classification.setText("")
        self.label_classified_animal_title.setText(QCoreApplication.translate("MainWindow", u"Classified animal(s):", None))
        self.label_classified_animal.setText("")
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

