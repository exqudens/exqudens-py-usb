cmake_minimum_required(VERSION 3.25 FATAL_ERROR)

if(NOT "${CMAKE_SCRIPT_MODE_FILE}" STREQUAL "")
    message(FATAL_ERROR "Unsupported in script mode '${CMAKE_CURRENT_LIST_FILE}'!")
endif()

function(vscode)
    set(currentFunctionName "${CMAKE_CURRENT_FUNCTION}")
    set(options)
    set(oneValueKeywords
        "SETTINGS_FILE"
        "C_CPP_PROPERTIES_FILE"
        "TASKS_FILE"
        "LAUNCH_FILE"
    )
    set(multiValueKeywords)

    cmake_parse_arguments("${currentFunctionName}" "${options}" "${oneValueKeywords}" "${multiValueKeywords}" "${ARGN}")

    # Generate ".vscode/settings.json"
    if(NOT "${${currentFunctionName}_SETTINGS_FILE}" STREQUAL "")
        if(EXISTS "${${currentFunctionName}_SETTINGS_FILE}")
            file(READ "${${currentFunctionName}_SETTINGS_FILE}" settings)
            if("${settings}" STREQUAL "")
                set(settings "{}")
            endif()
        else()
            set(settings "{}")
        endif()

        # Get keys
        set(settingsKeys)
        string(JSON listLength LENGTH "${settings}")
        if("${listLength}" GREATER "0")
            math(EXPR maxIndex "${listLength} - 1")
            foreach(i RANGE "0" "${maxIndex}")
                string(JSON k MEMBER "${settings}" "${i}")
                list(APPEND settingsKeys "${k}")
            endforeach()
        endif()

        # Set items
        set(k "C_Cpp.errorSquiggles")
        if(NOT "${k}" IN_LIST "settingsKeys")
            string(JSON settings SET "${settings}" "${k}" "\"enabled\"")
        endif()
        set(k "C_Cpp.intelliSenseEngine")
        if(NOT "${k}" IN_LIST "settingsKeys")
            string(JSON settings SET "${settings}" "${k}" "\"default\"")
        endif()
        set(k "C_Cpp.intelliSenseEngineFallback")
        if(NOT "${k}" IN_LIST "settingsKeys")
            string(JSON settings SET "${settings}" "${k}" "\"enabled\"")
        endif()
        set(k "files.readonlyFromPermissions")
        if(NOT "${k}" IN_LIST "settingsKeys")
            string(JSON settings SET "${settings}" "${k}" "true")
        endif()
        set(k "files.associations")
        if(NOT "${k}" IN_LIST "settingsKeys")
            string(JSON settings SET "${settings}" "${k}" "{}")
            string(JSON settings SET "${settings}" "${k}" "*.h" "\"c\"")
            string(JSON settings SET "${settings}" "${k}" "*.c" "\"c\"")
            string(JSON settings SET "${settings}" "${k}" "*.hpp" "\"cpp\"")
            string(JSON settings SET "${settings}" "${k}" "*.cpp" "\"cpp\"")
        endif()

        file(WRITE "${${currentFunctionName}_SETTINGS_FILE}" "${settings}")
    endif()

    # Generate ".vscode/c_cpp_properties.json"
    if(NOT "${${currentFunctionName}_C_CPP_PROPERTIES_FILE}" STREQUAL "")
        if(EXISTS "${${currentFunctionName}_C_CPP_PROPERTIES_FILE}")
            file(READ "${${currentFunctionName}_C_CPP_PROPERTIES_FILE}" cCppProperties)
            if("${cCppProperties}" STREQUAL "")
                string(JSON cCppProperties SET "{}" "version" "4")
                string(JSON cCppProperties SET "${cCppProperties}" "configurations" "[]")
            endif()
        else()
            string(JSON cCppProperties SET "{}" "version" "4")
            string(JSON cCppProperties SET "${cCppProperties}" "configurations" "[]")
        endif()

        string(REPLACE "." ";" values "${PRESET_NAME}")
        list(GET "values" "2" entryName)

        # Generate ".vscode/c_cpp_properties.json" content
        string(JSON entry SET "{}" "name" "\"${entryName}\"")
        string(JSON entry SET "${entry}" "compilerPath" "\"${CMAKE_CXX_COMPILER}\"")
        set(v "${PROJECT_BINARY_DIR}/compile_commands.json")
        cmake_path(RELATIVE_PATH v BASE_DIRECTORY "${PROJECT_SOURCE_DIR}")
        string(JSON entry SET "${entry}" "compileCommands" "\"${v}\"")
        if("${entryName}" STREQUAL "gcc-arm")
            set(v "gcc-arm")
        elseif("${entryName}" STREQUAL "gcc")
            set(v "gcc-x64")
        elseif("${entryName}" STREQUAL "msvc")
            set(v "msvc-x64")
        endif()
        string(JSON entry SET "${entry}" "intelliSenseMode" "\"${v}\"")
        string(JSON entry SET "${entry}" "cStandard" "\"c${CMAKE_C_STANDARD}\"")
        string(JSON entry SET "${entry}" "cppStandard" "\"c++${CMAKE_CXX_STANDARD}\"")
        string(JSON entry SET "${entry}" "configurationProvider" "\"ms-vscode.cmake-tools\"")
        string(JSON entry SET "${entry}" "mergeConfigurations" "true")

        # Find index
        string(JSON entryIndex LENGTH "${cCppProperties}" "configurations")
        if("${entryIndex}" GREATER "0")
            math(EXPR maxIndex "${entryIndex} - 1")
           foreach(i RANGE "0" "${maxIndex}")
                string(JSON v GET "${cCppProperties}" "configurations" "${i}")
                string(JSON vName GET "${v}" "name")
                if("${vName}" STREQUAL "${entryName}")
                    set(entryIndex "${i}")
                    break()
                endif()
            endforeach()
        endif()

        # Set item
        string(JSON cCppProperties SET "${cCppProperties}" "configurations" "${entryIndex}" "${entry}")

        file(WRITE "${${currentFunctionName}_C_CPP_PROPERTIES_FILE}" "${cCppProperties}")
    endif()
endfunction()
