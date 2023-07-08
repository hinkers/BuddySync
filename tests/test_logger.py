import logging

import pytest

from sync_buddy.logger import get_logger


@pytest.fixture
def logger_name():
    return 'test_logger'


class TestLogger:
    def test_get_logger_has_handlers(self, logger_name):
        logger = get_logger(logger_name)
        assert logger.hasHandlers()

    def test_get_logger_filehandler_level(self, logger_name):
        logger = get_logger(logger_name)
        filehandler = logger.handlers[0]
        assert filehandler.level == logging.DEBUG

    def test_get_logger_filehandler_formatter(self, logger_name):
        logger = get_logger(logger_name)
        filehandler = logger.handlers[0]
        assert isinstance(filehandler.formatter, logging.Formatter)

    def test_get_logger_streamhandler_level(self, logger_name):
        logger = get_logger(logger_name)
        streamhandler = logger.handlers[1]
        assert streamhandler.level == logging.INFO

    def test_get_logger_streamhandler_formatter(self, logger_name):
        logger = get_logger(logger_name)
        streamhandler = logger.handlers[1]
        assert isinstance(streamhandler.formatter, logging.Formatter)

    def test_get_logger_name(self, logger_name):
        logger = get_logger(logger_name)
        assert logger.name == logger_name

    def test_get_logger_return_type(self, logger_name):
        logger = get_logger(logger_name)
        assert isinstance(logger, logging.Logger)