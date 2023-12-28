import machine
import utime
import time
from machine import Pin
import rp2

max_lum =100
r=0
g=0
b=0

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_LEFT, autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    wrap_target()
    label("bitloop")
    out(x, 1)               .side(0)    [T3 - 1]
    jmp(not_x, "do_zero")   .side(1)    [T1 - 1]
    jmp("bitloop")          .side(1)    [T2 - 1]
    label("do_zero")
    nop()                   .side(0)    [T2 - 1]
    wrap()


# Create the StateMachine with the ws2812 program, outputting on Pin(4).
sm = rp2.StateMachine(0, ws2812, freq=8_000_000, sideset_base=Pin(25))

# Start the StateMachine, it will wait for data on its FIFO.
sm.active(1)

def make_color(r, g, b):  
    rgb =(g<<24) | (r<<16) | (b<<8)
    sm.put(rgb)
    
def test_color(g, r, b):
    make_color(g, r, b)

uart1 = machine.UART(1, baudrate=9600, tx=8, rx=9, timeout=1000, timeout_char=1000)

while True:
    #line reader - if data is in the RP2040 buffer, then it will read the line
    if uart1.any():
        print(uart1.readline())
    #LED indicator - illustrate power is on
    test_color(100, 100, 100)
    time.sleep_ms(500)
    test_color(0, 100, 0)
    time.sleep_ms(500)