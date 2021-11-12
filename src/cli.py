import sys
import os
import threading
import pickle
import sqlite3

from typing import Union, NoReturn


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
        self.db = Database(os.getcwd() + "/data/database.db")

    def writeMessage(self, mes: Message) -> None:
        try:
            with open(self.outfn, "wb") as fb:
                pickle.dump(mes, fb)
        except FileExistsError:
            print("File does not exists")
        except FileNotFoundError:
            print("File not found")
        finally:
            self.__sendMessage(self.outfn, mes)

    def __sendMessage(self, ofb: str, mes: Message) -> None:
        res = os.system(
            f"scp -P {self.db.getPort(mes.adress)} {ofb} \
{mes.adress}@{self.db.getAddress(mes.adress)}\
:/home/{mes.adress}/Messenger/data/inmes.pkl")
        if res:
            print("Unable to send message!")

    def fileUpdated(self, path: str) -> bool:
        if self.filetime != os.stat(path).st_mtime:
            self.filetime = os.stat(path).st_mtime
            return True
        return False

    def getingLoop(self) -> None:
        while True:
            if self.fileUpdated(self.infn):
                with open(self.infn, "rb") as fb:
                    ex = pickle.load(fb)
                    self.db.addMessage(ex.author, ex)
                    if self.mode == "standart":
                        self.mesbuf.append(ex)
                    elif self.mode == "chat":
                        print("{ex.author}: {ex}")
        self.getingLoop()

    def givingLoop(self) -> None:
        while True:
            cmd = input(">>> ")
            if cmd == "help":
                print("add    | to add user to database")
                print("remove | to remove user from database")
                print("send   | to send a message to someone")
                print("check  | to see unchecked messages")
                print("hist   | to see chat history")
                print("users  | to see all users")
                print("clear  | to clear terminal output")
            elif cmd == "send":
                sendto = input("Send to:\n")
                print("Content: ")
                content = sys.stdin.readlines()
                mes = Message(self.db.getLastMessageId(sendto) + 1,
                              self.user, sendto, content)
                self.db.addMessage(sendto, mes)
                self.writeMessage(mes)
            elif cmd == "add":
                name = input("Username: ")
                adr = input("Adress:    ")
                port = input("Port:     ")
                self.db.addDialog(name, adr, port)
            elif cmd == "hist":
                data = self.db.getDialogContent(input("User: "))
                for el in data:
                    print(f"{el[1]}: {el[3]}")
            elif cmd == "users":
                data = self.db.getChats()
                for el in data:
                    print(el[0])
            elif cmd == "remove":
                self.db.removeDialog(input("User: "))
            elif cmd == "check":
                for el in self.mesbuf:
                    print(f"Message from {el.author}:")
                    print(el)
                self.mesbuf.clear()
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
