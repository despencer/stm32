#ifndef HAL_USART_H
#define HAL_USART_H
// This file is a mapper between common interface and specific HAL interface

#include <stddef.h>
#include <stdint.h>

typedef struct hal_usart_s hal_usart_t;

void hal_usarts_init(void);
void hal_usart_send(hal_usart_t* usart, uint8_t* buf, size_t buflen);
void hal_usart_send_byte(hal_usart_t* usart, uint8_t data);
uint8_t hal_usart_read(hal_usart_t* usart);
uint32_t hal_usart_read_uint32(hal_usart_t* usart);
void hal_usart_read_buf(hal_usart_t* usart, uint8_t* buf, size_t buflen);
void hal_usart_skip(hal_usart_t* usart, size_t buflen);

#endif
