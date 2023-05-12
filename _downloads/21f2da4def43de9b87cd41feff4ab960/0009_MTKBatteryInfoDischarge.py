#!/usr/bin/env python3

import datetime
from turtle import color
import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

import PluginsPy

@PluginsPy.addRun
class MTKBatteryInfoDischarge:

    """
    MTK放电数据曲线

    @input(default/mtk_battery_info.txt): 放电数据
    """

    def __init__(self, kwargs):

        filename = kwargs["input"]

        # <5>[  313.509051]  (0)[235:battery_thread]car[-30,251,-251,50,-259] tmp:30 soc:100 uisoc:97 vbat:4297 ibat:-2762 algo:0 gm3:0 0 0 0,boot:0
        self.lineInfos = LogParser.logFileParser(
                filename,
                r'\[\s*(\d*\.\d*)\].*\d*\:battery_thread.*tmp:(\d*) soc:(\d*) uisoc:(\d*) vbat:(\d*) ibat:([-]?\d*)',
                callback=self.defaultLineCallback,
                fileEncode="ISO-8859-1"
            )
        for info in self.lineInfos:
            print(info)

        self.labels = ["Temperature", "SOC(%)", "UISOC(%)", "BAT Voltage(mV * 10)", "Discharge Current(mA * 10)"]
        self.customData = {"xlabel": "X", "ylabel": "Y"}
        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 2, cols = 3)

    def defaultShowCallback(self, fig, index):
        ax = fig.get_axes()[index]
        ax.set_xlabel(self.customData["xlabel"])
        ax.set_ylabel(self.customData["ylabel"])

        if index == 5:
            ax.plot([s[0] for s in self.lineInfos], [s[4] for s in self.lineInfos], color="r")
            ax2 = ax.twinx()
            ax2.plot([s[0] for s in self.lineInfos], [s[5] for s in self.lineInfos], color="b")
            ax2.set_ylabel(self.customData["ylabel"])
        else:
            ax.plot([s[0] for s in self.lineInfos], [s[index + 1] for s in self.lineInfos], label = self.labels[index])

        ax.legend()

    def defaultLineCallback(self, lineInfo):
        lineInfoFixed = []
        print(lineInfo)
        for index in range(len(lineInfo)):
            lineInfoFixed.append(float(lineInfo[index].strip()))
        
        return lineInfoFixed

if __name__ == "__main__" :
    print("main")
