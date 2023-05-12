#!/usr/bin/env python3

from smbus import SMBus
from time import sleep
from datetime import datetime

i2cbus = SMBus(1)  # Create a new I2C bus
i2caddress = 0x3c  # Address of SW6106 device

outputFile = "batteryInfo_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".txt"
with open(outputFile, "w") as out:
    while True:
        print("---------------------------------------")

        try:
            batLow = i2cbus.read_byte_data(i2caddress, 0x14)
            voutBatHigh = i2cbus.read_byte_data(i2caddress, 0x15)
            voutLow = i2cbus.read_byte_data(i2caddress, 0x16)
        except:
            print("get SW6106 data from i2c bus error")
            continue

        bat = (((voutBatHigh & 0x0f) << 8) | (batLow & 0xff))
        vout = ((((voutBatHigh & 0x0f0) >> 4) << 8) | voutLow)

        batVoltage = bat * 1.2
        voutVoltage = vout * 4

        print("batLow, voutBatHigh, voutLow: 0x%x, 0x%x, 0x%x" % (batLow, voutBatHigh, voutLow))
        print("bat, batVoltage, 0x%x, %f" % (bat, batVoltage))
        print("vout, voutVoltage, 0x%x, %f" % (vout, voutVoltage))

        chargeCurrentLow = i2cbus.read_byte_data(i2caddress, 0x17)
        dischargeChargeCurrentHigh = i2cbus.read_byte_data(i2caddress, 0x18)
        dischargCurrentLow = i2cbus.read_byte_data(i2caddress, 0x19)

        charge = (((dischargeChargeCurrentHigh & 0x0f) << 8) | (chargeCurrentLow & 0xff))
        discharge = ((((dischargeChargeCurrentHigh & 0x0f0) >> 4) << 8) | dischargCurrentLow)

        chargeCurrent = charge * 25 / 7.0
        dischargeCurrent = discharge * 25 / 7.0

        print("chargeCurrentLow, dischargeChargeCurrentHigh, dischargCurrentLow: 0x%x, 0x%x, 0x%x" % (chargeCurrentLow, dischargeChargeCurrentHigh, dischargCurrentLow))
        print("charge, batVoltage, 0x%x, %f" % (charge, chargeCurrent))
        print("discharge, voutVoltage, 0x%x, %f" % (discharge, dischargeCurrent))

        soc = i2cbus.read_byte_data(i2caddress, 0x4f)

        print("soc: %d" % (soc & 0x7f))

        outputLine = "%s, soc: %d, bat: %f, vout: %f, charge: %f, discharge: %f\n"  % (\
                datetime.today().strftime('%Y-%m-%d %H:%M:%S'), \
                soc, \
                batVoltage, \
                voutVoltage, \
                chargeCurrent, \
                dischargeCurrent
            )

        out.write(outputLine)
        out.flush()

        sleep(1)

