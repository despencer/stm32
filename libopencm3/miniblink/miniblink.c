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
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>

static void
gpio_setup(void) {

	/* Enable GPIOC clock. */
	rcc_periph_clock_enable(RCC_GPIOC);

	/* Set GPIO8 (in GPIO port C) to 'output push-pull'. */
#ifdef STM32F1
    gpio_set_mode(GPIOC, GPIO_MODE_OUTPUT_2_MHZ, GPIO_CNF_OUTPUT_PUSHPULL, GPIO13);
#else
    gpio_mode_setup(GPIOC, GPIO_MODE_OUTPUT, GPIO_PUPD_NONE, GPIO13);
#endif
}

void blink(bool length);

int
main(void) {
	int i;

	gpio_setup();

	for (;;) {
		blink(true); blink(true); blink(true);
		blink(false); blink(false); blink(false);
		blink(true); blink(true); blink(true);
		for (i = 0; i < 3000000; i++)	/* Wait a bit. */
			__asm__("nop");
	}

	return 0;
}

void blink(bool length)
{
    int i;
    int wait;

    wait = length?2500000:50000;

	gpio_clear(GPIOC,GPIO13);	/* LED on */
	for (i = 0; i < wait; i++)	/* Wait a bit. */
		__asm__("nop");

	gpio_set(GPIOC,GPIO13);		/* LED off */
	for (i = 0; i < 500000; i++)	/* Wait a bit. */
		__asm__("nop"); 
}