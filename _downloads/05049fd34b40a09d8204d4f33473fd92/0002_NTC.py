#!/usr/bin/env python3

from smbus import SMBus
from time import sleep

RTTable = (
    (-30 , 181.71),
    (-25 , 133.31),
    (-20 , 98.88 ),
    (-15 , 74.10 ),
    (-10 , 56.06 ),
    (-5  , 42.80 ),
    (0   , 98.96 ),
    (5   , 25.58 ),
    (10  , 20.00 ),
    (15  , 15.76 ),
    (20  , 12.51 ),
    (25  , 10.00 ),
    (30  , 8.048 ),
    (35  , 6.518 ),
    (40  , 5.312 ),
    (45  , 4.354 ),
    (50  , 3.588 ),
    (55  , 2.974 ),
    (60  , 2.476 ),
    (65  , 2.072 ),
    (70  , 1.743 ),
    (75  , 1.473 ),
    (80  , 1.250 ),
    (85  , 1.065 ),
    (90  , 0.911 ),
    (95  , 0.7825),
    (100 , 0.6745),
    (105 , 0.5837),
    (110 , 0.5066),
)

i2cbus = SMBus(1)  # Create a new I2C bus
i2caddress = 0x3c  # Address of SW6106 device

while True:
    print("---------------------------------------")

    chipTemeratureLow = i2cbus.read_byte_data(i2caddress, 0x1a)
    chipNTCtemperature = i2cbus.read_byte_data(i2caddress, 0x1b)
    ntctemperatureLow = i2cbus.read_byte_data(i2caddress, 0x1c)

    chipTempratue = ((((chipNTCtemperature & 0x0f) << 8) | (chipTemeratureLow & 0xff)) - 1851) * 1 / 6.82
    ntcResistance = ((((chipNTCtemperature & 0x0f0) >> 4) << 8) | ntctemperatureLow) / 1.1 /80

    print("chip low, ntc chip, ntc low: 0x%x, 0x%x, 0x%x" % (chipTemeratureLow, chipNTCtemperature, ntctemperatureLow))
    print("chip: 0x%x" % (((chipNTCtemperature & 0x0f) << 8) | (chipTemeratureLow & 0xff)))
    print("ntc: 0x%x" % ((((chipNTCtemperature & 0xf0) >> 4) << 8) | ntctemperatureLow))
    print("Resistance: " + str(ntcResistance))

    RTTableIndex = 0
    for index in range(len(RTTable)):
        if ntcResistance > RTTable[index][1]:
            RTTableIndex = index
            break

    print("RT - 1: " + str(RTTable[RTTableIndex - 1]))
    print("RT    : " + str(RTTable[RTTableIndex]))

    diffX = RTTable[RTTableIndex][0] - RTTable[RTTableIndex -  1][0]
    diffY = RTTable[RTTableIndex][1] - RTTable[RTTableIndex -  1][1]
    slope = diffY / diffX
    print("diffx, diffy, slope: " + str(diffX) + ", " + str(diffY) + ", " + str(slope))

    ntcResistanceDiffY = ntcResistance - RTTable[RTTableIndex -  1][1]
    print("chipTempratue: " + str(chipTempratue))
    print("ntcTemperature: " + str(RTTable[RTTableIndex -  1][0] + (ntcResistanceDiffY / slope)))

    sleep(1)

