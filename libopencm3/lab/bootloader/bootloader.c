#include "FreeRTOS.h"
#include "task.h"

#include <opencm3hal.h>
#include <string.h>

#define MSG_IN_RESET  0
#define MSG_IN_BOOTLOADER 1
#define MSG_IN_COUNT  2

#define MSG_OUT_MESSAGE 0
#define MSG_OUT_BOOTLOADER 1

void cmd_reset(uint32_t msgsize, hal_usart_t* usart);
void cmd_bootloader(uint32_t msgsize, hal_usart_t* usart);
void put_message(hal_usart_t* usart, const char* msg);

static char* resetmsg = "Resetting\n";
char listenmsg[] = "Listening\n";
volatile uint32_t version = 2;

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

void cmd_bootloader(uint32_t, hal_usart_t* usart)
{
 uint32_t hb = MSG_OUT_BOOTLOADER, size=0;
 hal_usart_send(usart, (uint8_t*)&hb, 4);
 hal_usart_send(usart, (uint8_t*)&size, 4);
 vTaskDelay(500 / portTICK_PERIOD_MS);
 hal_write_backup_register(0, 1);
 hal_reset();
}

typedef void (*msg_handler)(uint32_t msgsize, hal_usart_t* usart);

msg_handler handlers[MSG_IN_COUNT] = {cmd_reset, cmd_bootloader};

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
   if(hal_read_backup_register(0) != 0)
      {
      hal_write_backup_register(0, 0);
      hal_jump_to_bootloader();
      }
   hal_init();

   xTaskCreate(cmdlisten, "CmdLst", 200, NULL, configMAX_PRIORITIES-1,NULL);
   vTaskStartScheduler();

   version++;  // just for reference
   for (;;);
   return 0;
}