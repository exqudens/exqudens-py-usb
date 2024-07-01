import logging
from typing import Callable

from exqudens.usb.pybind.client import Client as PyBindClient


class Client:
    """
    Client class.
    """
    __logger = logging.getLogger(".".join([__name__, __qualname__]))
    __pybind_client = None

    @classmethod
    def set_logger_level(cls, level: int = logging.DEBUG) -> None:
        try:
            cls.__logger.setLevel(level)
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    @classmethod
    def get_logger_name(cls):
        try:
            return cls.__logger.name
        except Exception as e:
            cls.__logger.error(e, exc_info=True)
            raise e

    def __init__(
            self,
            auto_init: bool = True,
            auto_close: bool = True
    ) -> None:
        try:
            self.__pybind_client = PyBindClient(
                auto_init,
                auto_close
            )
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def get_logger_id(self) -> str:
        try:
            return self.__pybind_client.get_logger_id()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def set_log_function(self, function: Callable[[str, int, str, str, int, str], None]) -> None:
        try:
            self.__pybind_client.set_log_function(function)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def is_set_log_function(self) -> bool:
        try:
            return self.__pybind_client.is_set_log_function()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def init(self) -> None:
        try:
            self.__pybind_client.init()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def is_initialized(self) -> bool:
        try:
            return self.__pybind_client.is_initialized()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def get_version(self) -> str:
        try:
            return self.__pybind_client.get_version()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def list_devices(self) -> list[dict[str, int]]:
        try:
            return self.__pybind_client.list_devices()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def to_string(self, value: dict[str, int]) -> str:
        try:
            return self.__pybind_client.to_string(value)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def open(self, device: dict[str, int], detach_kernel_driver_if_active: bool = True, claim_interface: bool = True) -> None:
        try:
            self.__pybind_client.open(device, detach_kernel_driver_if_active, claim_interface)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def is_open(self) -> bool:
        try:
            return self.__pybind_client.is_open()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def get_device(self) -> dict[str, int]:
        try:
            return self.__pybind_client.get_device()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def to_write_endpoint(self, value: int) -> int:
        try:
            return self.__pybind_client.to_write_endpoint(value)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def to_read_endpoint(self, value: int) -> int:
        try:
            return self.__pybind_client.to_read_endpoint(value)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def bulk_write(
            self,
            value: list[int],
            endpoint: int,
            timeout: int = 1000,
            auto_endpoint_direction: bool = True
    ) -> int:
        try:
            return self.__pybind_client.bulk_write(value, endpoint, timeout, auto_endpoint_direction)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def bulk_read(
            self,
            endpoint: int,
            timeout: int = 1000,
            size: int = 2147483647,
            auto_endpoint_direction: bool = True
    ) -> list[int]:
        try:
            return self.__pybind_client.bulk_read(endpoint, timeout, size, auto_endpoint_direction)
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def close(self) -> None:
        try:
            self.__pybind_client.close()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e

    def destroy(self) -> None:
        try:
            self.__pybind_client.destroy()
        except Exception as e:
            self.__logger.error(e, exc_info=True)
            raise e


Client.set_logger_level(logging.INFO)
