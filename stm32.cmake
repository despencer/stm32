if(NOT DEFINED BOARD)
    message(FATAL_ERROR "BOARD is not defined")
endif()

set(STM32_BOARD ${BOARD})
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

set(STM32_LINK_FLAGS ${STM32_LINK_FLAGS}
  --static
  -nostartfiles
  -Wl,--gc-sections
  -specs=nosys.specs
  -Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group
  )

if(STM32_CPU STREQUAL "STM32F103C8T6")
   set(STM32_FAMILY "STM32F1")
   set(STM32_C_FLAGS ${STM32_C_FLAGS}
   -mcpu=cortex-m3
   -msoft-float
   -mfix-cortex-m3-ldrd
   )
elseif(STM32_CPU STREQUAL "STM32F411CEU6")
   set(STM32_FAMILY "STM32F4")
   set(STM32_C_FLAGS ${STM32_C_FLAGS}
     -mcpu=cortex-m4
     -mfloat-abi=hard
     -mfpu=fpv4-sp-d16
     )
   set(STM32_LINK_FLAGS ${STM32_LINK_FLAGS}
     -mcpu=cortex-m4
     -mfloat-abi=hard
     )
else()
   message(FATAL_ERROR "Unknown CPU")
endif()

set(CMAKE_TOOLCHAIN_FILE ${CMAKE_CURRENT_LIST_DIR}/arm.cmake)