import logging.config

from exqudens.usb.client import Client


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
                    f"{Client.get_logger_name()}": {'level': logging.getLevelName(logging.CRITICAL)},
                    f"{cls.__logger.name}": {'level': logging.getLevelName(logging.INFO)}
                }
            })
        except Exception as e:
            cls.__logger.info(e, exc_info=True)
            raise e

    def test_1(self):
        try:
            client = Client()
            self.__logger.info(f"client: {client is not None}")

            assert client is not None

            device = {}
            devices = client.list_devices()
            for d in devices:
                self.__logger.info(f"{client.to_string(d)}")
                if d["vendor"] == 1155 and d["product"] == 22337:
                    device = d
                    break
            self.__logger.info(f"device: {device}")

            assert len(device) == 5

            client.open(device)
            self.__logger.info(f"client.is_open: {client.is_open()}")

            assert client.is_open()

            data_bytes: list[int] = []
            last_exception = None
            try:
                data_bytes = client.bulk_read(endpoint=1)
            except Exception as exception:
                cause = exception
                while cause is not None:
                    last_exception = str(cause)
                    cause = cause.__cause__
            self.__logger.info(f"last_exception: '{last_exception}'")
            size = len(data_bytes)
            self.__logger.info(f"size: {size}")

            assert size == 0
            assert last_exception.endswith("libusbErrorName: 'LIBUSB_ERROR_TIMEOUT'")

            data = "hi test"
            data_bytes = list(data.encode())
            size = client.bulk_write(value=data_bytes, endpoint=1)
            self.__logger.info(f"size: {size}")

            assert size == 7

            data_bytes = client.bulk_read(endpoint=1, size=7)
            data = bytes(data_bytes).decode()
            self.__logger.info(f"data: '{data}'")

            assert data == "HI TEST"

            data_bytes: list[int] = []
            last_exception = None
            try:
                data_bytes = client.bulk_read(endpoint=1)
            except Exception as exception:
                cause = exception
                while cause is not None:
                    last_exception = str(cause)
                    cause = cause.__cause__
            self.__logger.info(f"last_exception: '{last_exception}'")
            size = len(data_bytes)
            self.__logger.info(f"size: {size}")

            assert size == 0
            assert last_exception.endswith("libusbErrorName: 'LIBUSB_ERROR_TIMEOUT'")

            client.close()
            self.__logger.info(f"client.is_open: {client.is_open()}")

            assert not client.is_open()
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

    def __causes(self, result: list[Exception] = [], exception: Exception = None) -> list[Exception]:
        try:
            if exception is not None:
                result.append(exception)
                self.__causes(result=result, exception=exception.__cause__)
            return result
        except Exception as e:
            self.__logger.info(e, exc_info=True)
            raise e
