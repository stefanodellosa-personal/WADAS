# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPlainTextEdit,
    QSizePolicy,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 815)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(1150, 815))
        self.actionSelect_Mode = QAction(MainWindow)
        self.actionSelect_Mode.setObjectName("actionSelect_Mode")
        icon = QIcon(QIcon.fromTheme("camera-web"))
        self.actionSelect_Mode.setIcon(icon)
        self.actionSelect_Mode.setMenuRole(QAction.MenuRole.NoRole)
        self.actionRun = QAction(MainWindow)
        self.actionRun.setObjectName("actionRun")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaPlaybackStart))
        self.actionRun.setIcon(icon1)
        self.actionRun.setMenuRole(QAction.MenuRole.NoRole)
        self.actionStop = QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        icon2 = QIcon(QIcon.fromTheme("media-playback-stop"))
        self.actionStop.setIcon(icon2)
        self.actionStop.setMenuRole(QAction.MenuRole.NoRole)
        self.actionActionConfigureEmail = QAction(MainWindow)
        self.actionActionConfigureEmail.setObjectName("actionActionConfigureEmail")
        icon3 = QIcon(QIcon.fromTheme("emblem-mail"))
        self.actionActionConfigureEmail.setIcon(icon3)
        self.actionActionConfigureEmail.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSelectLocalCameras = QAction(MainWindow)
        self.actionSelectLocalCameras.setObjectName("actionSelectLocalCameras")
        icon4 = QIcon(QIcon.fromTheme("camera-video"))
        self.actionSelectLocalCameras.setIcon(icon4)
        self.actionSelectLocalCameras.setMenuRole(QAction.MenuRole.NoRole)
        self.actionConfigure_Ai_model = QAction(MainWindow)
        self.actionConfigure_Ai_model.setObjectName("actionConfigure_Ai_model")
        icon5 = QIcon()
        icon5.addFile(
            "./icons/icon-ai-24.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionConfigure_Ai_model.setIcon(icon5)
        self.actionConfigure_Ai_model.setMenuRole(QAction.MenuRole.NoRole)
        self.actionOpen_configuration_file = QAction(MainWindow)
        self.actionOpen_configuration_file.setObjectName(
            "actionOpen_configuration_file"
        )
        icon6 = QIcon(QIcon.fromTheme("document-open"))
        self.actionOpen_configuration_file.setIcon(icon6)
        self.actionOpen_configuration_file.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSave_configuration_as = QAction(MainWindow)
        self.actionSave_configuration_as.setObjectName("actionSave_configuration_as")
        icon7 = QIcon(QIcon.fromTheme("document-save-as"))
        self.actionSave_configuration_as.setIcon(icon7)
        self.actionSave_configuration_as.setMenuRole(QAction.MenuRole.NoRole)
        self.actionOpen_configuration_file_menu = QAction(MainWindow)
        self.actionOpen_configuration_file_menu.setObjectName(
            "actionOpen_configuration_file_menu"
        )
        self.actionOpen_configuration_file_menu.setIcon(icon6)
        self.actionSave_configuration_as_menu = QAction(MainWindow)
        self.actionSave_configuration_as_menu.setObjectName(
            "actionSave_configuration_as_menu"
        )
        self.actionSave_configuration_as_menu.setIcon(icon7)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon8 = QIcon(QIcon.fromTheme("dialog-question"))
        self.actionAbout.setIcon(icon8)
        self.actionLicense = QAction(MainWindow)
        self.actionLicense.setObjectName("actionLicense")
        self.actionSave_configuration = QAction(MainWindow)
        self.actionSave_configuration.setObjectName("actionSave_configuration")
        icon9 = QIcon(QIcon.fromTheme("document-save"))
        self.actionSave_configuration.setIcon(icon9)
        self.actionSave_configuration.setMenuRole(QAction.MenuRole.NoRole)
        self.actionSave_configuration_menu = QAction(MainWindow)
        self.actionSave_configuration_menu.setObjectName(
            "actionSave_configuration_menu"
        )
        self.actionSave_configuration_menu.setIcon(icon9)
        self.actionSave_configuration_menu.setMenuRole(QAction.MenuRole.NoRole)
        self.actionConfigure_FTP_Cameras = QAction(MainWindow)
        self.actionConfigure_FTP_Cameras.setObjectName("actionConfigure_FTP_Cameras")
        icon10 = QIcon(QIcon.fromTheme("system-file-manager"))
        self.actionConfigure_FTP_Cameras.setIcon(icon10)
        self.actionConfigure_FTP_Cameras.setMenuRole(QAction.MenuRole.NoRole)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_image = QLabel(self.centralwidget)
        self.label_image.setObjectName("label_image")
        self.label_image.setEnabled(True)
        self.label_image.setGeometry(QRect(10, 10, 800, 600))
        self.plainTextEdit_log = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_log.setObjectName("plainTextEdit_log")
        self.plainTextEdit_log.setGeometry(QRect(10, 620, 1121, 109))
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.plainTextEdit_log.sizePolicy().hasHeightForWidth()
        )
        self.plainTextEdit_log.setSizePolicy(sizePolicy1)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(830, 10, 301, 601))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_op_mode_title = QLabel(self.verticalLayoutWidget)
        self.label_op_mode_title.setObjectName("label_op_mode_title")
        font = QFont()
        font.setBold(True)
        self.label_op_mode_title.setFont(font)

        self.verticalLayout.addWidget(self.label_op_mode_title)

        self.label_op_mode = QLabel(self.verticalLayoutWidget)
        self.label_op_mode.setObjectName("label_op_mode")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.label_op_mode.sizePolicy().hasHeightForWidth()
        )
        self.label_op_mode.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_op_mode)

        self.label_last_detection_title = QLabel(self.verticalLayoutWidget)
        self.label_last_detection_title.setObjectName("label_last_detection_title")
        self.label_last_detection_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_detection_title)

        self.label_last_detection = QLabel(self.verticalLayoutWidget)
        self.label_last_detection.setObjectName("label_last_detection")
        sizePolicy2.setHeightForWidth(
            self.label_last_detection.sizePolicy().hasHeightForWidth()
        )
        self.label_last_detection.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_detection)

        self.label_last_classification_title = QLabel(self.verticalLayoutWidget)
        self.label_last_classification_title.setObjectName(
            "label_last_classification_title"
        )
        self.label_last_classification_title.setFont(font)

        self.verticalLayout.addWidget(self.label_last_classification_title)

        self.label_last_classification = QLabel(self.verticalLayoutWidget)
        self.label_last_classification.setObjectName("label_last_classification")
        sizePolicy2.setHeightForWidth(
            self.label_last_classification.sizePolicy().hasHeightForWidth()
        )
        self.label_last_classification.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.label_last_classification)

        self.label_classified_animal_title = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal_title.setObjectName(
            "label_classified_animal_title"
        )
        self.label_classified_animal_title.setFont(font)

        self.verticalLayout.addWidget(self.label_classified_animal_title)

        self.label_classified_animal = QLabel(self.verticalLayoutWidget)
        self.label_classified_animal.setObjectName("label_classified_animal")

        self.verticalLayout.addWidget(self.label_classified_animal)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.listWidget_en_cameras = QListWidget(self.verticalLayoutWidget)
        self.listWidget_en_cameras.setObjectName("listWidget_en_cameras")

        self.verticalLayout.addWidget(self.listWidget_en_cameras)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1150, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
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
        self.toolBar.addAction(self.actionSelectLocalCameras)
        self.toolBar.addAction(self.actionConfigure_FTP_Cameras)
        self.toolBar.addAction(self.actionActionConfigureEmail)
        self.toolBar.addAction(self.actionSelect_Mode)
        self.toolBar.addAction(self.actionConfigure_Ai_model)
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionStop)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate(
                "MainWindow",
                "Wild Animals Detection and Alert System (WADAS) [*]",
                None,
            )
        )
        self.actionSelect_Mode.setText(
            QCoreApplication.translate("MainWindow", "Select Mode", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSelect_Mode.setToolTip(
            QCoreApplication.translate("MainWindow", "Select operating mode", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionRun.setText(QCoreApplication.translate("MainWindow", "Run", None))
        # if QT_CONFIG(tooltip)
        self.actionRun.setToolTip(
            QCoreApplication.translate("MainWindow", "Run detection", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionStop.setText(QCoreApplication.translate("MainWindow", "Stop ", None))
        # if QT_CONFIG(tooltip)
        self.actionStop.setToolTip(
            QCoreApplication.translate("MainWindow", "Stop detection", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionActionConfigureEmail.setText(
            QCoreApplication.translate("MainWindow", "ActionConfigureEmail", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionActionConfigureEmail.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Configure Email notifications", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSelectLocalCameras.setText(
            QCoreApplication.translate("MainWindow", "selectLocalCameras", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSelectLocalCameras.setToolTip(
            QCoreApplication.translate("MainWindow", "Configure camera(s)", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionConfigure_Ai_model.setText(
            QCoreApplication.translate("MainWindow", "Configure Ai model", None)
        )
        self.actionOpen_configuration_file.setText(
            QCoreApplication.translate("MainWindow", "Open configuration file", None)
        )
        self.actionSave_configuration_as.setText(
            QCoreApplication.translate("MainWindow", "Save configuration as", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_configuration_as.setToolTip(
            QCoreApplication.translate("MainWindow", "Save configuration as ...", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionOpen_configuration_file_menu.setText(
            QCoreApplication.translate("MainWindow", "Open configuration file", None)
        )
        self.actionSave_configuration_as_menu.setText(
            QCoreApplication.translate("MainWindow", "Save configuration as ...", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_configuration_as_menu.setToolTip(
            QCoreApplication.translate("MainWindow", "Save configuration as ...", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionLicense.setText(
            QCoreApplication.translate("MainWindow", "License", None)
        )
        self.actionSave_configuration.setText(
            QCoreApplication.translate("MainWindow", "Save configuration", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_configuration.setToolTip(
            QCoreApplication.translate("MainWindow", "Save configuration", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSave_configuration_menu.setText(
            QCoreApplication.translate("MainWindow", "Save configuration", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_configuration_menu.setToolTip(
            QCoreApplication.translate("MainWindow", "Save configuration", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionConfigure_FTP_Cameras.setText(
            QCoreApplication.translate("MainWindow", "Configure FTP Cameras", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionConfigure_FTP_Cameras.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Configure FTP cameras and server", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_image.setText(
            QCoreApplication.translate("MainWindow", "Detecion viewer", None)
        )
        self.label_op_mode_title.setText(
            QCoreApplication.translate("MainWindow", "Operation mode:", None)
        )
        self.label_op_mode.setText("")
        self.label_last_detection_title.setText(
            QCoreApplication.translate("MainWindow", "Last detection:", None)
        )
        self.label_last_detection.setText("")
        self.label_last_classification_title.setText(
            QCoreApplication.translate("MainWindow", "Last classification:", None)
        )
        self.label_last_classification.setText("")
        self.label_classified_animal_title.setText(
            QCoreApplication.translate("MainWindow", "Classified animal(s):", None)
        )
        self.label_classified_animal.setText("")
        self.label.setText(
            QCoreApplication.translate("MainWindow", "Enabled Camera(s):", None)
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.toolBar.setWindowTitle(
            QCoreApplication.translate("MainWindow", "toolBar", None)
        )

    # retranslateUi
