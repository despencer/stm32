# non-HAL libraries
add_library(comm STATIC
    ${OPENCM3HAL_SRC}/comm/slpx.c
)
target_compile_options(comm PRIVATE ${STM32_C_FLAGS})
target_include_directories(comm PUBLIC ${CMAKE_SOURCE_DIR} ${CMAKE_CURRENT_LIST_DIR} ${CMAKE_CURRENT_LIST_DIR}/opencm3hal ${CMAKE_CURRENT_BINARY_DIR})
target_link_libraries(${EXECUTABLE} comm)
