from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """
        Присоединяет наблюдателя к издателю.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """
        Отсоединяет наблюдателя от издателя.
        """
        pass

    @abstractmethod
    def notify(self, msg) -> None:
        """
        Уведомляет всех наблюдателей о событии.
        """
        pass


class ConcreteSubject(Subject):
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, msg: str) -> None:
        """
        Запуск обновления в каждом подписчике.
        """
        msg = "[" + str(datetime.now()) + "]: " + msg
        for observer in self._observers:
            observer.update(msg)


class Observer(ABC):
    """
    Интерфейс Наблюдателя объявляет метод уведомления, который издатели
    используют для оповещения своих подписчиков.
    """

    @abstractmethod
    def update(self, msg: str) -> None:
        """
        Получить обновление от субъекта.
        """
        pass


class FileObserver(Observer):
    def update(self, msg) -> None:
        with open("./log.log", "a") as f:
            f.write(msg.rstrip("\n") + "\n")


class ConsoleObserver(Observer):
    def update(self, msg) -> None:
        print(msg)


if __name__ == "__main__":
    subject = ConcreteSubject()

    observer_a = FileObserver()
    subject.attach(observer_a)

    observer_b = ConsoleObserver()
    subject.attach(observer_b)
