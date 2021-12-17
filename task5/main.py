from __future__ import annotations
from strategy import Context, ConnectToMySQL, ConnectToSQLite
from Observer import ConcreteSubject, FileObserver, ConsoleObserver


if __name__ == "__main__":
    subject = ConcreteSubject()
    subject.attach(FileObserver())
    subject.attach(ConsoleObserver())

    context = Context(ConnectToMySQL("127.0.0.1:root:root:iis"), subject)
    cursor = context.connect_to_database()
    cursor.execute("SELECT * FROM data_frame")
    print(cursor.fetchall())
    context.disconnect()

    context.strategy = ConnectToSQLite("sqlite.db")
    print("Connect to SQLite")
    cursor = context.connect_to_database()
    cursor.execute("SELECT * FROM data_frame")
    print(cursor.fetchall())
    context.disconnect()
