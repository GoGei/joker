import os
import json
from loguru import logger
from django.conf import settings as dj_settings

from core.Utils.singleton import Singleton


class Logger(metaclass=Singleton):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    JSON = 'json'
    LOG = 'log'

    default_settings = {
        'path': os.path.join(dj_settings.BASE_DIR, 'logger/'),
        'name': 'default_user_activity',
        'extension': LOG,
        'format': '{time} {level} {message}',
        'level': INFO,
        'rotation': None,
        'compression': None,
        'serialize': False,
    }

    def __init__(self, path='', name='', extension='', logger_format='', level='', rotation='',
                 compression='', serialize=False):
        settings = self.default_settings.copy()
        provided = dj_settings.LOGURU_CONFIGS.copy()
        settings.update(provided)
        self.path = path or settings.get('path')
        self.name = name or settings.get('name')
        self.extension = extension or settings.get('extension')
        self.file_name = f'{self.path}{self.name}.{self.extension}'

        self.format = logger_format or settings.get('format')
        self.level = level or settings.get('level')
        self.rotation = rotation or settings.get('rotation')
        self.compression = compression or settings.get('compression')
        self.serialize = serialize or settings.get('serialize')

        self.args = (self.file_name,)
        self.kwargs = {
            'format': self.format,
            'level': self.level,
            'rotation': self.rotation,
            'compression': self.compression,
            'serialize': self.serialize
        }
        self.logger = logger
        self.logger.add(*self.args, **self.kwargs)

    def debug(self, message, *args, **kwargs):
        data = self.prepare_logger_data(message, *args, **kwargs)
        self.logger.debug(*data)

    def info(self, message, *args, **kwargs):
        data = self.prepare_logger_data(message, *args, **kwargs)
        self.logger.info(*data)

    def warning(self, message, *args, **kwargs):
        data = self.prepare_logger_data(message, *args, **kwargs)
        self.logger.warning(*data)

    def error(self, message, *args, **kwargs):
        data = self.prepare_logger_data(message, *args, **kwargs)
        self.logger.error(*data)

    def critical(self, message, *args, **kwargs):
        data = self.prepare_logger_data(message, *args, **kwargs)
        self.logger.critical(*data)

    def prepare_logger_data(self, message, *args, **kwargs):
        args = self.args + args
        init_kwargs = self.kwargs.copy()
        init_kwargs.update(kwargs)
        if self.extension == self.JSON:
            message = json.dumps(message)
        return message, args, kwargs


log = Logger()
