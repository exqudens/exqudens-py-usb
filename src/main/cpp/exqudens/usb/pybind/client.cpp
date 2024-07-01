#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

#include <exqudens/usb/Client.hpp>

PYBIND11_MODULE(client, object) {
    pybind11::class_<exqudens::usb::Client>(object, "Client")
        .def(
            pybind11::init<
                const bool&,
                const bool&
            >()
        )
        .def(
            "get_logger_id",
            &exqudens::usb::Client::getLoggerId
        )
        .def(
            "set_log_function",
            &exqudens::usb::Client::setLogFunction
        )
        .def(
            "is_set_log_function",
            &exqudens::usb::Client::isSetLogFunction
        )
        .def(
            "init",
            &exqudens::usb::Client::init
        )
        .def(
            "is_initialized",
            &exqudens::usb::Client::isInitialized
        )
        .def(
            "get_version",
            &exqudens::usb::Client::getVersion
        )
        .def(
            "list_devices",
            &exqudens::usb::Client::listDevices
        )
        .def(
            "to_string",
            &exqudens::usb::Client::toString
        )
        .def(
            "open",
            pybind11::overload_cast<
                const std::map<std::string, unsigned short>&,
                const bool&,
                const bool&
            >(&exqudens::usb::Client::open)
        )
        .def(
            "is_open",
            &exqudens::usb::Client::isOpen
        )
        .def(
            "get_device",
            &exqudens::usb::Client::getDevice
        )
        .def(
            "to_write_endpoint",
            &exqudens::usb::Client::toWriteEndpoint
        )
        .def(
            "to_read_endpoint",
            &exqudens::usb::Client::toReadEndpoint
        )
        .def(
            "bulk_write",
            [](
                exqudens::usb::Client* self,
                const std::vector<unsigned char>& value,
                const unsigned char& endpoint,
                const unsigned int& timeout,
                const bool& autoEndpointDirection
            ) {
                std::vector<unsigned char> bytes(value.begin(), value.end());
                return self->bulkWrite(bytes, endpoint, timeout, autoEndpointDirection);
            }
        )
        .def(
            "bulk_read",
            [](
                exqudens::usb::Client* self,
                const unsigned char& endpoint,
                const unsigned int& timeout,
                const int& size,
                const bool& autoEndpointDirection
            ) {
                std::vector<unsigned char> bytes = self->bulkRead(endpoint, timeout, size, autoEndpointDirection);
                std::vector<int> result(bytes.begin(), bytes.end());
                return result;
            }
        )
        .def(
            "close",
            &exqudens::usb::Client::close
        )
        .def(
            "destroy",
            &exqudens::usb::Client::destroy
        );
}
