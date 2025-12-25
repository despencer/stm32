#ifndef SLPX_H
#define SLPX_H

#include <stdbool.h>
#include <halusart.h>
#include <halmutex.h>

#define SLPX_INFORMATION 0x01
#define SLPX_TELEMETRY   0x02
#define SLPX_OPEN        0x0102
#define SLPX_HEARTBEAT   0x0402
#define SLPX_OPEN_ACK    0x0502

#define SLPX_STATUS_NONE 0
#define SLPX_CONNECTED 0x01

typedef struct slpx_s {
   hal_usart_t* usart;
   uint8_t xor_tx;
   hal_mutex_t* tx_mutex;
   uint8_t xor_rx;
   uint8_t status;
} slpx_t;


void slpxs_init(void);
void slpx_init(slpx_t* slpx, const char* readername);

void slpx_send(slpx_t* slpx, uint16_t funcid, uint8_t* buf, size_t buflen);

#endif