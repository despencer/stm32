#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>

static void maintask(void *args __attribute((unused)))
{
 uint8_t data;
 for (;;)
   {
   data = hal_usart_read(&console);
   hal_usart_send(&console, &data, 1);
   if (data == '\r')
      { data = '\n'; hal_usart_send(&console, &data, 1); }
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