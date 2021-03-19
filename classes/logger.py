import logging


class Logger(logging.Logger):

    __FORMAT = {
        'fmt': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }

    def __init__(self, name: str, level: str, write_file: bool = False, level_file: str = 'INFO', formatter: dict = __FORMAT):

        super().__init__(name)

        _format = logging.Formatter(**formatter)
        self.setLevel(getattr(logging, level))
        self.handlers = []

        handler = logging.StreamHandler()
        handler.setFormatter(_format)
        self.addHandler(handler)

        if write_file:
            file_log = logging.FileHandler("{}.log".format(name))
            file_log.setLevel(level_file)
            file_log.setFormatter(_format)
            self.addHandler(file_log)

