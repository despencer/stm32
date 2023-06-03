#include <libopencm3/stm32/rcc.h>
#include "opencm3hal.h"

// setups the clock at default speed
void hal_setup_clock(void)
{
  rcc_clock_setup_pll(&rcc_hse_25mhz_3v3[RCC_CLOCK_3V3_96MHZ]);
}