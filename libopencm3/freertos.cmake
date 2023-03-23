set(RTOS_PATH $ENV{HOME}/.local/lib/freertos)
set(RTOS_PORTABLE ARM_CM4F)
set(RTOS_PORTABLE_PATH ${RTOS_PATH}/portable/GCC/${RTOS_PORTABLE})

target_include_directories(${EXECUTABLE} PRIVATE ${RTOS_PATH}/include)

add_library(FreeRTOS STATIC
    ${RTOS_PATH}/event_groups.c
    ${RTOS_PATH}/list.c
    ${RTOS_PATH}/queue.c
    ${RTOS_PATH}/stream_buffer.c
    ${RTOS_PATH}/tasks.c
    ${RTOS_PATH}/timers.c
    ${RTOS_PORTABLE_PATH}/port.c
    ${RTOS_PATH}/portable/MemMang/heap_4.c
)
target_include_directories(FreeRTOS PUBLIC ${RTOS_PATH}/include ${RTOS_PORTABLE_PATH} ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_LIST_DIR} )
target_compile_options(FreeRTOS PRIVATE ${STM32_C_FLAGS})
target_link_libraries(${EXECUTABLE} FreeRTOS)
