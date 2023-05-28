import logging
from colorlog import ColoredFormatter
from functools import partial
import sys

class Write:
    log_levels = {
        'trace': { 'level': 5,  'color': 'cyan',       'terminate': False },
        'debug': { 'level': 10, 'color': 'blue',       'terminate': False },
        'info':  { 'level': 20, 'color': 'green',      'terminate': False },
        'warn':  { 'level': 30, 'color': 'yellow',     'terminate': False },
        'error': { 'level': 40, 'color': 'red',        'terminate': False },
        'fatal': { 'level': 50, 'color': 'thin_red',   'terminate': True  },
        'help':  { 'level': 60, 'color': 'purple',     'terminate': False },
    }

    def update_log_levels(self):
        for level_name, level_params in self.log_levels.items():
            logging.addLevelName(level_params['level'], level_name.upper())
        self.max_level_length = max(len(level) for level in self.log_levels)

    def setup_log_methods(self):
        for level, level_params in self.log_levels.items():
            setattr(self, level, partial(self._log, level, level_params.get('terminate', False)))

    def refresh_log(self):
        self.update_log_levels()
        self.logger = self._setup_logger(stream=self.stream)
        self.setup_log_methods()

    def __init__(self, use_colors=True, log_level='info', format_string='', date_format=None, stream=None):
        self.use_colors = use_colors
        self.log_level = log_level
        self.format_string = format_string
        self.date_format = date_format
        self.stream = stream
        self.refresh_log()

    def _setup_logger(self, stream=None):
        logger = logging.getLogger('write')
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        handler = logging.StreamHandler(stream)

        if self.format_string == '':
            if self.use_colors:
                if self.date_format is not None:
                    self.format_string = f"%(log_color)s%(asctime)s :: %(levelname)-{self.max_level_length}s :: %(reset)s%(white)s%(message)s"
                else:
                    self.format_string = f"%(log_color)s%(levelname)-{self.max_level_length}s :: %(reset)s%(white)s%(message)s"
            else:
                if self.date_format is not None:
                    self.format_string = f"%(asctime)s :: %(levelname)-{self.max_level_length}s :: %(message)s"
                else:
                    self.format_string = f"%(levelname)-{self.max_level_length}s :: %(message)s"

        if self.use_colors:
            formatter = ColoredFormatter(
                self.format_string,
                datefmt=self.date_format,
                log_colors={key.upper(): val['color'] for key, val in self.log_levels.items()},
            )
        else:
            formatter = ColoredFormatter(
                self.format_string,
                datefmt=self.date_format,
            )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.log_levels[self.log_level]['level'])

        return logger

    def _log(self, level, terminate, message, *args):
        self.logger.log(self.log_levels[level]['level'], message, *args)
        if terminate:
            sys.exit(1)
