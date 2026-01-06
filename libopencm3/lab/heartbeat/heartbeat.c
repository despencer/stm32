#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>
#include <slpx.h>

static void heartbeat(void *args __attribute((unused)))
{
 const TickType_t delay = 1000 / portTICK_PERIOD_MS;
 uint32_t value = 232;
 for (;;)
   {
   if (cmdcnt.status & SLPX_CONNECTED)
      {
      slpx_send(&cmdcnt, SLPX_HEARTBEAT, (uint8_t*)&value, 4);
      value++;
      }
   vTaskDelay(delay);
   }
}

int main(void)
{
   hal_system_init();

   xTaskCreate(heartbeat, "HeartBeat", 200, NULL, configMAX_PRIORITIES-1,NULL);
   vTaskStartScheduler();

   for (;;);
   return 0;
}