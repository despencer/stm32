cmake_minimum_required(VERSION 3.20)
include(${CMAKE_SOURCE_DIR}/../lab.cmake)

project(reset VERSION 1.0)
set(EXECUTABLE ${PROJECT_NAME})

add_executable(${EXECUTABLE} reset.c)
target_include_directories(${EXECUTABLE} PUBLIC ${CMAKE_SOURCE_DIR})

include(${CMAKE_LIBOPENCM3})
include(${CMAKE_FREERTOS})