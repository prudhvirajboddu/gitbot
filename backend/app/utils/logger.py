import logging
from logging.config import dictConfig

from ..config import settings


def configure_logging():
    log_level = settings.LOG_LEVEL.upper()
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'level': log_level,
            'handlers': ['console'],
        },
    }
    dictConfig(config)