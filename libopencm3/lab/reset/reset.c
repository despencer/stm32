#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>

#define MSG_IN_RESET  0
#define MSG_IN_COUNT  1

#define MSG_OUT_MESSAGE 0

void cmd_reset(uint32_t msgsize, hal_usart_t* usart);
void put_message(hal_usart_t* usart, const char* msg);

static char* resetmsg = "Resetting\n\r";
static char* listenmsg = "Listening\n\r";

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wstringop-overread"
void put_message(hal_usart_t* usart, const char* msg)
{
 uint32_t hb = MSG_OUT_MESSAGE, size;
 size = strnlen(msg, 100);
 hal_usart_send(usart, (uint8_t*)&hb, 4);
 hal_usart_send(usart, (uint8_t*)&size, 4);
 hal_usart_send(usart, (uint8_t*)msg, size);
}
#pragma GCC diagnostic pop

void cmd_reset(uint32_t, hal_usart_t* usart)
{
 put_message(usart, resetmsg);
 vTaskDelay(500 / portTICK_PERIOD_MS);
 hal_reset();
}

typedef void (*msg_handler)(uint32_t msgsize, hal_usart_t* usart);

msg_handler handlers[MSG_IN_COUNT] = {cmd_reset};

static void cmdlisten(void *args __attribute((unused)))
{
 uint32_t msgid, msgsize;

 put_message(&cmdcnt, listenmsg);

 for(;;)
   {
   msgid = hal_usart_read_uint32(&cmdcnt);
   msgsize = hal_usart_read_uint32(&cmdcnt);
   if(msgid < MSG_IN_COUNT)
       handlers[msgid](msgsize, &cmdcnt);
   else
       hal_usart_skip(&cmdcnt, msgsize);
   }
}

int main(void)
{
   hal_init();

   xTaskCreate(cmdlisten, "CmdLst", 200, NULL, configMAX_PRIORITIES-1,NULL);
   vTaskStartScheduler();

   for (;;);
   return 0;
}