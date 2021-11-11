#!/usr/bin/env python3

import sys
import os

import pickle
import time
import sqlite3
import subprocess
import pyperclip
import webbrowser

from PyQt5.QtWidgets import (QLabel, QListWidget, QPushButton, QDialog,
                             QMainWindow, QApplication, QListWidgetItem,
                             QFileDialog)
from PyQt5.QtCore import QThread, QFile, QTextStream, Qt

from typing import Union, NoReturn
from functools import partial

from dialog import Ui_Dialog
from mainwindow import Ui_MainWindow


class MessageChecker(QThread):
    def __init__(self, parent=None) -> None:
        super(QThread, self).__init__()
        self.parent = parent
        self.timer = 0

    def __del__(self) -> None:
        self.wait()

    def fileUpdated(self) -> bool:
        if self.parent.filetime != os.stat(self.parent.infn).st_mtime:
            self.parent.filetime = os.stat(self.parent.infn).st_mtime
            self.timer = time.time()
            return True
        return False

    def run(self) -> NoReturn:
        while True:
            if self.fileUpdated():
                with open(self.parent.infn, "rb") as fb:
                    ex = pickle.load(fb)
                    self.parent.db.addMessage(ex.author, ex)
                    item = QListWidgetItem(f"{ex.author}: {ex.content}")
                    item.setTextAlignment(Qt.AlignLeft)
                    self.parent.DialogList.addItem(item)
                    self.parent.DialogList.scrollToBottom()
                print(f"Message send: {time.time() - self.timer} sec")


class Message:
    def __init__(self, *args: list[int, str, list[str]]) -> None:
        self.id = int(args[0])
        self.author = args[1]
        self.adress = args[2]
        self.content = "".join(args[3])

    def __str__(self) -> str:
        return self.content


class Database:
    def __init__(self, path: str) -> None:
        self.path = path
        if self.checkForDb():
            self.db = sqlite3.connect(self.path, check_same_thread=False)
            self.cur = self.db.cursor()
        else:
            print(self.__class__, "No database file exists!")
            sys.exit(0)

    def checkForDb(self) -> bool:
        if os.path.exists(self.path):
            return True
        return False

    def getAllIds(self, table: str) -> tuple[int]:
        try:
            return self.cur.execute(f"SELECT id FROM {table};").fetchall()
        except sqlite3.OperationalError:
            print(self.__class__, f"No such table: {table}")

    def getLastMessageId(self, table: str) -> int:
        try:
            return self.cur.execute(f"SELECT MAX(id) \
FROM '{table}';").fetchone()[0]
        except sqlite3.OperationalError:
            print(self.__class__, f"No such table: {table}")
            return -2

    def getMessage(self, table: str, id: int) -> Union[str, NoReturn]:
        try:
            return self.cur.execute(f"SELECT * FROM {table} \
WHERE id = {id}").fetchone()[0]
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't get message:", e)

    def getAddress(self, table: str) -> Union[str, NoReturn]:
        try:
            return self.cur.execute(f"SELECT ip FROM '{table}';").fetchone()[0]
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't get user address:", e)

    def getPort(self, table: str) -> Union[str, NoReturn]:
        try:
            return self.cur.execute(f"SELECT port FROM \
'{table}';").fetchone()[0]
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't get port:", e)

    def getDialogContent(self, table: str) -> Union[list[str], NoReturn]:
        if table is None:
            return []
        try:
            return self.cur.execute(f"SELECT * FROM '{table}'").fetchall()
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't get dialog content:", e)

    def getChats(self) -> Union[list[str], NoReturn]:
        try:
            return list(self.cur.execute("SELECT name FROM sqlite_master \
WHERE type='table';").fetchall())
        except sqlite3.OperationalError as e:
            print(self.__class__, "Cant get chats list:", e)

    def addMessage(self, table: str, mes: Message) -> NoReturn:
        try:
            toAdd = f"INSERT INTO '{table}' \
VALUES (?, ?, ?, ?, ?, ?);"
            data = (mes.id, mes.author, mes.adress, mes.content,
                    self.getAddress(table), self.getPort(table))
            self.cur.execute(toAdd, data)
            self.db.commit()
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't add message to chat:", e)

    def addDialog(self, name: str, addr: str, port: str) -> NoReturn:
        try:
            self.cur.execute(f"CREATE TABLE '{name}' \
(id INT NOT NULL, \
author TEXT NOT NULL, \
address TEXT NOT NULL, \
content TEXT NOT NULL, \
ip TEXT DEFAULT localhost, \
port TEXT DEFAULT (22));")
            self.cur.execute(f"INSERT INTO '{name}' \
VALUES (-1, 0, 0, 0, '{addr}', '{port}');")
            self.db.commit()
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't add dialog table to database:", e)

    def removeDialog(self, name: str) -> NoReturn:
        try:
            self.cur.execute(f"DROP TABLE {name}")
        except sqlite3.OperationalError as e:
            print(self.__class__, "Can't drop table:", e)

    def closeConnection(self) -> NoReturn:
        self.cur.close()
        self.db.close()


class AddUserDialog(QDialog, Ui_Dialog):
    def __init__(self, perent=None) -> None:
        super().__init__()
        self.setupUi(self)
        self.withAuth = False
        self.useKeys.stateChanged.connect(self.addAuth)

    def addAuth(self) -> NoReturn:
        self.passwordLine.setReadOnly(self.withAuth)
        self.withAuth = not self.withAuth

    def getVals(self) -> tuple[str]:
        if self.withAuth:
            res = os.system(f"""sshpass -p "{self.passwordLine.text()}" \
ssh-copy-id -f -p {self.portLine.text()} \
{self.nameLine.text()}@{self.addressLine.text()}""")
            if res:
                print(self.__class__, "Auth is not completed!")
        return (self.nameLine.text(),
                self.addressLine.text(), self.portLine.text())


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, curdir: str) -> None:
        super().__init__()
        self.setupUi(self)
        self.curdir = curdir
        self.initVars()
        self.initFns()
        self.relogDialog()
        self.messagecheker = MessageChecker(self)
        self.messagecheker.start()
        self.label.setText(self.label.text() + self.user)
        self.label_2.setText(self.label_2.text() + subprocess.getoutput("ip address | grep 'inet 19'").split()[1])
        self.label_3.setText(self.label_3.text() + subprocess.getoutput("grep Port /etc/ssh/sshd_config").split()[1])

    def initFns(self) -> NoReturn:
        self.ChatsList.currentItemChanged.connect(self.changeItem)
        self.SendButton.clicked.connect(self.writeMessage)
        self.SendButton.setAutoDefault(True)
        self.MessageLine.returnPressed.connect(self.writeMessage)
        self.AddFriend.clicked.connect(self.addFriend)
        self.RemoveFriend.clicked.connect(self.removeFriend)
        self.actionView_config.triggered.connect(partial(self.viewDir, f"{self.curdir}/data/"))
        self.actionView_directory.triggered.connect(partial(self.viewDir, os.curdir))
        self.actionView_database.triggered.connect(partial(self.viewDir, f"{self.curdir}/data/"))
        self.actionCopy.triggered.connect(lambda: pyperclip.copy(self.MessageLine.text()))
        self.actionPaste.triggered.connect(partial(self.MessageLine.setText, self.MessageLine.text() + pyperclip.paste()))
        self.actionFullscreen.triggered.connect(self.showFullScreen)
        self.actionMinimize.triggered.connect(self.showMinimized)
        self.actionMaximize.triggered.connect(self.showMaximized)
        self.actionShow_normaly.triggered.connect(self.showNormal)
        self.actionAdd_Remove.triggered.connect(self.hideButtons)
        self.actionChatbar.triggered.connect(self.hideChats)
        self.actionDialogbar.triggered.connect(self.hideDial)
        self.actionMessageLine.triggered.connect(self.hideMessageBar)
        self.actionGet_help.triggered.connect(self.getHelp)
        self.actionSave.triggered.connect(self.saveChat)
        self.actionOpen.triggered.connect(self.openChat)

    def initVars(self) -> NoReturn:
        self.db = Database(f"{self.curdir}/data/database.db")
        self.user = os.getlogin()
        self.outfn = f"{self.curdir}/data/outmes.pkl"
        self.infn = f"{self.curdir}/data/inmes.pkl"
        self.filetime = os.stat(self.infn).st_mtime
        self.listOfDials = []
        self.chats = self.db.getChats()
        for el in self.chats:
            self.ChatsList.addItem(el[0])
        self.curChat = self.ChatsList.currentItem()

    def getHelp(self) -> NoReturn:
        webbrowser.open("https://github.com/OBRATEN/Messenger")

    def saveChat(self) -> None:
        if self.curChat:
            fname = QFileDialog.getSaveFileName(self,
                                                "Save dialog", self.curdir)[0]
            if not fname:
                return
            with open(fname, "w") as f:
                data = self.db.getDialogContent(self.curChat)
                for el in data:
                    if el[2] == self.user:
                        f.write('|'.join(list(map(str, el))) + "\n")

    def openChat(self) -> None:
        fname = QFileDialog.getOpenFileName(self,
                                            "Open dialog", self.curdir)[0]
        if not fname:
            return
        with open(fname, "r") as f:
            data = [el.strip().split('|') for el in f.readlines()]
            for el in data:
                if el[2] == self.user or el[1] == self.user:
                    ids = [el[0] for el in self.db.getAllIds(el[2])]
                    print(ids)
                    el[0] = int(el[0])
                    if el[0] not in ids:
                        el[-1] = int(el[-1])
                        mes = Message(el[0], el[1], el[2], el[3], el[4], el[5])
                        self.db.addMessage(el[1], mes)
            self.relogDialog()

    def hideMessageBar(self) -> NoReturn:
        if self.MessageLine.visibleRegion().isEmpty():
            self.MessageLine.show()
            self.SendButton.show()
        else:
            self.MessageLine.hide()
            self.SendButton.hide()

    def hideDial(self) -> NoReturn:
        if self.DialogList.visibleRegion().isEmpty():
            self.DialogList.show()
            self.MessageLine.show()
            self.SendButton.show()
        else:
            self.DialogList.hide()
            self.MessageLine.hide()
            self.SendButton.hide()

    def hideButtons(self) -> NoReturn:
        if self.AddFriend.visibleRegion().isEmpty():
            self.AddFriend.show()
            self.RemoveFriend.show()
        else:
            self.AddFriend.hide()
            self.RemoveFriend.hide()

    def hideChats(self) -> NoReturn:
        if self.ChatsList.visibleRegion().isEmpty():
            self.ChatsList.show()
            self.AddFriend.show()
            self.RemoveFriend.show()
        else:
            self.ChatsList.hide()
            self.AddFriend.hide()
            self.RemoveFriend.hide()

    def viewDir(self, path: str) -> NoReturn:
        subprocess.check_call(["xdg-open", path])

    def removeFriend(self) -> None:
        torem = self.ChatsList.currentItem()
        try:
            self.ChatsList.takeItem(self.ChatsList.row(torem))
            self.db.removeDialog(torem.text())
            self.DialogList.clear()
            self.curChat = ''
        except AttributeError:
            return

    def addFriend(self) -> NoReturn:
        dial = AddUserDialog(self)
        if dial.exec():
            data = dial.getVals()
            self.db.addDialog(data[0], data[1], data[2])
            self.chats = self.db.getChats()
            self.ChatsList.clear()
            for el in self.chats:
                self.ChatsList.addItem(el[0])

    def relogDialog(self) -> None:
        self.DialogList.clear()
        toadd = self.db.getDialogContent(self.curChat)
        if type(toadd) is bool:
            return
        for el in toadd:
            if el[0] != -1:
                item = QListWidgetItem(f"{el[1]}: {el[3]}")
                print(el[1] == self.user)
                if el[1] == self.user:
                    item.setTextAlignment(Qt.AlignRight)
                else:
                    item.setTextAlignment(Qt.AlignLeft)
                self.DialogList.addItem(item)
        self.DialogList.scrollToBottom()

    def changeItem(self) -> None:
        try:
            self.curChat = self.ChatsList.currentItem().text()
            self.relogDialog()
        except AttributeError:
            return
        except TypeError:
            return

    def writeMessage(self) -> None:
        content = self.MessageLine.text()
        if not content:
            return
        nid = self.db.getLastMessageId(self.curChat)
        if nid == -2:
            return
        mes = Message(nid + 1, self.user, self.curChat, content)
        self.db.addMessage(self.curChat, mes)
        item = QListWidgetItem(f"{mes.author}: {mes.content}")
        item.setTextAlignment(Qt.AlignRight)
        self.DialogList.addItem(item)
        self.DialogList.scrollToBottom()
        try:
            with open(self.outfn, "wb") as fb:
                pickle.dump(mes, fb)
        except FileExistsError:
            print(self.__class__, "File does not exists")
        except FileNotFoundError:
            print(self.__class__, "File not found")
        finally:
            self.__sendMessage()
            self.MessageLine.setText('')

    def __sendMessage(self) -> NoReturn:
        res = os.system(f"scp -P {self.db.getPort(self.curChat)} \
{self.outfn} {self.curChat}@\
{self.db.getAddress(self.curChat)}:/home/{self.curChat}\
/Messenger/data/inmes.pkl")
        if res:
            print(self.__class__, "Can't send a message!")


def getCurDir() -> str:
    res = os.path.dirname(os.path.abspath(__file__)).split('/')
    return '/'.join(res[:res.index("src")])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file = QFile(f"{getCurDir()}/src/stylesheet.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    wind = Window(getCurDir())
    wind.show()
    sys.exit(app.exec())
