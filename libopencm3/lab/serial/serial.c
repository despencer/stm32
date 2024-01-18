#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>

static void maintask(void *args __attribute((unused)))
{
 for (;;)
  {
    int i;

    hal_output_set(&red);
    vTaskDelay(3000);
    hal_output_set(&yellow);
    vTaskDelay(1000);
    hal_output_clear(&red);
    hal_output_clear(&yellow);
    hal_output_set(&green);
    vTaskDelay(3000);
    for(i=0; i<5; i++)
        {
        hal_output_toggle(&green);
        vTaskDelay(750);
        }
    hal_output_set(&yellow);
    vTaskDelay(1000);
    hal_output_clear(&yellow);
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