#ifndef FREERTOS_MUTEX_H
#define FREERTOS_MUTEX_H

// This file is a mapper from common HAL to FreeRTOS

#include <halmutex.h>
#include "FreeRTOS.h"
#include "semphr.h"

typedef struct hal_mutex_s
{
 SemaphoreHandle_t xSemHandle;
 StaticSemaphore_t xSemData;
}
hal_mutex_t;

#endif
