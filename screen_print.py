#To set and print in the screen using ssd1306

from machine import Pin, I2C
import time
import ssd1306

# --------------------------------
# OLED POWER
# --------------------------------
vext = Pin(36, Pin.OUT)
vext.value(0)

# Give OLED power time to stabilize
time.sleep_ms(1000)

# --------------------------------
# OLED RESET
# --------------------------------
oled_rst = Pin(21, Pin.OUT)

oled_rst.value(0)
time.sleep_ms(100)
oled_rst.value(1)
time.sleep_ms(500)

# --------------------------------
# I2C
# --------------------------------
i2c = I2C(
    0,
    scl=Pin(18),
    sda=Pin(17),
    freq=100000
)

devices = i2c.scan()
print("I2C devices:", devices)

# --------------------------------
# OLED
# --------------------------------
if 60 not in devices:
    print("OLED not detected!")
else:
    oled = ssd1306.SSD1306_I2C(
        128,
        64,
        i2c,
        addr=0x3C
    )

    oled.fill(0)

    oled.text("HELTEC V3", 0, 0)
    oled.text("MicroPython OK", 0, 16)
    oled.text("OLED OK", 0, 32)
    oled.text("I2C: 0x3C", 0, 48)

    oled.show()

    print("OLED initialized successfully")
