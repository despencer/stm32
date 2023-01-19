if(STM32_BOARD STREQUAL "BluePill")
    set(STM32_CPU "STM32F103C8T6")
endif()

if(NOT DEFINED STM32_CPU)
    message(FATAL_ERROR "STM32_CPU is not defined")
endif()

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_LIST_DIR}/arm.cmake)