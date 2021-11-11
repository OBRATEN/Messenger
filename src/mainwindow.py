from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 781, 511))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ChatsList = QtWidgets.QListWidget(self.layoutWidget)
        self.ChatsList.setObjectName("ChatsList")
        self.verticalLayout_2.addWidget(self.ChatsList, 0, QtCore.Qt.AlignLeft)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AddFriend = QtWidgets.QPushButton(self.layoutWidget)
        self.AddFriend.setObjectName("AddFriend")
        self.horizontalLayout.addWidget(self.AddFriend)
        self.RemoveFriend = QtWidgets.QPushButton(self.layoutWidget)
        self.RemoveFriend.setObjectName("RemoveFriend")
        self.horizontalLayout.addWidget(self.RemoveFriend)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.DialogList = QtWidgets.QListWidget(self.layoutWidget)
        self.DialogList.setObjectName("DialogList")
        self.verticalLayout.addWidget(self.DialogList)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.MessageLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.MessageLine.setObjectName("MessageLine")
        self.horizontalLayout_2.addWidget(self.MessageLine)
        self.SendButton = QtWidgets.QPushButton(self.layoutWidget)
        self.SendButton.setObjectName("SendButton")
        self.horizontalLayout_2.addWidget(self.SendButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 0, 781, 24))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 34))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionEdit_config = QtWidgets.QAction(MainWindow)
        self.actionEdit_config.setObjectName("actionEdit_config")
        self.actionView_config = QtWidgets.QAction(MainWindow)
        self.actionView_config.setObjectName("actionView_config")
        self.actionView_directory = QtWidgets.QAction(MainWindow)
        self.actionView_directory.setObjectName("actionView_directory")
        self.actionView_database = QtWidgets.QAction(MainWindow)
        self.actionView_database.setObjectName("actionView_database")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionSelect_all_2 = QtWidgets.QAction(MainWindow)
        self.actionSelect_all_2.setObjectName("actionSelect_all_2")
        self.actionAdd_Remove = QtWidgets.QAction(MainWindow)
        self.actionAdd_Remove.setObjectName("actionAdd_Remove")
        self.actionChatbar = QtWidgets.QAction(MainWindow)
        self.actionChatbar.setObjectName("actionChatbar")
        self.actionDialogbar = QtWidgets.QAction(MainWindow)
        self.actionDialogbar.setObjectName("actionDialogbar")
        self.actionMessageLine = QtWidgets.QAction(MainWindow)
        self.actionMessageLine.setObjectName("actionMessageLine")
        self.actionPreferences = QtWidgets.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionFullscreen = QtWidgets.QAction(MainWindow)
        self.actionFullscreen.setObjectName("actionFullscreen")
        self.actionMinimize = QtWidgets.QAction(MainWindow)
        self.actionMinimize.setObjectName("actionMinimize")
        self.actionMaximize = QtWidgets.QAction(MainWindow)
        self.actionMaximize.setObjectName("actionMaximize")
        self.actionGet_help = QtWidgets.QAction(MainWindow)
        self.actionGet_help.setObjectName("actionGet_help")
        self.actionShow_normaly = QtWidgets.QAction(MainWindow)
        self.actionShow_normaly.setObjectName("actionShow_normaly")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionView_config)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionView_directory)
        self.menuFile.addAction(self.actionView_database)
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addSeparator()
        self.menuView.addAction(self.actionAdd_Remove)
        self.menuView.addAction(self.actionChatbar)
        self.menuView.addAction(self.actionDialogbar)
        self.menuView.addAction(self.actionMessageLine)
        self.menuView.addSeparator()
        self.menuWindow.addAction(self.actionFullscreen)
        self.menuWindow.addAction(self.actionMinimize)
        self.menuWindow.addAction(self.actionMaximize)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionShow_normaly)
        self.menuHelp.addAction(self.actionGet_help)
        self.menuHelp.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.AddFriend.setText(_translate("MainWindow", "Add"))
        self.RemoveFriend.setText(_translate("MainWindow", "Remove"))
        self.SendButton.setText(_translate("MainWindow", "Send"))
        self.label.setText(_translate("MainWindow", "Username: "))
        self.label_2.setText(_translate("MainWindow", "Address: "))
        self.label_3.setText(_translate("MainWindow", "Port: "))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionEdit_config.setText(_translate("MainWindow", "Edit config"))
        self.actionView_config.setText(_translate("MainWindow", "View config"))
        self.actionView_directory.setText(_translate("MainWindow",
                                                     "View directory"))
        self.actionView_database.setText(_translate("MainWindow",
                                                    "View database"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionCopy.setText(_translate("MainWindow", "Copy all"))
        self.actionSelect_all_2.setText(_translate("MainWindow", "Select all"))
        self.actionAdd_Remove.setText(_translate("MainWindow", "Add/Remove"))
        self.actionChatbar.setText(_translate("MainWindow", "Chatbar"))
        self.actionDialogbar.setText(_translate("MainWindow", "Dialogbar"))
        self.actionMessageLine.setText(_translate("MainWindow", "MessageLine"))
        self.actionPreferences.setText(_translate("MainWindow",
                                                  "Preferences..."))
        self.actionFullscreen.setText(_translate("MainWindow", "Fullscreen"))
        self.actionMinimize.setText(_translate("MainWindow", "Minimize"))
        self.actionMaximize.setText(_translate("MainWindow", "Maximize"))
        self.actionGet_help.setText(_translate("MainWindow", "Get help"))
        self.actionShow_normaly.setText(_translate("MainWindow",
                                                   "Show normaly"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))