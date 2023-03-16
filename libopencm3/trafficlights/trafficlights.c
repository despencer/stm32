/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2009 Uwe Hermann <uwe@hermann-uwe.de>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */
#include "FreeRTOS.h"
#include "task.h"

#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>

void toggleloop(void);

void setled(void)
{
 gpio_clear(GPIOC,GPIO13);
}

void toggleloop(void)
{
// gpio_clear(GPIOC,GPIO13);
 int i;
 for (;;)
      {
        gpio_toggle(GPIOC,GPIO13);
        for (i = 0; i < 5000000; i++)	/* Wait a bit. */
            __asm__("nop"); 
      }

}

void vApplicationIdleHook(void)
{
//  gpio_clear(GPIOC,GPIO13);
}

extern void vApplicationTickHook(void)
{
//  gpio_clear(GPIOC,GPIO13);
}

static void maintask(void *args __attribute((unused)))
{
//  toggleloop();
    for (;;)
      {
        gpio_toggle(GPIOC,GPIO13);
        vTaskDelay(3000);
      }
}

static void gpio_setup(void)
{
    /* Enable GPIOC clock. */
    rcc_periph_clock_enable(RCC_GPIOC);

    /* Set GPIO8 (in GPIO port C) to 'output push-pull'. */
#ifdef STM32F1
    gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
#else
    gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13);
#endif
    gpio_set(GPIOC,GPIO13);
}

int main(void)
{
    rcc_clock_setup_pll(&rcc_hse_25mhz_3v3[RCC_CLOCK_3V3_96MHZ]);
    gpio_setup();
//    toggleloop();

    xTaskCreate(maintask, "MAIN", 200, NULL, configMAX_PRIORITIES-1,NULL);
//    setled();
    vTaskStartScheduler();
    gpio_clear(GPIOC,GPIO13);

    for (;;);
    return 0;
}