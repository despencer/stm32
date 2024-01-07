cmake_minimum_required(VERSION 3.15)
include(${CMAKE_SOURCE_DIR}/../../../stm32.cmake)

project(miniblink VERSION 1.0)
set(EXECUTABLE ${PROJECT_NAME})
add_executable(${EXECUTABLE} miniblink.c)

include(${CMAKE_SOURCE_DIR}/../../libopencm3.cmake)