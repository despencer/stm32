cmake_minimum_required(VERSION 3.15)
include(${CMAKE_SOURCE_DIR}/../lab.cmake)

project(miniblink VERSION 1.0)
set(EXECUTABLE ${PROJECT_NAME})
add_executable(${EXECUTABLE} miniblink.c)

include(${CMAKE_LIBOPENCM3})
