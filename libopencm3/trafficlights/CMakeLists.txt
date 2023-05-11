cmake_minimum_required(VERSION 3.15)
include(${CMAKE_SOURCE_DIR}/../../stm32.cmake)

project(trafficlights VERSION 1.0)
set(EXECUTABLE ${PROJECT_NAME})

add_executable(${EXECUTABLE} trafficlights.c)
target_include_directories(${EXECUTABLE} PUBLIC ${CMAKE_SOURCE_DIR})

include(${CMAKE_SOURCE_DIR}/../libopencm3.cmake)
include(${CMAKE_SOURCE_DIR}/../freertos.cmake)