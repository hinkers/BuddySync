import logging
from datetime import datetime

def get_logger(name):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():    
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter("%(asctime)s %(name)-9s %(levelname)s %(message)s")

        filehandler = logging.FileHandler(f'SyncBuddy_{datetime.today().strftime("%d-%b-%Y")}.log')
        filehandler.setLevel(logging.DEBUG)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        streamhandler = logging.StreamHandler()
        streamhandler.setLevel(logging.INFO)
        streamhandler.setFormatter(formatter)
        logger.addHandler(streamhandler)

    return logger
