from machine import Pin, I2C
import time
import random
import ssd1306
from sx1262 import SX1262

#Transmitter and Receiver code for heltec v3 
#Change the last lines of code

# ========================================
# OLED POWER
# ========================================

vext = Pin(36, Pin.OUT)
vext.value(0)

time.sleep_ms(1000)


# ========================================
# OLED RESET
# ========================================

oled_rst = Pin(21, Pin.OUT)

oled_rst.value(0)
time.sleep_ms(100)

oled_rst.value(1)
time.sleep_ms(500)


# ========================================
# I2C
# ========================================

i2c = I2C(
    0,
    scl=Pin(18),
    sda=Pin(17),
    freq=100000
)


# ========================================
# OLED
# ========================================

oled = ssd1306.SSD1306_I2C(
    128,
    64,
    i2c,
    addr=0x3C
)


def display(line1="", line2="", line3="", line4=""):

    oled.fill(0)

    oled.text(line1, 0, 0)
    oled.text(line2, 0, 16)
    oled.text(line3, 0, 32)
    oled.text(line4, 0, 48)

    oled.show()


# ========================================
# START
# ========================================

display(
    "LoRa",
    "Transmitter",
    "Starting...",
    ""
)

time.sleep(1)


# ========================================
# SX1262
# ========================================

sx = SX1262(
    spi_bus=1,
    clk=9,
    mosi=10,
    miso=11,
    cs=8,
    irq=14,
    rst=12,
    gpio=13
)


status = sx.begin(
    freq=434.0,
    bw=125.0,
    sf=7,
    cr=5,
    syncWord=0x12,
    power=5,
    currentLimit=60.0,
    preambleLength=8,
    implicit=False,
    implicitLen=0xFF,
    crcOn=True,
    txIq=False,
    rxIq=False,
    tcxoVoltage=1.7,
    useRegulatorLDO=False,
    blocking=True
)


display(
    "TRANSMITTER",
    "LoRa ready",
    "Status:",
    str(status)
)

time.sleep(2)


# ========================================
# TRANSMITTER LOOP
# ========================================

while True:

    # Generate random number
    number = random.randint(0, 9999)

    # Convert number to bytes
    message = str(number).encode()

    # Show on OLED
    display(
        "TRANSMITTER",
        "Sending:",
        str(number),
        ""
    )

    # Send packet
    length, tx_status = sx.send(message)

    # Show result
    display(
        "TRANSMITTER",
        "Sent:",
        str(number),
        "Status: " + str(tx_status)
    )

    # Random 5s
    delay = 5
    time.sleep(delay)

'''
# ========================================
# RECEIVER LOOP
# ========================================

while True:

    display(
        "RECEIVER",
        "Waiting...",
        "",
        ""
    )

    # Wait for packet
    data, rx_status = sx.recv()

    if data:

        try:
            number = data.decode()
        except:
            number = str(data)

        display(
            "RECEIVER",
            "Received:",
            number,
            "Status: " + str(rx_status)
        )

        # Keep result on screen for 2 seconds
        time.sleep(2)
'''
