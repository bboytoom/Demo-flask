from datetime import datetime

CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
            }
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
            },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': 'logs/' + datetime.now().strftime('flask-%Y-%m-%d.log'),
            'maxBytes': 1024 ** 2,
            'backupCount': 10,
            'delay': 'True'
            }
        },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file'],
        'propagate': False
        }
    }
