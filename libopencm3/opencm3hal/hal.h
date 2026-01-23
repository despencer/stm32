#ifndef HAL_H
#define HAL_H

#include <stdint.h>

void hal_system_init(void);
void hal_system_shutdown(void);
void hal_system_reboot(void);
void hal_system_bootloader(void);

#endif