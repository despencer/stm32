#include <freertos_mutex.h>

void hal_mutex_create(hal_mutex_t* mutex)
{
 mutex->xSemHandle = xSemaphoreCreateMutexStatic(&mutex->xSemData);
}

void hal_mutex_lock(hal_mutex_t* mutex)
{
 xSemaphoreTake(mutex->xSemHandle, portMAX_DELAY);
}

void hal_mutex_unlock(hal_mutex_t* mutex)
{
 xSemaphoreGive(mutex->xSemHandle);
}