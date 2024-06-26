import os
import logging
from logging import handlers
from pathlib import Path


class Log:

    def __init__(self):
        self.log_file = None
        self.logger = None
        self.create_log_dir()
        self.config()

    def create_log_dir(self):
        """Criar o diretório de log caso não houver e configurar o arquivo de
        log
        """
        dir_log = Path(Path(os.getcwd()), 'logs').__str__()
        try:
            if Path(dir_log).exists() is False:
                os.mkdir(dir_log)
            self.log_file = Path(dir_log, 'logs.txt').__str__()
        except IOError:
            self.error('Não foi possível criar o diretório de log.')

    def config(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - '
                                      '%(message)s')
        handler = logging.handlers.RotatingFileHandler(
            self.log_file, maxBytes=1024 * 1024 * 5, backupCount=5,
            encoding='utf-8')

        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        self.logger = logger

    def error(self, message: str = '') -> None:
        self.logger.error(message)

    def info(self, message: str = '') -> None:
        self.logger.info(message)


log = Log()

