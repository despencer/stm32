if(STM32_CPU STREQUAL "STM32F103C8T6")
   set(STM32_C_FLAGS ${STM32_C_FLAGS} -DSTM32F1 -DSTM32F103C8T6 -D_ROM=64K -D_RAM=20K -D_ROM_OFF=0x08000000 -D_RAM_OFF=0x20000000)
   set(LINKER_FILE ${CMAKE_CURRENT_LIST_DIR}/stm32f103x8.ld)
   target_link_libraries(${EXECUTABLE} opencm3_stm32f1)
elseif(STM32_CPU STREQUAL "STM32F411CEU6")
   set(STM32_C_FLAGS ${STM32_C_FLAGS} -DSTM32F4 -DSTM32F411CEU6 -D_ROM=512K -D_RAM=128K -D_ROM_OFF=0x08000000 -D_RAM_OFF=0x20000000)
   set(LINKER_FILE ${CMAKE_CURRENT_LIST_DIR}/stm32f411xe.ld)
   target_link_libraries(${EXECUTABLE} opencm3_stm32f4)
else()
   message(FATAL_ERROR "Unknown CPU")
endif()

set(CMAKE_C_STANDARD 99)

target_compile_options(${EXECUTABLE} PRIVATE ${STM32_C_FLAGS})

target_link_options(${EXECUTABLE} PRIVATE
--static
-nostartfiles
#-nostdlib
-mcpu=cortex-m4
-mfloat-abi=hard
-T${LINKER_FILE}
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

