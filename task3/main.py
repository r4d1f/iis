from Singletone import MyLogger


def bar_def():
    logger = MyLogger().get_logger()
    try:
        a = 1/0
    except ZeroDivisionError:
        logger.error("Деление на ноль!")


def foo_def():
    logger_obj = MyLogger()
    logger = logger_obj.get_logger()
    logger.info("Лог из функции 2")


def main():
    logger_obj1 = MyLogger()
    logger_obj2 = MyLogger()
    logger = logger_obj1.get_logger()
    logger.debug(f"Object 1: {logger_obj1}\tObject 2: {logger_obj2}")
    logger.info("Лог из функции 1")
    foo_def()
    bar_def()


if __name__ == "__main__":
    main()
