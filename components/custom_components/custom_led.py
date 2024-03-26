import dash_daq as daq
from components.colors import *


def create_led(nstr):
    led = daq.LEDDisplay(value=nstr, color=trend_color, size=30)
    return led
