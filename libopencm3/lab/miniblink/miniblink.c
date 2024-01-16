#include <stdbool.h>
#include <opencm3hal.h>

void blink(bool length);

int main(void)
{
 int i;

 hal_init();
 for (;;)
    {
      blink(true); blink(true); blink(true);
      blink(false); blink(false); blink(false);
      blink(true); blink(true); blink(true);
      for (i = 0; i < 10000000; i++)	
             __asm__("nop");
    }

 return 0;
}

void blink(bool length)
{
  int i;
  int wait;

  wait = length?10000000:200000;

  hal_output_clear(&indicator);
  for (i = 0; i < wait; i++)
     __asm__("nop");

  hal_output_set(&indicator);
  for (i = 0; i < 2000000; i++)
     __asm__("nop"); 
}