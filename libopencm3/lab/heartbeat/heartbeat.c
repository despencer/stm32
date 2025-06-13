#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>

static void heartbeat(void *args __attribute((unused)))
{
 const TickType_t delay = 1000 / portTICK_PERIOD_MS;
 uint32_t hb = 0, size = 4, value = 0;
 for (;;)
   {
   hal_usart_send(&cmdcnt, (uint8_t*)&hb, 4);
   hal_usart_send(&cmdcnt, (uint8_t*)&size, 4);
   hal_usart_send(&cmdcnt, (uint8_t*)&value, 4);
   value++;
   vTaskDelay(delay);
   }
}

int main(void)
{
   hal_init();

   xTaskCreate(heartbeat, "HeartBeat", 200, NULL, configMAX_PRIORITIES-1,NULL);
   vTaskStartScheduler();

   for (;;);
   return 0;
}