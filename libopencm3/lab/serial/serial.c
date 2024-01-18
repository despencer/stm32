#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>

static char* hello = "Hello from STM32\n";

static void maintask(void *args __attribute((unused)))
{
 for (;;)
  {
    hal_usart_send(&console, hello, strnlen(hello, 100));
    vTaskDelay(1000);
  }
}

int main(void)
{
   hal_init();

   xTaskCreate(maintask, "MAIN", 200, NULL, configMAX_PRIORITIES-1,NULL);
   vTaskStartScheduler();

   for (;;);
   return 0;
}