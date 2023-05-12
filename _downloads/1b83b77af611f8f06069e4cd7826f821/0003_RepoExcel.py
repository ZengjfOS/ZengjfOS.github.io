#!/usr/bin/env python3

import datetime
from datetime import timedelta
from xmlrpc.client import FastParser
import PluginsPy
import os
import xlwt

from tools.ShellCMD import Shell

@PluginsPy.addRun
class RepoExcel:

    """
    处理二进制文件

    @dir(../../android/merge/): input dir
    @last(7): 最后几天时间
    """

    def __init__(self, kwargs):

        repoDir = kwargs["dir"]
        lastDates = kwargs["last"]

        # 定义用户
        authors = ["anhengxuan", "chenfujun", "huangjiangwei"]
        authorsCommits = {}
        for authorName in authors:
            authorsCommits[authorName] = []

        now = datetime.datetime.now()
        # 从上周一开始算
        # lastWeekStart = now - timedelta(days=now.weekday() + int(lastDates))
        # 最近7天
        lastWeekStart = now - timedelta(int(lastDates))
        lastWeek = lastWeekStart.strftime("%Y-%m-%d 00:00")
        print(lastWeek)

        # 设置环境变量
        os.environ['dateInfo'] = lastWeek

        # 跳转目录
        workDir = os.getcwd()
        os.chdir(repoDir)
        print(os.getcwd())

        # 获取repo commit信息
        shellRet = Shell("repo", "forall", "-c", 'echo "# `basename $PWD`";echo;echo "commit id | date | author name | module | commit log";echo "---|---|---|---|---";git log --after "${dateInfo}" --pretty=format:"%H | %ai | %ae | `basename $PWD` | %s";echo;echo;echo;')

        # 跳转目录
        os.chdir(workDir)
        print(os.getcwd())

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

        currentSheet = None
        commitStart = False
        gitRepoStart = False
        row = 1
        for line in shellRet.splitlines():

            if line.startswith("# "):
                gitRepoStart = False
                commitStart = False
                name = line.strip()[2:]

                if not name in ["kernel-4.19", "device", "vendor"]:
                    continue

                # add same sheet[0] name to output file from input file sheet[0] name, we just analyze sheet[0]
                currentSheet = outputBomXL.add_sheet(name, cell_overwrite_ok = True)
                currentSheet.write(0, 0, "Commit id", style)
                currentSheet.col(0).width = 256 * 40
                currentSheet.write(0, 1, "date", style)
                currentSheet.col(1).width = 256 * 30
                currentSheet.write(0, 2, "author name", style)
                currentSheet.col(2).width = 256 * 30
                currentSheet.write(0, 3, "module", style)
                currentSheet.col(3).width = 256 * 10
                currentSheet.write(0, 4, "commit log", style)
                currentSheet.col(4).width = 256 * 120

                row = 1
                gitRepoStart = True
            elif gitRepoStart and "---|---|---|---|---" in line:
                commitStart = True
            elif commitStart and " | " in line:
                commitInfo = line.split(" | ")
                if len(commitInfo) == 5:

                    for col in range(5):
                        currentSheet.write(row, col, commitInfo[col], leftStyle)
                        currentSheet.row(row).height = 20 * 40
                    
                    authorName = commitInfo[2].split("@")[0]
                    if authorName in authors:
                        authorsCommits[authorName].append(commitInfo)

                    row += 1
            else:
                pass

        outputBomXL.save("output/week_commit_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xls")


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

        for authorName in authors:
            # add same sheet[0] name to output file from input file sheet[0] name, we just analyze sheet[0]
            currentSheet = outputBomXL.add_sheet(authorName, cell_overwrite_ok = True)
            currentSheet.write(0, 0, "Commit id", style)
            currentSheet.col(0).width = 256 * 40
            currentSheet.write(0, 1, "date", style)
            currentSheet.col(1).width = 256 * 30
            currentSheet.write(0, 2, "author name", style)
            currentSheet.col(2).width = 256 * 30
            currentSheet.write(0, 3, "module", style)
            currentSheet.col(3).width = 256 * 10
            currentSheet.write(0, 4, "commit log", style)
            currentSheet.col(4).width = 256 * 120

            row = 1
            for commitInfo in authorsCommits[authorName]:
                for col in range(5):
                    currentSheet.write(row, col, commitInfo[col], leftStyle)
                    currentSheet.row(row).height = 20 * 40
                
                row += 1

        outputBomXL.save("output/week_bsp_" + datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".xls")

if __name__ == '__main__':
    RepoExcel({"dir": "../../android/merge/", "last": 120})
