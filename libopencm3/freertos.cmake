set(RTOS_PATH $ENV{HOME}/.local/lib/freertos)
set(RTOS_PORTABLE ARM_CM4F)
set(RTOS_PORTABLE_PATH ${RTOS_PATH}/portable/GCC/${RTOS_PORTABLE})

target_include_directories(${EXECUTABLE} PRIVATE ${RTOS_PATH}/include)

file(GLOB FreeRTOS_src ${RTOS_PATH}/*.c)
add_library(FreeRTOS STATIC
    ${FreeRTOS_src}
    ${RTOS_PORTABLE_PATH}/port.c
    ${RTOS_PATH}/portable/MemMang/heap_4.c
)
target_include_directories(FreeRTOS PUBLIC ${RTOS_PATH}/include ${RTOS_PORTABLE_PATH} ${CMAKE_SOURCE_DIR} )
target_compile_options(FreeRTOS PRIVATE ${STM32_C_FLAGS})
message(STATUS ${STM32_C_FLAGS})
target_link_libraries(${EXECUTABLE} FreeRTOS)