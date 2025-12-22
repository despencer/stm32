#ifndef HAL_MUTEX_H
#define HAL_MUTEX_H
// This file is a mapper between common interface and specific HAL interface

#include <stddef.h>
#include <stdint.h>

typedef struct hal_mutex_s hal_mutex_t;

void hal_mutex_create(hal_mutex_t* mutex);
void hal_mutex_lock(hal_mutex_t* mutex);
void hal_mutex_unlock(hal_mutex_t* mutex);

#endif
