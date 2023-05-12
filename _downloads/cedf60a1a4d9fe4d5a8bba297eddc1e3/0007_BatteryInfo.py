#!/usr/bin/env python3

import datetime
import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

import PluginsPy

@PluginsPy.addRun
class BatteryInfo:

    """
    绘制PowerZ数据曲线

    @input(default/batteryInfo_20221003051117.txt): zcv数据
    """

    def __init__(self, kwargs):

        filename = kwargs["input"]

        # 2022-10-03 05:11:17, soc: 0, bat: 0.000000, vout: 3448.000000, charge: 3.571429, discharge: 0.000000
        self.lineInfos = LogParser.logFileParser(
                filename,
                r'(.*), soc: (\d*), bat: (\d*\.\d*), vout: \d*\.\d*, charge: (\d*\.\d*)',
                callback=self.defaultLineCallback
            )
        for info in self.lineInfos:
            print(info)

        self.labels = ["SOC(%)", "BAT Voltage(mV)", "Charge Current(mA)"]
        self.customData = {"xlabel": "X", "ylabel": "Y"}
        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 3)

    def defaultShowCallback(self, fig, index):
        ax = fig.get_axes()[index]
        ax.set_xlabel(self.customData["xlabel"])
        ax.set_ylabel(self.customData["ylabel"])

        ax.plot([s[0] for s in self.lineInfos], [s[index + 1] for s in self.lineInfos], label = self.labels[index])

        ax.legend()

    def defaultLineCallback(self, lineInfo):
        lineInfoFixed = []
        print(lineInfo)
        for index in range(len(lineInfo)):
            if index == 0:
                currentDate = datetime.datetime.strptime(lineInfo[index], "%Y-%m-%d %H:%M:%S")
                lineInfoFixed.append(currentDate)
            else:
                lineInfoFixed.append(float(lineInfo[index].strip()))
        
        return lineInfoFixed

if __name__ == "__main__" :
    print("main")
