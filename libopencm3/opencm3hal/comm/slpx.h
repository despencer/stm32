#ifndef SLPX_H
#define SLPX_H

#include <halusart.h>

#define SLPX_INFORMATION 0x01
#define SLPX_TELEMETRY   0x02
#define SLPX_OPEN        0x0102
#define SLPX_HEARTBEAT   0x0402

typedef struct slpx_s {
   hal_usart_t* usart;
   uint8_t xor_tx;
} slpx_t;


void slpxs_init(void);
void slpx_open(slpx_t* usart);

void slpx_send(slpx_t* usart, uint16_t funcid, uint8_t* buf, size_t buflen);

#endif