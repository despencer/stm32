set(OPENCM3HAL_SRC ${CMAKE_CURRENT_LIST_DIR}/opencm3hal)
if(STM32_CPU STREQUAL "STM32F103C8T6")
   set(STM32_C_FLAGS ${STM32_C_FLAGS} -DSTM32F1 -DSTM32F103C8T6 -D_ROM=64K -D_RAM=20K -D_ROM_OFF=0x08000000 -D_RAM_OFF=0x20000000)
   set(OPENCM3HAL_PATH ${CMAKE_CURRENT_LIST_DIR}/opencm3hal/stm32f1)
   set(LINKER_FILE ${OPENCM3HAL_PATH}/stm32f103x8.ld)
   target_link_libraries(${EXECUTABLE} opencm3_stm32f1)
elseif(STM32_CPU STREQUAL "STM32F411CEU6")
   set(STM32_C_FLAGS ${STM32_C_FLAGS} -DSTM32F4 -DSTM32F411CEU6 -D_ROM=512K -D_RAM=128K -D_ROM_OFF=0x08000000 -D_RAM_OFF=0x20000000)
   set(OPENCM3HAL_PATH ${CMAKE_CURRENT_LIST_DIR}/opencm3hal/stm32f4)
   set(LINKER_FILE ${OPENCM3HAL_PATH}/stm32f411xe.ld)
   target_link_libraries(${EXECUTABLE} opencm3_stm32f4)
else()
   message(FATAL_ERROR "Unknown CPU")
endif()

set(CMAKE_C_STANDARD 99)

# checking Python and required modules
find_package(Python REQUIRED)
execute_process(COMMAND ${Python_EXECUTABLE} -c "import jinja2" RESULT_VARIABLE RET)
if(NOT RET EQUAL 0)
    message(FATAL_ERROR "Missing jinja2")
endif()
execute_process(COMMAND ${Python_EXECUTABLE} -c "import yaml" RESULT_VARIABLE RET)
if(NOT RET EQUAL 0)
    message(FATAL_ERROR "Missing yaml")
endif()

if(NOT DEFINED BOARD)
   message(FATAL_ERROR "Board is not defined")
endif()

set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${OPENCM3HAL_SRC}/makedeps.py)
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${CMAKE_SOURCE_DIR}/board.config)

# getting list of generated files
execute_process(COMMAND ${Python_EXECUTABLE} ${OPENCM3HAL_SRC}/makedeps.py ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_LIST_DIR} ${BOARD}
    OUTPUT_VARIABLE DEPENDENCIES
    RESULT_VARIABLE RETURN_VALUE)
if(NOT RETURN_VALUE EQUAL 0)
   message(FATAL_ERROR "Failed to generate dependecies")
endif()

add_custom_command(
    OUTPUT opencm3hal.c opencm3res.c opencm3hal.h
    COMMAND ${Python_EXECUTABLE} ${OPENCM3HAL_SRC}/makehal.py ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${BOARD}
    DEPENDS ${OPENCM3HAL_SRC}/makehal.py ${OPENCM3HAL_SRC}/makedeps.py ${OPENCM3HAL_SRC}/config.py
            ${CMAKE_SOURCE_DIR}/board.config
            ${OPENCM3HAL_SRC}/opencm3hal.c.jinja ${OPENCM3HAL_SRC}/opencm3res.c.jinja ${OPENCM3HAL_SRC}/opencm3hal.h.jinja ${OPENCM3HAL_SRC}/opencm3haldef.h.jinja
            ${DEPENDENCIES}
            ${OPENCM3HAL_SRC}/output.py ${OPENCM3HAL_SRC}/usart.py
    COMMENT "Generating HAL")
add_custom_target(mcu_hal DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/opencm3hal.h)
add_dependencies(${EXECUTABLE} mcu_hal)

target_compile_options(${EXECUTABLE} PRIVATE ${STM32_C_FLAGS})
target_include_directories(${EXECUTABLE} PRIVATE ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_BINARY_DIR} ${CMAKE_CURRENT_LIST_DIR}/opencm3hal)
target_sources(${EXECUTABLE} PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/opencm3hal.c ${CMAKE_CURRENT_BINARY_DIR}/opencm3res.c ${OPENCM3HAL_PATH}/opencm3halmcu.c)

target_link_options(${EXECUTABLE} PRIVATE ${STM32_LINK_FLAGS}
  -T${LINKER_FILE}
  -Wl,-Map=${PROJECT_NAME}.map
  )

add_custom_command(TARGET ${EXECUTABLE}
POST_BUILD
COMMAND ${CMAKE_SIZE} ${EXECUTABLE}.elf
WORKING_DIRECTORY ${PROJECT_BINARY_DIR})

add_custom_command(TARGET ${EXECUTABLE}
POST_BUILD
COMMAND ${CMAKE_OBJCOPY} -Obinary ${EXECUTABLE}.elf ${PROJECT_NAME}.bin
WORKING_DIRECTORY ${PROJECT_BINARY_DIR})

