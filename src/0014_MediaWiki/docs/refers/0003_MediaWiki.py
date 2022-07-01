#!/usr/bin/env python3

from datetime import datetime
import string
import PluginsPy
import urllib.request
from urllib.parse import quote
import re
import datetime
import xlwt

@PluginsPy.addRun
class MediaWiki:
    """
    PluginExample类是一个编写LogTools插件的示例

    """

    def __init__(self, kwargs):

        # open BOM output file
        outputBomXL = xlwt.Workbook()
        style = xlwt.XFStyle()
        style.alignment.wrap = 1
        style.alignment.vert = xlwt.Alignment.VERT_CENTER
        style.alignment.horz = xlwt.Alignment.HORZ_CENTER

        leftStyle = xlwt.XFStyle()
        leftStyle.alignment.wrap = 1
        leftStyle.alignment.vert = xlwt.Alignment.VERT_CENTER
        leftStyle.alignment.horz = xlwt.Alignment.HORZ_LEFT

        names = [
                "曾剑锋"
            ]

        for name in names:
            url = quote("http://zengjf.local/index.php/" + name, safe=string.printable)
            content = urllib.request.urlopen(url, timeout=10).read().decode("utf-8")
            # print(content)

            """
            <h3><span id="2022.06.27_.7E_2022.07.03"></span><span class="mw-headline" id="2022.06.27_~_2022.07.03">2022.06.27 ~ 2022.07.03</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/index.php?title=%E6%9B%BE%E5%89%91%E9%94%8B&amp;action=edit&amp;section=3" title="编辑章节：2022.06.27 ~ 2022.07.03">编辑</a><span class="mw-editsection-bracket">]</span></span></h3>
            <ol><li>本周工作内容
            <ol><li>睡觉</li>
            <li>下周工作计划
            <ol><li>吃饭</li>
            <h3><span id="2022.06.20_.7E_2022.06.26"></span><span class="mw-headline" id="2022.06.20_~_2022.06.26">2022.06.20 ~ 2022.06.26</span><span class="mw-editsection"><span class="mw-editsection-bracket">[</span><a href="/index.php?title=%E6%9B%BE%E5%89%91%E9%94%8B&amp;action=edit&amp;section=4" title="编辑章节：2022.06.20 ~ 2022.06.26">编辑</a><span class="mw-editsection-bracket">]</span></span></h3>
            """
            start_captre_data = False
            interval = 1
            current_week_Flag = False
            current_week = []
            next_week_Flag = False
            next_week = []
            week_content_Flag = False

            for line in content.split("\n"):
                line = line.strip()

                matchObj = re.search( r'\d+[\./]\d+[\./]\d+[ ~/]+\d+[\./]\d+[\./]\d+', line, re.M|re.I)
                if matchObj:
                    if line.startswith("<h3><span id="):
                        data_array = re.split(">|<", line)
                        if len(data_array) > 9:
                            date_array = data_array[8].split(" ~ ")
                            if len(date_array) == 2:
                                # print(date_array[1])
                                interval = datetime.datetime.today() - datetime.datetime.strptime(date_array[1], "%Y.%m.%d")
                                if interval.days <= 0:
                                    start_captre_data = True
                                    print(date_array[1])
                                    continue
                                else:
                                    if start_captre_data:
                                        start_captre_data = False
                                        break
                                    else:
                                        print("赶紧让他写周报：" + name)
                                        exit(-1)

                if start_captre_data:
                    week_data = line.replace("<ol>", "").replace("<li>", "").replace("</ol>", "").replace("</li>", "")
                    if "本周" in week_data:
                        current_week_Flag = True
                        continue

                    if "下周" in week_data:
                        next_week_Flag = True
                        continue

                    if "<ol><li>" in line:
                        week_content_Flag = True
                    
                    if current_week_Flag:
                        if week_content_Flag:
                            current_week.append(week_data)
                    
                    if next_week_Flag:
                        if week_content_Flag:
                            next_week.append(week_data)

                    if "</li></ol>" in line:
                        current_week_Flag = False
                        next_week_Flag = False
                        week_content_Flag = False
            
            print(current_week)
            print(next_week)

            # add same sheet[0] name to output file from input file sheet[0] name, we just analyze sheet[0]
            currentSheet = outputBomXL.add_sheet(name, cell_overwrite_ok = True)
            currentSheet.write(0, 0, "NO.", style)
            currentSheet.col(0).width = 256 * 10
            currentSheet.write(0, 1, "时间", style)
            currentSheet.col(1).width = 256 * 40
            currentSheet.write(0, 2, "描述", style)
            currentSheet.col(2).width = 256 * 30

            i = 1
            currentSheet.write(i, 1, "本周工作内容", leftStyle)
            for work in current_week:
                print(work)

                currentSheet.write(i, 0, i, style)
                currentSheet.write(i, 2, work, leftStyle)

                i += 1

            currentSheet.write(i, 1, "下周工作计划", leftStyle)
            for work in next_week:
                print(work)

                currentSheet.write(i, 0, i, style)
                currentSheet.write(i, 2, work, leftStyle)

                i += 1

        outputBomXL.save("week_works_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xls")


if __name__ == "__main__" :
    MediaWiki({})
