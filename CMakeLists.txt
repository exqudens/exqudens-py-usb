cmake_minimum_required(VERSION 3.25 FATAL_ERROR)

set(INSTALL_PREFIX "${CMAKE_BINARY_DIR}/../common/cmake-install")
cmake_path(NORMAL_PATH "INSTALL_PREFIX")
cmake_path(RELATIVE_PATH "INSTALL_PREFIX" BASE_DIRECTORY "${CMAKE_SOURCE_DIR}" OUTPUT_VARIABLE RELATIVE_INSTALL_PREFIX)

set(INSTALL_PREFIX "${INSTALL_PREFIX}" CACHE PATH "..." FORCE)
set(RELATIVE_INSTALL_PREFIX "${RELATIVE_INSTALL_PREFIX}" CACHE PATH "..." FORCE)
set(CMAKE_INSTALL_PREFIX "${INSTALL_PREFIX}" CACHE PATH "..." FORCE)
set(USE_CONAN "TRUE" CACHE BOOL "...")
set(SKIP_TEST "FALSE" CACHE BOOL "" FORCE)
set(TEST_GROUP "unit" CACHE STRING "...")
set(TEST_CASE "all" CACHE STRING "...")

block()
    set(fileName "util.cmake")
    if(NOT EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../common/${fileName}")
        file(REMOVE "${CMAKE_CURRENT_BINARY_DIR}/tmp/${fileName}")
        file(DOWNLOAD
            "https://raw.githubusercontent.com/exqudens/exqudens-cmake/1.0.1/src/main/cmake/${fileName}"
            "${CMAKE_CURRENT_BINARY_DIR}/tmp/${fileName}"
            EXPECTED_MD5 "d7dd546adf3830d9eb6cca7b0dda7d4e"
            STATUS downloadStatus
        )
        if(NOT "${downloadStatus}" STREQUAL "0;\"No error\"")
            message(FATAL_ERROR "downloadStatus: '${downloadStatus}'")
        endif()
        file(COPY "${CMAKE_CURRENT_BINARY_DIR}/tmp/${fileName}" DESTINATION "${CMAKE_CURRENT_BINARY_DIR}/../common")
    endif()
endblock()

include("${CMAKE_CURRENT_BINARY_DIR}/../common/util.cmake")

string(REPLACE "." ";" PRESET_NAME_ELEMENTS "${PRESET_NAME}")
if("msvc-16-x64-x64" IN_LIST "PRESET_NAME_ELEMENTS")
    if(NOT EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../common/msvc-16-x64-x64-toolchain.cmake")
        set_msvc_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            VERSION "16"
            HOST "x64"
            TARGET "x64"
            OUTPUT_FILE "${CMAKE_CURRENT_BINARY_DIR}/../common/msvc-16-x64-x64-toolchain.cmake"
        )
    endif()
    if("${USE_CONAN}")
        find_program(CONAN_COMMAND NAMES "conan.exe" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    endif()
    find_program(PYTHON_COMMAND NAMES "py.exe" "py" PATHS ENV PYTHON_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    set(PYTHON_ENV_REL_PATH "Scripts/python.exe")
    set(PYTEST_ENV_REL_PATH "Scripts/pytest.exe")
elseif("gcc" IN_LIST PRESET_NAME_ELEMENTS)
    if(NOT EXISTS "${CMAKE_CURRENT_BINARY_DIR}/../common/gcc-toolchain.cmake")
        find_file(COMPILER_FILE NAMES "gcc" PATHS ENV GCC_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
        set_gnu_toolchain(TOOLCHAIN_CONTENT
            PROCESSOR "x86_64"
            OS "${CMAKE_HOST_SYSTEM_NAME}"
            PATH "${COMPILER_FILE}"
            OUTPUT_FILE "${CMAKE_CURRENT_BINARY_DIR}/../common/gcc-toolchain.cmake"
        )
    endif()
    if("${USE_CONAN}")
        find_program(CONAN_COMMAND NAMES "conan" PATHS ENV CONAN_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    endif()
    find_program(PYTHON_COMMAND NAMES "python" PATHS ENV PYTHON_PATH ENV PATH REQUIRED NO_CACHE NO_DEFAULT_PATH)
    set(PYTHON_ENV_REL_PATH "bin/python")
    set(PYTEST_ENV_REL_PATH "bin/pytest")
endif()

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/pyproject.toml" INFO)
string(REGEX MATCH "name = \"[^\"]+\"" RAW_NAME "${INFO}")
string(REGEX MATCH "version = \"[^\"]+\"" RAW_VERSION "${INFO}")
string(REGEX REPLACE "name = \"(.+)\"" "\\1" RAW_NAME "${RAW_NAME}")
string(REGEX REPLACE "version = \"(.+)\"" "\\1" RAW_VERSION "${RAW_VERSION}")
string(STRIP "${RAW_NAME}" NAME)
string(STRIP "${RAW_VERSION}" VERSION)

project("${NAME}" VERSION "${VERSION}" LANGUAGES "NONE")

message(STATUS "project: '${PROJECT_NAME}-${PROJECT_VERSION}'")

string(REPLACE "_" "-" BASE_DIR "${PROJECT_NAME}")
string(REPLACE "-py-" "-" BASE_DIR "${BASE_DIR}")
string(REPLACE "-" "/" BASE_DIR "${BASE_DIR}")

message(STATUS "BASE_DIR: '${BASE_DIR}'")

string(REPLACE "-" "_" PACKAGE_NAME "${PROJECT_NAME}")

message(STATUS "PACKAGE_NAME: '${PACKAGE_NAME}'")

include("GenerateExportHeader")
enable_testing()
include("GoogleTest")

if("$ENV{CLION_IDE}")
    cmake_path(CONVERT "$ENV{PATH}" TO_CMAKE_PATH_LIST TMP_CMAKE_ENV_PATH NORMALIZE)
    list(REMOVE_AT TMP_CMAKE_ENV_PATH 0)
    cmake_path(CONVERT "${TMP_CMAKE_ENV_PATH}" TO_NATIVE_PATH_LIST TMP_NATIVE_ENV_PATH NORMALIZE)
    set("ENV{PATH}" "${TMP_NATIVE_ENV_PATH}")
endif()

enable_language("C")
enable_language("CXX")

set(CMAKE_VERBOSE_MAKEFILE "TRUE" CACHE BOOL "" FORCE)
set(CMAKE_EXPORT_COMPILE_COMMANDS "TRUE" CACHE BOOL "" FORCE)

set(CMAKE_OBJECT_PATH_MAX 1000)
set(CMAKE_SHARED_LIBRARY_PREFIX "")
set(CMAKE_SHARED_MODULE_PREFIX "")
set(CMAKE_STATIC_LIBRARY_PREFIX "")
set(CMAKE_IMPORT_LIBRARY_PREFIX "")
set(CMAKE_STAGING_PREFIX "")
set(CMAKE_FIND_LIBRARY_PREFIXES "" "lib")
set(CMAKE_FIND_USE_CMAKE_ENVIRONMENT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_SYSTEM_PATH FALSE)
set(CMAKE_FIND_USE_SYSTEM_ENVIRONMENT_PATH TRUE)
set(CMAKE_FIND_USE_SYSTEM_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_REGISTRY FALSE)
set(CMAKE_FIND_USE_PACKAGE_ROOT_PATH FALSE)
set(CMAKE_FIND_USE_CMAKE_PATH TRUE)
set(CMAKE_FIND_PACKAGE_PREFER_CONFIG FALSE)
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS FALSE)
set(CMAKE_BUILD_RPATH "\$ORIGIN")
set(CMAKE_INSTALL_RPATH "\$ORIGIN")
set(CMAKE_SKIP_BUILD_RPATH TRUE)
set(CMAKE_BUILD_RPATH_USE_ORIGIN TRUE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH FALSE)
set(CMAKE_CXX_VISIBILITY_PRESET "hidden")
set(CMAKE_VISIBILITY_INLINES_HIDDEN TRUE)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

separate_arguments(CMAKE_CXX_FLAGS NATIVE_COMMAND "${CMAKE_CXX_FLAGS}")
if(MSVC)
    if(NOT "/EHa" IN_LIST CMAKE_CXX_FLAGS AND "/EHsc" IN_LIST CMAKE_CXX_FLAGS)
        list(REMOVE_ITEM CMAKE_CXX_FLAGS "/EHsc")
        list(APPEND CMAKE_CXX_FLAGS "/EHa")
    endif()
endif()
string(JOIN " " CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})

if("${BUILD_SHARED_LIBS}")
    set(CONAN_RELEASE_COMPILER_RUNTIME "MD")
else()
    set(CONAN_RELEASE_COMPILER_RUNTIME "MT")
    if("${MINGW}")
        set(CMAKE_CXX_STANDARD_LIBRARIES "-static-libgcc -static-libstdc++ ${CMAKE_CXX_STANDARD_LIBRARIES}")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Bstatic,--whole-archive -lwinpthread -Wl,--no-whole-archive")
    endif()
endif()

if(NOT "${SKIP_TEST}")
    if("${TEST_GROUP}" STREQUAL "all" AND "${TEST_CASE}" STREQUAL "all")
        set(TEST_REGEXP "^.+\\..+$")
    elseif(NOT "${TEST_GROUP}" STREQUAL "all" AND "${TEST_CASE}" STREQUAL "all")
        set(TEST_REGEXP "^${TEST_GROUP}\\..+$")
    elseif("${TEST_GROUP}" STREQUAL "all" AND NOT "${TEST_CASE}" STREQUAL "all")
        set(TEST_REGEXP "^.+\\.${TEST_CASE}$")
    elseif(NOT "${TEST_GROUP}" STREQUAL "all" AND NOT "${TEST_CASE}" STREQUAL "all")
        set(TEST_REGEXP "^${TEST_GROUP}\\.${TEST_CASE}$")
    endif()

    message(STATUS "TEST_GROUP: '${TEST_GROUP}'")
    message(STATUS "TEST_CASE: '${TEST_CASE}'")
    message(STATUS "TEST_REGEXP: '${TEST_REGEXP}'")
endif()

set(CONAN_INSTALL_PREFIX "${PROJECT_BINARY_DIR}/conan-install")
set(CONAN_INSTALL_TEST_PREFIX "${PROJECT_BINARY_DIR}/conan-install-test")

file(MAKE_DIRECTORY "${CONAN_INSTALL_PREFIX}/bin")
file(MAKE_DIRECTORY "${CONAN_INSTALL_PREFIX}/lib")
file(MAKE_DIRECTORY "${CONAN_INSTALL_TEST_PREFIX}/bin")
file(MAKE_DIRECTORY "${CONAN_INSTALL_TEST_PREFIX}/lib")

if("${USE_CONAN}")
    set_conan_architecture(CONAN_ARCH "${CMAKE_SYSTEM_PROCESSOR}")
    set_conan_compiler(CONAN_COMPILER "${CMAKE_CXX_COMPILER_ID}")
    set_conan_compiler_version(CONAN_COMPILER_VERSION "${CMAKE_CXX_COMPILER_ID}" "${CMAKE_CXX_COMPILER_VERSION}" MAX_ELEMENTS "1")
    set_conan_compiler_runtime(CONAN_COMPILER_RUNTIME "${CMAKE_MSVC_RUNTIME_LIBRARY}")

    set_python_boolean(CONAN_INTERFACE_ONLY "${INTERFACE_ONLY}")
    set_python_boolean(CONAN_BUILD_SHARED_LIBS "${BUILD_SHARED_LIBS}")

    set_conan_settings(CONAN_SETTINGS
        "arch=${CONAN_ARCH}"
        "os=${CMAKE_SYSTEM_NAME}"
        "compiler=${CONAN_COMPILER}"
        "compiler.version=${CONAN_COMPILER_VERSION}"
        "compiler.runtime=${CONAN_COMPILER_RUNTIME}"
        "compiler.libcxx=${CONAN_COMPILER_LIBCXX}"
        "build_type=${CMAKE_BUILD_TYPE}"
    )
    set_conan_options(CONAN_OPTIONS
        "interface=${CONAN_INTERFACE_ONLY}"
        "shared=${CONAN_BUILD_SHARED_LIBS}"
    )
    if(NOT EXISTS "${CONAN_INSTALL_PREFIX}/conan-packages.cmake")
        execute_process(
            COMMAND "${CONAN_COMMAND}" "install"
                    "--install-folder" "${CONAN_INSTALL_PREFIX}"
                    ${CONAN_SETTINGS}
                    ${CONAN_OPTIONS}
                    "${PROJECT_SOURCE_DIR}/conanfile.py"
            COMMAND_ECHO "STDOUT"
            ENCODING "UTF-8"
            COMMAND_ERROR_IS_FATAL "ANY"
        )
    endif()
    if(NOT EXISTS "${CONAN_INSTALL_PREFIX}/conan-packages.cmake")
        message(FATAL_ERROR "Not exists: '${CONAN_INSTALL_PREFIX}/conan-packages.cmake'")
    endif()
    include("${CONAN_INSTALL_PREFIX}/conan-packages.cmake")
    list(APPEND CMAKE_MODULE_PATH "${CONAN_INSTALL_PREFIX}")
    foreach(
        conanPackageName
        cmakePackageName
        cmakePackageVersion
        cmakePackagePath
        IN ZIP_LISTS
        "${PROJECT_NAME}_CONAN_PACKAGE_NAMES"
        "${PROJECT_NAME}_CMAKE_PACKAGE_NAMES"
        "${PROJECT_NAME}_CMAKE_PACKAGE_VERSIONS"
        "${PROJECT_NAME}_CMAKE_PACKAGE_PATHS"
    )
        if(
            "" STREQUAL "${conanPackageName}"
            OR "" STREQUAL "${cmakePackageName}"
            OR "" STREQUAL "${cmakePackageVersion}"
            OR "" STREQUAL "${cmakePackagePath}"
        )
            string(JOIN " " errorMessage
                "Empty value 'conanPackageName': '${conanPackageName}'"
                "or 'cmakePackageName': '${cmakePackageName}'"
                "or 'cmakePackageVersion': '${cmakePackageVersion}'"
                "or 'cmakePackagePath': '${cmakePackagePath}'!"
            )
            message(FATAL_ERROR "${errorMessage}")
        elseif(NOT IS_DIRECTORY "${cmakePackagePath}")
            message(FATAL_ERROR "Not is directory 'cmakePackagePath': '${cmakePackagePath}'!")
        endif()

        if("${${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_VERSION}" STREQUAL "")
            set("${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_VERSION" "${cmakePackageVersion}")
        endif()

        if("${${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_PATH}" STREQUAL "")
            set("${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_PATH" "${cmakePackagePath}")
        endif()

        list(APPEND "${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES" "${cmakePackageName}")
        list(APPEND CMAKE_PREFIX_PATH "${cmakePackagePath}")
    endforeach()
endif()

if("${${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES}" STREQUAL "")
    set("${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES"
        "exqudens-cpp-usb"
        "pybind11"
    )
endif()
message(STATUS "${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES:")
foreach(cmakePackageName IN LISTS "${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES")
    message(STATUS "  ${cmakePackageName}")
endforeach()
unset(NOT_FOUND_PACKAGE_NAMES)
foreach(cmakePackageName IN LISTS "${PROJECT_NAME}_CMAKE_FIND_PACKAGE_NAMES")
    if("exqudens-cpp-usb" STREQUAL "${cmakePackageName}")
        file(REMOVE "${CONAN_INSTALL_TEST_PREFIX}/Find${cmakePackageName}.cmake")
        list(APPEND NOT_FOUND_PACKAGE_NAMES "${cmakePackageName}")
        find_package("${cmakePackageName}" "${${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_VERSION}" EXACT QUIET CONFIG)
    elseif("pybind11" STREQUAL "${cmakePackageName}")
        list(APPEND NOT_FOUND_PACKAGE_NAMES "${cmakePackageName}")
        find_package("${cmakePackageName}" "${${PROJECT_NAME}_CMAKE_PACKAGE_${cmakePackageName}_VERSION}" EXACT QUIET)
    else()
        message("Ignore cmakePackageName: '${cmakePackageName}'")
    endif()
endforeach()
set_not_found_package_names(NOT_FOUND_PACKAGE_NAMES ${NOT_FOUND_PACKAGE_NAMES})
if(NOT "" STREQUAL "${NOT_FOUND_PACKAGE_NAMES}")
    foreach(package IN LISTS NOT_FOUND_PACKAGE_NAMES)
        message(SEND_ERROR "${package}_FOUND: '${${package}_FOUND}' ${package}_NOT_FOUND_MESSAGE: '${${package}_NOT_FOUND_MESSAGE}'")
    endforeach()
    message(FATAL_ERROR "Some package not found!")
endif()

if("${CMAKE_SYSTEM_NAME}" STREQUAL "Windows")
    #set(CMAKE_CXX_STANDARD_LIBRARIES "${CMAKE_CXX_STANDARD_LIBRARIES} setupapi.lib")
elseif("${CMAKE_SYSTEM_NAME}" STREQUAL "Linux")
    #set(CMAKE_CXX_STANDARD_LIBRARIES "${CMAKE_CXX_STANDARD_LIBRARIES} Ws2_32.lib")
endif()

pybind11_add_module("client"
    "src/main/cpp/${BASE_DIR}/pybind/client.cpp"
)
target_include_directories("client" PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/src/main/cpp>"
    "$<INSTALL_INTERFACE:include>"
)
target_link_libraries("client" PUBLIC
    "exqudens-cpp-usb::exqudens-cpp-usb"
)
set_target_properties("client" PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/bin"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/bin"

    ARCHIVE_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/lib"
    ARCHIVE_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/lib"

    LIBRARY_OUTPUT_DIRECTORY                "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE        "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_RELWITHDEBINFO "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_MINSIZEREL     "${PROJECT_BINARY_DIR}/main/lib"
    LIBRARY_OUTPUT_DIRECTORY_DEBUG          "${PROJECT_BINARY_DIR}/main/lib"
)
#set_property(TARGET "client" PROPERTY "VERSION" "${PROJECT_VERSION}")
#set_property(TARGET "client" PROPERTY "SOVERSION" "${PROJECT_VERSION}")
set_property(TARGET "client" PROPERTY "INTERFACE_${PROJECT_NAME}_MAJOR_VERSION" "${PROJECT_VERSION}")
set_property(TARGET "client" APPEND PROPERTY "COMPATIBLE_INTERFACE_STRING" "${PROJECT_NAME}_MAJOR_VERSION")
install(
    TARGETS "client"
    LIBRARY DESTINATION "src/exqudens/usb/pybind"
)
install(
    DIRECTORY "src/main/py/"
    DESTINATION "src"
    FILES_MATCHING
    PATTERN "*.py"
)
install(
    FILES "pyproject.toml"
    DESTINATION "."
)

add_custom_command(
    OUTPUT "${CMAKE_INSTALL_PREFIX}/pyproject.toml"
    COMMAND "${CMAKE_COMMAND}" "--install" "${PROJECT_BINARY_DIR}" --prefix "${CMAKE_INSTALL_PREFIX}"
    DEPENDS "client"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_command(
    OUTPUT "${PROJECT_BINARY_DIR}/../common/py-build-env/${PYTHON_ENV_REL_PATH}"
    COMMAND "${PYTHON_COMMAND}" "-m" "venv" "${PROJECT_BINARY_DIR}/../common/py-build-env"
    WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    USES_TERMINAL
    VERBATIM
)

add_custom_command(
    OUTPUT "${CMAKE_INSTALL_PREFIX}/dist/${PACKAGE_NAME}-${PROJECT_VERSION}-py3-none-any.whl"
    COMMAND "${PROJECT_BINARY_DIR}/../common/py-build-env/${PYTHON_ENV_REL_PATH}" "-m" "pip" "install" "build==1.2.1"
    COMMAND "${PROJECT_BINARY_DIR}/../common/py-build-env/${PYTHON_ENV_REL_PATH}" "-m" "build"
    DEPENDS "${CMAKE_INSTALL_PREFIX}/pyproject.toml" "${PROJECT_BINARY_DIR}/../common/py-build-env/${PYTHON_ENV_REL_PATH}"
    WORKING_DIRECTORY "${CMAKE_INSTALL_PREFIX}"
    USES_TERMINAL
    VERBATIM
)

add_custom_target("wheel"
    DEPENDS "${CMAKE_INSTALL_PREFIX}/dist/${PACKAGE_NAME}-${PROJECT_VERSION}-py3-none-any.whl"
)

if(NOT "${SKIP_TEST}")
    add_custom_command(
        OUTPUT "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTHON_ENV_REL_PATH}"
        COMMAND "${PYTHON_COMMAND}" "-m" "venv" "${PROJECT_BINARY_DIR}/../common/py-test-env"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_custom_command(
        OUTPUT "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTEST_ENV_REL_PATH}"
        COMMAND "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTHON_ENV_REL_PATH}" "-m" "pip" "install" "-r" "src/test/resources/requirements.txt"
        COMMAND "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTHON_ENV_REL_PATH}" "-m" "pip" "install" "./${RELATIVE_INSTALL_PREFIX}/dist/${PACKAGE_NAME}-${PROJECT_VERSION}-py3-none-any.whl"
        DEPENDS "${CMAKE_INSTALL_PREFIX}/dist/${PACKAGE_NAME}-${PROJECT_VERSION}-py3-none-any.whl"
                "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTHON_ENV_REL_PATH}"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )

    add_test(
        NAME "unit.test_1"
        COMMAND "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTEST_ENV_REL_PATH}" "--log-cli-level=DEBUG" "src/test/py/system/test_exqudens_usb_client.py::TestExqudensUsbClient::test_1"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
    )

    add_custom_target("cmake-test"
        COMMAND "${CMAKE_CTEST_COMMAND}" --preset "${PRESET_NAME}" -R "${TEST_REGEXP}"
        DEPENDS "${PROJECT_BINARY_DIR}/../common/py-test-env/${PYTEST_ENV_REL_PATH}"
        WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}"
        USES_TERMINAL
        VERBATIM
    )
endif()

set_target_names(ALL_TARGETS "${CMAKE_CURRENT_SOURCE_DIR}")
message(STATUS "all-targets:")
foreach(t IN LISTS ALL_TARGETS)
    message(STATUS "${t}")
endforeach()

# Generate vscode files if env var VSCODE value is "true"
if("$ENV{VSCODE}")
    include("${PROJECT_SOURCE_DIR}/cmake/vscode.cmake")
    if("$ENV{VSCODE_SETTINGS}")
        vscode(SETTINGS_FILE "${PROJECT_SOURCE_DIR}/.vscode/settings.json")
    endif()
    if("$ENV{VSCODE_C_CPP_PROPERTIES}")
        vscode(C_CPP_PROPERTIES_FILE "${PROJECT_SOURCE_DIR}/.vscode/c_cpp_properties.json")
    endif()
endif()
