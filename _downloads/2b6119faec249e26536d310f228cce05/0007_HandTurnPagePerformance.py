#!/usr/bin/env python3

import matplotlib.pyplot as plt
import PluginsPy
import datetime

@PluginsPy.addRun
class HandTurnPagePerformance:

    """
    可视化Hand Turn Page的帧处理时间效率

    @data(default/HandTurnPagePerformance.txt): mediapipe数据
    """

    def __init__(self, kwargs):
        data = kwargs["data"]

        with open(data, "r") as fp:
            startFrameTime = -1
            frameTime = None
            frameTimes = []

            for line in fp:
                if "HandTurnPagePerformance" in line:
                    lineArray = line.split()
                    print(lineArray)
                    print(lineArray[1].split(".")[0])
                    currentTime = (datetime.datetime.strptime(lineArray[1].split(".")[0], "%H:%M:%S") - datetime.datetime(1900,1,1)).total_seconds()
                    print(currentTime)
                    currentTime += float("0." + lineArray[1].split(".")[1])
                    print(currentTime)

                    if "Get Frame From Camera Over" in line:
                        if startFrameTime == -1:
                            startFrameTime = currentTime
                            frameTime = []
                            frameTime.append(currentTime)
                    elif "End Of MediaPipe Processed" in line:
                        if frameTime != None:
                            frameTime.append(currentTime - startFrameTime)
                    elif "End Of HandTurnPage Processed" in line:
                        if frameTime != None:
                           frameTime.append(currentTime - startFrameTime)
                           if len(frameTime) == 3:
                               frameTimes.append(frameTime)
                        
                           startFrameTime = -1
                           frameTime = None
                    else:
                        pass

            print(frameTimes)

            x = []
            y1 = []
            y2 = []

            for frame in frameTimes:
                x.append(frame[0])
                y1.append(frame[1])
                y2.append(frame[2])

                plt.plot([frame[0], frame[0]], [0, frame[1]], c="blue")
                plt.scatter(frame[0], frame[2], c="red")
            
            print(x)
            print(y1)
            print(y2)

            # plt.plot(x, y1, c='blue')
            # plt.plot(x, y2, c='red')
            plt.show()


if __name__ == "__main__":
    HandTurnPagePerformance({"mode":"pointer"})
