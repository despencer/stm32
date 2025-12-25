#include "slpx.h"
#include "FreeRTOS.h"
#include "task.h"

#define SLPX_BYTE_START      0xF0    // a start byte
#define SLPX_BYTE_ESCAPE     0xF1    // an escape byte
#define SLPX_BYTE_ESC_START  0xF2    // a substitute for a start byte
#define SLPX_BYTE_ESC_ESC    0xF3    // a substitute for an escape byte

void slpx_send_byte(slpx_t* slpx, uint8_t data);
uint8_t slpx_read_byte(slpx_t* slpx, uint8_t data);

static void slpx_listen(void *args)
{
 slpx_t* slpx;
 slpx = (slpx_t*)args;

 slpx_send(slpx, SLPX_OPEN, NULL, 0);

 for(;;)
  {
   hal_usart_read(slpx->usart);
  }
}

void slpx_init(slpx_t* slpx, const char* readername)
{
 slpx->xor_tx = 0;
 hal_mutex_create(slpx->tx_mutex);
 slpx->status = SLPX_STATUS_NONE;
 xTaskCreate(slpx_listen, readername, 200, slpx, configMAX_PRIORITIES-1,NULL);
}

void slpx_send_byte(slpx_t* slpx, uint8_t data)
{
 if(data == SLPX_BYTE_START)
    { hal_usart_send_byte(slpx->usart, SLPX_BYTE_ESCAPE); hal_usart_send_byte(slpx->usart, SLPX_BYTE_ESC_START); }
 else if(data == SLPX_BYTE_ESCAPE)
    { hal_usart_send_byte(slpx->usart, SLPX_BYTE_ESCAPE); hal_usart_send_byte(slpx->usart, SLPX_BYTE_ESC_ESC); }
 else
    hal_usart_send_byte(slpx->usart, data);
 slpx->xor_tx ^= data;
}

void slpx_send(slpx_t* slpx, uint16_t funcid, uint8_t* buf, size_t buflen)
{
 unsigned int i;
 hal_mutex_lock(slpx->tx_mutex);
 slpx->xor_tx = 0;

 hal_usart_send_byte(slpx->usart, SLPX_BYTE_START);
 slpx_send_byte(slpx, (uint8_t)(funcid&0xFF) );
 slpx_send_byte(slpx, (uint8_t)((funcid>>8)&0xFF) );
 slpx_send_byte(slpx, (uint8_t)(buflen&0xFF) );
 slpx_send_byte(slpx, (uint8_t)((buflen>>8)&0xFF) );
 for(i=0; i<buflen; i++)
    slpx_send_byte(slpx, buf[i]);
 slpx_send_byte(slpx, slpx->xor_tx);
 hal_mutex_unlock(slpx->tx_mutex);
}