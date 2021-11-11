import sys
import os
import threading
import pickle
import sqlite3


class Message:
    def __init__(self, *args) -> None:
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


class Client:
    def __init__(self, *args) -> None:
        self.user = os.getlogin()
        open(os.getcwd() + "/data/inmes.pkl", "wb").close()
        open(os.getcwd() + "/data/outmes.pkl", "wb").close()
        self.infn = os.getcwd() + "/data/inmes.pkl"
        self.outfn = os.getcwd() + "/data/outmes.pkl"
        self.filetime = os.stat(self.infn).st_mtime
        self.mesbuf = list()
        self.mode = "standart"

    def writeMessage(self, mes: Message) -> None:
        adress = mes.adress
        try:
            with open(self.outfn, "wb") as fb:
                pickle.dump(mes, fb)
        except FileExistsError:
            print("File does not exists")
        except FileNotFoundError:
            print("File not found")
        finally:
            self.__sendMessage(self.outfn, adress)

    def __sendMessage(self, ofb: str, adress: str) -> None:
        res = os.system(
            f"scp {ofb} {adress}@localhost:/home/{adress}/Messenger/data/inmes.pkl")

    def fileUpdated(self, path: str) -> bool:
        if self.filetime != os.stat(path).st_mtime:
            self.filetime = os.stat(path).st_mtime
            return True
        return False

    def getingLoop(self) -> None:
        while True:
            if self.fileUpdated(self.infn):
                db = Database(os.getcwd() + "/data/database.db")
                with open(self.infn, "rb") as fb:
                    ex = pickle.load(fb)
                    db.addMessage(ex)
                    if self.mode == "standart":
                        self.mesbuf.append(ex)
                    elif self.mode == "chat":
                        print("{ex.author}: {ex}")
                db.closeConnection()
        self.getingLoop()

    def givingLoop(self) -> None:
        db = Database(os.getcwd() + "/data/database.db")
        while True:
            cmd = input(">>> ")
            if cmd == "help":
                print("send, check, chat, clear, exit")
            elif cmd == "send":
                sendto = input("Send to:\n")
                print("Content: ")
                content = sys.stdin.readlines()
                mes = Message(db.getLastMessageId("messages") +
                              1, self.user.name, sendto, content)
                db.addMessage(mes)
                self.writeMessage(mes)
            elif cmd == "check":
                for el in self.mesbuf:
                    print(f"Message from {el.author}:")
                    print(el)
                self.mesbuf.clear()
            elif "chat" == cmd.split()[0]:
                self.mode = "chat"
                args = cmd.split()
                data = db.getDialogContent(0)
                for i in range(1, len(data)):
                    if data[i][1] == self.user.name:
                        print(f"Вы: {data[i][3]}")
                    else:
                        print(f"{data[i][1]}: {data[i][3]}")
                    print("--------")
                while True:
                    print("Content: ")
                    content = sys.stdin.readlines()
                    mes = Message(db.getLastMessageId(0) + 1,
                                  self.user.name, args[1], content)
                    db.addMessage(mes)
                    self.writeMessage(mes)
            elif cmd == "clear":
                os.system("clear")
            self.mode = "standart"
        self.givingLoop()

    def main(self) -> None:
        thr1 = threading.Thread(target=self.getingLoop)
        thr2 = threading.Thread(target=self.givingLoop)
        thr1.start()
        thr2.start()
        thr1.join()
        thr2.join()


if __name__ == "__main__":
    client = Client()
    client.main()
