import logging.config


class TestExqudensUsbClient:
    """
    TestExqudensUsbClient class.
    """
    __logger = logging.getLogger(".".join([__name__, __qualname__]))

    @classmethod
    def setup_class(cls):
        """
        Setup class.
        """
        try:
            logging.config.dictConfig({
                'version': 1,
                'incremental': True,
                'loggers': {
                    f"exqudens.usb.Client": {'level': logging.getLevelName(logging.DEBUG)},
                    #f"{Serial.get_logger_name()}": {'level': logging.getLevelName(logging.DEBUG)},
                    f"{cls.__logger.name}": {'level': logging.getLevelName(logging.INFO)}
                }
            })
        except Exception as e:
            cls.__logger.info(e, exc_info=True)
            raise e

    def test_1(self):
        try:
            self.__logger.info(f"version: '{123}'")
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e

    def __cpp_log(self, file: str, line: int, function: str, id: str, level: int, message: str) -> None:
        try:
            if level == 1:
                logging.getLogger(id).critical(message)
            elif level == 2:
                logging.getLogger(id).error(message)
            elif level == 3:
                logging.getLogger(id).warn(message)
            elif level == 4:
                logging.getLogger(id).info(message)
            elif level == 5:
                logging.getLogger(id).debug(message)
            elif level == 6:
                logging.getLogger(id).info(message)
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e
