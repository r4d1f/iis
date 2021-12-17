from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Union
import sqlite3
import pymysql
from Observer import ConcreteSubject
import os


class Context:
    def __init__(self, strategy: Strategy, observers: ConcreteSubject) -> None:
        self.observers = observers
        self._strategy = strategy

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def connect_to_database(self) -> Union[pymysql.cursors.Cursor, sqlite3.Cursor]:
        self.observers.notify(f"Подключение к базе данных из процесса: {os.getpid()}")
        db_cursor = self._strategy.connect()
        return db_cursor

    def disconnect(self):
        self.observers.notify(f"Отключение от базы данных из процесса: {os.getpid()}")
        del self._strategy


class Strategy(ABC):
    connection: Any
    cursor: Union[pymysql.cursors.Cursor, sqlite3.Cursor]

    @abstractmethod
    def connect(self):
        pass


class ConnectToMySQL(Strategy):

    def __init__(self, connect_str: str):
        self.host, self.user, self.password, self.db = connect_str.split(":")

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def connect(self):
        self.connection = pymysql.connect(host=self.host, user=self.user,
                                          passwd=self.password, db=self.db)
        self.cursor = self.connection.cursor()
        return self.cursor


class ConnectToSQLite(Strategy):
    def __init__(self, connect_str: str):
        self.path = connect_str.split(":")[0]

    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def connect(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        return self.cursor

