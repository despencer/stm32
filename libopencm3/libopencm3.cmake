if(NOT DEFINED STM32_FAMILY)
    message(FATAL_ERROR "STM32_FAMILY is not defined")
endif()

set(STM32_C_FLAGS ${STM32_C_FLAGS} -D${STM32_FAMILY})

set(LINKER_FILE ${CMAKE_SOURCE_DIR}/stm32f103x8.ld)

set(CMAKE_C_STANDARD 99)

target_link_libraries(${EXECUTABLE} opencm3_stm32f1)
target_compile_options(${EXECUTABLE} PRIVATE ${STM32_C_FLAGS})

target_link_options(${EXECUTABLE} PRIVATE
--static
-nostartfiles
-T${LINKER_FILE}
-mthumb
-mcpu=cortex-m3
-msoft-float
-mfix-cortex-m3-ldrd
-Wl,-Map=${PROJECT_NAME}.map
-Wl,--gc-sections
-specs=nosys.specs
-Wl,--start-group -lc -lgcc -lnosys -Wl,--end-group
)

add_custom_command(TARGET ${EXECUTABLE}
POST_BUILD
COMMAND ${CMAKE_SIZE} ${EXECUTABLE}.elf
WORKING_DIRECTORY ${PROJECT_BINARY_DIR})

add_custom_command(TARGET ${EXECUTABLE}
POST_BUILD
COMMAND ${CMAKE_OBJCOPY} -Obinary ${EXECUTABLE}.elf ${PROJECT_NAME}.bin
WORKING_DIRECTORY ${PROJECT_BINARY_DIR})

