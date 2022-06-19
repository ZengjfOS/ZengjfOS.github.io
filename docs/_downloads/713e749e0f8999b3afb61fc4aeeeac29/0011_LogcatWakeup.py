import sys
from os import walk
import re
from matplotlib import pyplot as plt
import datetime

def getFiles() :

    f = []
    for (dirpath, dirnames, filenames) in walk("input") :
        dirpath = dirpath
        dirnames = dirnames

        for filename in filenames:
            if filename != "empty":
                if (filename.startswith("main_")):
                    f.append(filename)

    for file in f:
        print(file)

    return f

def main(argv=None) :

    inputFiles = getFiles()
    print(inputFiles)

    inputFilesCount = len(inputFiles)
    if (inputFilesCount > 0):
        for filename in inputFiles:

            wakeupCount = 0

            with open("input/" + filename, mode="r", encoding='UTF-8') as fd:
                for line in fd:
                    if line.strip().find("BatteryStatsService: In wakeup_callback: resumed from suspend") > -1:
                        # res = re.search(r'\d+:\d+:\d+\.\d+', line)
                        res = re.search(r'\d+-\d+\s\d+:\d+:\d+\.\d+', line.strip())
                        timeString = "2021-" + res.group(0).strip()
                        print(line.strip())
                        print(timeString)

                        wakeupCount += 1
                        
                        currentDate = datetime.datetime.strptime(timeString.split(".")[0], "%Y-%m-%d %H:%M:%S")
                        plt.text(currentDate, wakeupCount + 0.2, str(wakeupCount), fontsize=9)
                        plt.plot(currentDate, wakeupCount, 'o')
                        plt.plot([currentDate, currentDate], [wakeupCount, 0])

            print("wake up count: " + str(wakeupCount))

        plt.xlabel("X Date Time")
        plt.ylabel("Y Wakeup Number")
        plt.title("Logcat Wakeup Status Info")
        plt.show()

    else:
        print("Please check input file at input dir")


if __name__ == "__main__" :
    sys.exit(main())
