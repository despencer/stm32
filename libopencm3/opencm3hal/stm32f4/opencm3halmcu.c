#include "opencm3hal.h"

#define BOOTLOADER_ADDRESS (0x1FFF0000)
#define BOOTLOADER_JUMP    (0x1FFF0004)

typedef void (*funcjump)(void);

__attribute__((always_inline)) static inline void __set_MSP(uint32_t topOfMainStack)
{
  __asm volatile ("MSR msp, %0" : : "r" (topOfMainStack) : );
}

funcjump volatile jumpbl;

void hal_jump_to_bootloader(void)
{
 jumpbl = (funcjump)(*(uint32_t*)BOOTLOADER_JUMP);
// asm("move r13,a");
// __regMainStackPointer = BOOTLOADER_ADDRESS;
 __set_MSP( *(uint32_t*)BOOTLOADER_ADDRESS);
 jumpbl();
 while(1);
}