import logging
from pathlib import Path
from conans import ConanFile
from conans.util.files import save


required_conan_version = ">=1.43.0"


class ConanConfiguration(ConanFile):
    settings = "arch", "os", "compiler", "build_type"
    options = {"interface": [True, False], "shared": [True, False]}
    default_options = {"interface": False, "shared": True}
    generators = "cmake_find_package"

    def requirements(self):
        try:
            self.requires('exqudens-cpp-usb/1.0.0')
            self.requires("pybind11/2.10.1")
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e

    def configure(self):
        try:
            self.options["exqudens-cpp-usb"].shared = self.options.shared
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e

    def generate(self):
        try:
            filename = 'conan-packages.cmake'
            content = ''

            content += 'set("${PROJECT_NAME}_CONAN_PACKAGE_NAMES"\n'
            for dep_name in self.deps_cpp_info.deps:
                content += '    "' + dep_name + '"' + '\n'
            content += ')\n'

            content += 'set("${PROJECT_NAME}_CMAKE_PACKAGE_NAMES"\n'
            for dep_name, dep in self.deps_cpp_info.dependencies:
                content += '    "' + dep.get_name('cmake_find_package') + '" # ' + dep_name + '\n'
            content += ')\n'

            content += 'set("${PROJECT_NAME}_CMAKE_PACKAGE_VERSIONS"\n'
            for dep_name, dep in self.deps_cpp_info.dependencies:
                content += '    "' + str(dep.version) + '" # ' + dep_name + '\n'
            content += ')\n'

            content += 'set("${PROJECT_NAME}_CMAKE_PACKAGE_PATHS"\n'
            for dep_name, dep in self.deps_cpp_info.dependencies:
                content += '    "' + dep.rootpath.replace('\\', '/') + '" # ' + dep_name + '\n'
            content += ')\n'

            save(filename, content)
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e

    def imports(self):
        try:
            self.copy(pattern="*.dll", dst="bin", src="bin")
            self.copy(pattern="*.so", dst="lib", src="lib")
            self.copy(pattern="*.so.*", dst="lib", src="lib")
            self.copy(pattern="*.dylib", dst="lib", src="lib")
        except Exception as e:
            logging.error(e, exc_info=True)
            raise e


if __name__ == "__main__":
    pass
