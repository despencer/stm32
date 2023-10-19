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
#include <opencm3hal.h>

#include "trafficlights.h"

static void maintask(void *args __attribute((unused)))
{
 for (;;)
  {
    int i;

    hal_gpio_set(TL_RED_PORT, TL_RED_PIN);
    vTaskDelay(3000);
    hal_gpio_set(TL_YELLOW_PORT, TL_YELLOW_PIN);
    vTaskDelay(1000);
    hal_gpio_clear(TL_RED_PORT, TL_RED_PIN);
    hal_gpio_clear(TL_YELLOW_PORT, TL_YELLOW_PIN);
    hal_gpio_set(TL_GREEN_PORT, TL_GREEN_PIN);
    vTaskDelay(3000);
    for(i=0; i<5; i++)
        {
        hal_gpio_toggle(TL_GREEN_PORT, TL_GREEN_PIN);
        vTaskDelay(750);
        }
    hal_gpio_set(TL_YELLOW_PORT, TL_YELLOW_PIN);
    vTaskDelay(1000);
    hal_gpio_clear(TL_YELLOW_PORT, TL_YELLOW_PIN);
  }
}

int main(void)
{
   hal_init();

   hal_gpio_open(TL_RED_PORT, TL_RED_PIN, HAL_GPIO_MODE_OUTPUT | HAL_GPIO_PUPD_NONE);
   hal_gpio_open(TL_YELLOW_PORT, TL_YELLOW_PIN, HAL_GPIO_MODE_OUTPUT | HAL_GPIO_PUPD_NONE);
   hal_gpio_open(TL_GREEN_PORT, TL_GREEN_PIN, HAL_GPIO_MODE_OUTPUT | HAL_GPIO_PUPD_NONE);

    xTaskCreate(maintask, "MAIN", 200, NULL, configMAX_PRIORITIES-1,NULL);
    vTaskStartScheduler();

    for (;;);
    return 0;
}