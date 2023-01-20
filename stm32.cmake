if(STM32_BOARD STREQUAL "BluePill")
    set(STM32_CPU "STM32F103C8T6")
elseif(STM32_BOARD STREQUAL "BlackPill")
    set(STM32_CPU "STM32F411CEU6")
endif()

if(NOT DEFINED STM32_CPU)
    message(FATAL_ERROR "STM32_CPU is not defined")
endif()

set(STM32_C_FLAGS ${STM32_C_FLAGS}
   -Os  # size optimization
   -mthumb  # 16-bit Thumb instruction set
   -Wextra -Wshadow -Wimplicit-function-declaration -Wredundant-decls -Wmissing-prototypes -Wstrict-prototypes -Wall -Wundef  # warnings
   -fno-common   # a way of treating uninitialized variables (put them to BSS)
   -ffunction-sections -fdata-sections  # put each function and data item into its own section
)

if(STM32_CPU STREQUAL "STM32F103C8T6")
   set(STM32_FAMILY "STM32F1")
   set(STM32_C_FLAGS ${STM32_C_FLAGS}
-mcpu=cortex-m3
-msoft-float
-mfix-cortex-m3-ldrd
)
endif()

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_LIST_DIR}/arm.cmake)