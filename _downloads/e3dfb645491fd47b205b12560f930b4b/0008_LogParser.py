#!/usr/bin/env python3

import re
import datetime

def defaultLineCallback(lineInfo):
    lineInfoFixed = []
    for index in range(len(lineInfo)):
        lineInfoFixed.append(lineInfo[index].strip())
    
    return lineInfoFixed

def logFileParser(file = None, regex = None , callback=defaultLineCallback, fileEncode = "utf-8"):

    lineInfos = []
    if file != None and isinstance(file, str) and (regex != None):
        with open(file, mode = "r", encoding = fileEncode) as fd:
            for line in fd:
                line = line.strip()

                foundList = re.findall(regex, line, re.M | re.I)
                if foundList:
                    if callback != None:
                        # 一行文字可能存在多个匹配的，目前只取一个匹配的
                        if len(foundList) == 1:
                            lineInfos.append(callback([s.strip() for s in foundList[0]]))
    else:
        return None
    
    return lineInfos

def floatLineCallback(lineInfo):
    lineInfoFixed = []
    for index in range(len(lineInfo)):
        lineInfoFixed.append(float(lineInfo[index].strip()))
    
    return lineInfoFixed

def dateLineCallback(lineInfo):
    lineInfoFixed = []
    for index in range(len(lineInfo)):
        if index == 0:
            continue

        if index == 1:
            timeString = "2021-" + lineInfo[0] + " " + lineInfo[index].split(".")[0]
            currentDate = datetime.datetime.strptime(timeString.split(".")[0], "%Y-%m-%d %H:%M:%S")
            lineInfoFixed.append(currentDate)
            continue

        lineInfoFixed.append(lineInfo[index].strip())
    
    return lineInfoFixed

if __name__ == "__main__":
    # 298.039308 :    1-swapper/0       : initcall: init_menu    16.019692ms
    # 15932.513576 : 1138-android.bg      : AP_Launch: com.android.settings/.FallbackHome 756ms
    lineInfos = logFileParser("default/Android_Q_bootprof.txt", r'(\d+.\d+)\s+:(.*):\s+(\w*):\s*(.*)')
    for info in lineInfos:
        print(info)

    # 2705    42248   1025
    lineInfos = logFileParser(
            "default/zcv.txt",
            r'(\d+)\s+(\d+)\s+(\d+)',
            callback=floatLineCallback
        )
    for info in lineInfos:
        print(info)

    # 06-29 09:37:46.551252  2283  2283 I DebugLoggerUI/MainActivity: onPause
    lineInfos = logFileParser(
            "default/AndroidSystemWakeup.curf", 
            r'(\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\.\d*)\s+\d+\s+\d+\s+\w+\s+(.*)',
            callback=dateLineCallback
            )
    for info in lineInfos:
        print(info)
