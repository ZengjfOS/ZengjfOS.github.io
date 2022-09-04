import os
import shutil
from datetime import date

from os import path

def main():
    exePath = os.path.abspath(__file__)
    folder = os.path.dirname(exePath)
    currentFolder = os.getcwd()
    templateFolder = os.path.join(folder, 'template')

    dirArray = ["_static"]
    fileArray = ["make.bat", "Makefile", "conf.py"]

    for info in dirArray:
        if path.exists(os.path.join(currentFolder, info)):
            shutil.rmtree(os.path.join(currentFolder, info))
    for info in fileArray:
        if path.exists(os.path.join(currentFolder, info)):
            os.remove(os.path.join(currentFolder, info))
    
    shutil.copytree(os.path.join(templateFolder, '_static'), os.path.join(currentFolder, '_static'))
    shutil.copy(os.path.join(templateFolder, 'make.bat'), currentFolder)
    shutil.copy(os.path.join(templateFolder, 'Makefile'), currentFolder)
    if not path.exists(os.path.join(currentFolder, "docs")):
        os.mkdir(os.path.join(currentFolder, 'docs'))
    if not path.exists(os.path.join(currentFolder, "README.md")):
        shutil.copy(os.path.join(templateFolder, 'README.md'), currentFolder)


    with open(os.path.join(templateFolder, 'conf.py'), "r") as inputFd:
        with open(os.path.join(currentFolder, 'conf.py'), "w") as outputFd:
            for line in inputFd:
                if "author = " in line:
                    author = input("Input Author Name: ")
                    outputFd.write("author = '" + author + "'\n")
                    outputFd.write("copyright = '" + str(date.today().year) + ", " + author+ "'\n")

                    continue
                elif "copyright = " in line:
                    continue
                
                outputFd.write(line)

    if not path.exists(os.path.join(currentFolder, "CNAME")):
        with open(os.path.join(currentFolder, 'CNAME'), "w") as outputFd:
            cname = input("Input Your CNAME: ")
            outputFd.write(cname)

