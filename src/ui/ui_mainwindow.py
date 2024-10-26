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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QSizePolicy, QStatusBar, QToolBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1150, 815)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1150, 815))
        self.actionSelect_Mode = QAction(MainWindow)
        self.actionSelect_Mode.setObjectName(u"actionSelect_Mode")
        icon = QIcon(QIcon.fromTheme(u"camera-web"))
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
        self.actionActionConfigureEmail = QAction(MainWindow)
        self.actionActionConfigureEmail.setObjectName(u"actionActionConfigureEmail")
        icon3 = QIcon(QIcon.fromTheme(u"emblem-mail"))
        self.actionActionConfigureEmail.setIcon(icon3)
        self.actionActionConfigureEmail.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSelectLocalCameras = QAction(MainWindow)
        self.actionSelectLocalCameras.setObjectName(u"actionSelectLocalCameras")
        icon4 = QIcon(QIcon.fromTheme(u"camera-video"))
        self.actionSelectLocalCameras.setIcon(icon4)
        self.actionSelectLocalCameras.setMenuRole(QAction.MenuRole.NoRole)
        self.actionConfigure_Ai_model = QAction(MainWindow)
        self.actionConfigure_Ai_model.setObjectName(u"actionConfigure_Ai_model")
        icon5 = QIcon()
        icon5.addFile(u"icons/icon-ai-24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionConfigure_Ai_model.setIcon(icon5)
        self.actionConfigure_Ai_model.setMenuRole(QAction.MenuRole.NoRole)
        self.actionOpen_configuration_file = QAction(MainWindow)
        self.actionOpen_configuration_file.setObjectName(u"actionOpen_configuration_file")
        icon6 = QIcon(QIcon.fromTheme(u"document-open"))
        self.actionOpen_configuration_file.setIcon(icon6)
        self.actionOpen_configuration_file.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSave_configuration_as = QAction(MainWindow)
        self.actionSave_configuration_as.setObjectName(u"actionSave_configuration_as")
        icon7 = QIcon(QIcon.fromTheme(u"document-save-as"))
        self.actionSave_configuration_as.setIcon(icon7)
        self.actionSave_configuration_as.setMenuRole(QAction.MenuRole.NoRole)
        self.actionOpen_configuration_file_menu = QAction(MainWindow)
        self.actionOpen_configuration_file_menu.setObjectName(u"actionOpen_configuration_file_menu")
        self.actionOpen_configuration_file_menu.setIcon(icon6)
        self.actionSave_configuration_as_menu = QAction(MainWindow)
        self.actionSave_configuration_as_menu.setObjectName(u"actionSave_configuration_as_menu")
        self.actionSave_configuration_as_menu.setIcon(icon7)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        icon8 = QIcon(QIcon.fromTheme(u"dialog-question"))
        self.actionAbout.setIcon(icon8)
        self.actionLicense = QAction(MainWindow)
        self.actionLicense.setObjectName(u"actionLicense")
        self.actionSave_configuration = QAction(MainWindow)
        self.actionSave_configuration.setObjectName(u"actionSave_configuration")
        icon9 = QIcon(QIcon.fromTheme(u"document-save"))
        self.actionSave_configuration.setIcon(icon9)
        self.actionSave_configuration.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSave_configuration_menu = QAction(MainWindow)
        self.actionSave_configuration_menu.setObjectName(u"actionSave_configuration_menu")
        self.actionSave_configuration_menu.setIcon(icon9)
        self.actionSave_configuration_menu.setMenuRole(QAction.MenuRole.NoRole)
        self.actionConfigure_FTP_Cameras = QAction(MainWindow)
        self.actionConfigure_FTP_Cameras.setObjectName(u"actionConfigure_FTP_Cameras")
        icon10 = QIcon(QIcon.fromTheme(u"system-file-manager"))
        self.actionConfigure_FTP_Cameras.setIcon(icon10)
        self.actionConfigure_FTP_Cameras.setMenuRole(QAction.MenuRole.NoRole)
        self.actionactionConfigure_actuators = QAction(MainWindow)
        self.actionactionConfigure_actuators.setObjectName(u"actionactionConfigure_actuators")
        icon11 = QIcon()
        icon11.addFile(u"icons/icon-actuator-24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionactionConfigure_actuators.setIcon(icon11)
        self.actionactionConfigure_actuators.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_image = QLabel(self.centralwidget)
        self.label_image.setObjectName(u"label_image")
        self.label_image.setEnabled(True)
        self.label_image.setGeometry(QRect(10, 10, 800, 600))
        sizePolicy.setHeightForWidth(self.label_image.sizePolicy().hasHeightForWidth())
        self.label_image.setSizePolicy(sizePolicy)
        self.plainTextEdit_log = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_log.setObjectName(u"plainTextEdit_log")
        self.plainTextEdit_log.setGeometry(QRect(10, 620, 1121, 109))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.plainTextEdit_log.sizePolicy().hasHeightForWidth())
        self.plainTextEdit_log.setSizePolicy(sizePolicy1)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(830, 10, 301, 601))
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

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.listWidget_en_cameras = QListWidget(self.verticalLayoutWidget)
        self.listWidget_en_cameras.setObjectName(u"listWidget_en_cameras")

        self.verticalLayout.addWidget(self.listWidget_en_cameras)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.listWidget_en_actuators = QListWidget(self.verticalLayoutWidget)
        self.listWidget_en_actuators.setObjectName(u"listWidget_en_actuators")

        self.verticalLayout.addWidget(self.listWidget_en_actuators)

        self.label_classified_animal_title = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal_title.setObjectName(u"label_classified_animal_title")
        self.label_classified_animal_title.setFont(font)

        self.verticalLayout.addWidget(self.label_classified_animal_title)

        self.label_classified_animal = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal.setObjectName(u"label_classified_animal")

        self.verticalLayout.addWidget(self.label_classified_animal)

        self.label_last_classification_title = QLabel(self.verticalLayoutWidget)
        self.label_last_classification_title.setObjectName(u"label_last_classification_title")
        self.label_last_classification_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_classification_title)

        self.label_last_classification = QLabel(self.verticalLayoutWidget)
        self.label_last_classification.setObjectName(u"label_last_classification")
        sizePolicy2.setHeightForWidth(self.label_last_classification.sizePolicy().hasHeightForWidth())
        self.label_last_classification.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_classification)

        self.label_last_detection_title = QLabel(self.verticalLayoutWidget)
        self.label_last_detection_title.setObjectName(u"label_last_detection_title")
        self.label_last_detection_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_detection_title)

        self.label_last_detection = QLabel(self.verticalLayoutWidget)
        self.label_last_detection.setObjectName(u"label_last_detection")
        sizePolicy2.setHeightForWidth(self.label_last_detection.sizePolicy().hasHeightForWidth())
        self.label_last_detection.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_detection)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(803, 10, 20, 601))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionOpen_configuration_file_menu)
        self.menuFile.addAction(self.actionSave_configuration_as_menu)
        self.menuFile.addAction(self.actionSave_configuration_menu)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionLicense)
        self.toolBar.addAction(self.actionOpen_configuration_file)
        self.toolBar.addAction(self.actionSave_configuration_as)
        self.toolBar.addAction(self.actionSave_configuration)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSelectLocalCameras)
        self.toolBar.addAction(self.actionConfigure_FTP_Cameras)
        self.toolBar.addAction(self.actionactionConfigure_actuators)
        self.toolBar.addAction(self.actionActionConfigureEmail)
        self.toolBar.addAction(self.actionSelect_Mode)
        self.toolBar.addAction(self.actionConfigure_Ai_model)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStop)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Wild Animals Detection and Alert System (WADAS) [*]", None))
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
        self.actionActionConfigureEmail.setText(QCoreApplication.translate("MainWindow", u"ActionConfigureEmail", None))
#if QT_CONFIG(tooltip)
        self.actionActionConfigureEmail.setToolTip(QCoreApplication.translate("MainWindow", u"Configure Email notifications", None))
#endif // QT_CONFIG(tooltip)
        self.actionSelectLocalCameras.setText(QCoreApplication.translate("MainWindow", u"selectLocalCameras", None))
#if QT_CONFIG(tooltip)
        self.actionSelectLocalCameras.setToolTip(QCoreApplication.translate("MainWindow", u"Configure camera(s)", None))
#endif // QT_CONFIG(tooltip)
        self.actionConfigure_Ai_model.setText(QCoreApplication.translate("MainWindow", u"Configure Ai model", None))
        self.actionOpen_configuration_file.setText(QCoreApplication.translate("MainWindow", u"Open configuration file", None))
        self.actionSave_configuration_as.setText(QCoreApplication.translate("MainWindow", u"Save configuration as", None))
#if QT_CONFIG(tooltip)
        self.actionSave_configuration_as.setToolTip(QCoreApplication.translate("MainWindow", u"Save configuration as ...", None))
#endif // QT_CONFIG(tooltip)
        self.actionOpen_configuration_file_menu.setText(QCoreApplication.translate("MainWindow", u"Open configuration file", None))
        self.actionSave_configuration_as_menu.setText(QCoreApplication.translate("MainWindow", u"Save configuration as ...", None))
#if QT_CONFIG(tooltip)
        self.actionSave_configuration_as_menu.setToolTip(QCoreApplication.translate("MainWindow", u"Save configuration as ...", None))
#endif // QT_CONFIG(tooltip)
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionLicense.setText(QCoreApplication.translate("MainWindow", u"License", None))
        self.actionSave_configuration.setText(QCoreApplication.translate("MainWindow", u"Save configuration", None))
#if QT_CONFIG(tooltip)
        self.actionSave_configuration.setToolTip(QCoreApplication.translate("MainWindow", u"Save configuration", None))
#endif // QT_CONFIG(tooltip)
        self.actionSave_configuration_menu.setText(QCoreApplication.translate("MainWindow", u"Save configuration", None))
#if QT_CONFIG(tooltip)
        self.actionSave_configuration_menu.setToolTip(QCoreApplication.translate("MainWindow", u"Save configuration", None))
#endif // QT_CONFIG(tooltip)
        self.actionConfigure_FTP_Cameras.setText(QCoreApplication.translate("MainWindow", u"Configure FTP Cameras", None))
#if QT_CONFIG(tooltip)
        self.actionConfigure_FTP_Cameras.setToolTip(QCoreApplication.translate("MainWindow", u"Configure FTP cameras and server", None))
#endif // QT_CONFIG(tooltip)
        self.actionactionConfigure_actuators.setText(QCoreApplication.translate("MainWindow", u"actionConfigure_actuators", None))
#if QT_CONFIG(tooltip)
        self.actionactionConfigure_actuators.setToolTip(QCoreApplication.translate("MainWindow", u"Configure actuators", None))
#endif // QT_CONFIG(tooltip)
        self.label_image.setText(QCoreApplication.translate("MainWindow", u"Detecion viewer", None))
        self.label_op_mode_title.setText(QCoreApplication.translate("MainWindow", u"Operation mode:", None))
        self.label_op_mode.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Enabled Camera(s):", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Enabled Actuator(s)", None))
        self.label_classified_animal_title.setText(QCoreApplication.translate("MainWindow", u"Classified animal(s):", None))
        self.label_classified_animal.setText("")
        self.label_last_classification_title.setText(QCoreApplication.translate("MainWindow", u"Last classification:", None))
        self.label_last_classification.setText("")
        self.label_last_detection_title.setText(QCoreApplication.translate("MainWindow", u"Last detection:", None))
        self.label_last_detection.setText("")
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

