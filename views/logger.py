import logging

def setup_logger(name, log_file, level=logging.ERROR):
    formatter = logging.Formatter(' %(asctime)s [%(levelname)s] %(message)s  %(name)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    

    return logger

app_logger = setup_logger('app_logger', 'logs/app.log', level=logging.INFO)
error_logger = setup_logger('error_logger', 'logs/error.log', level=logging.ERROR)
warn_logger = setup_logger('warn_logger', 'logs/warn.log', level=logging.WARNING)




