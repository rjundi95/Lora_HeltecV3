#First main() so it can begin() the communication and set some parameters

from sx1262 import SX1262
import time

print("Initializing SX1262...")

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

print("SX1262 object created")

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

print("Status:", status)
print("SX1262 initialized successfully!")

while True:
    time.sleep(1)
