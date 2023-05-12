# Compute Module 4

CM4是4B的核心板，定制性更好

# 芯片参考手册

CM4和4B用的是同一颗芯片，CM4可以认为是芯片的核心板，4B是加了外围的成品板

* [bcm2711-peripherals.pdf](refers/0001_bcm2711-peripherals.pdf)

# cm4手册

这个手册主要是告诉我们定制板子的时候该怎么设计，相关注意事项

* [0001_cm4-datasheet.pdf](refers/0001_cm4-datasheet.pdf)

# cm4官方扩展板

* 官方io扩展板原理图：[cm4io-datasheet.pdf](refers/0001_cm4io-datasheet.pdf)
* 树莓派4b原理图：[rpi_SCH_4b_4p0_reduced.pdf](refers/0001_rpi_SCH_4b_4p0_reduced.pdf)

# 连接器

* [cm4-datasheet.pdf](refers/0001_cm4-datasheet.pdf)
  * 3.1. Mechanical
    * Stacking height either:
      * a. 1.5mm with mating connector (clearance under CM4 0mm) : DF40C-100DS-0.4v
      * b. 3.0mm with mating connector (clearance under CM4 1.5mm): DF40HC(3.0)-100DS-0.4v

![0001_CM4_DF40_Connector.jpg](images/0001_CM4_DF40_Connector.jpg)

# PCB设计参考

* https://www.raspberrypi.org/documentation/hardware/computemodule/schematics.md
  * [CM4IO-KiCAD.zip](refers/0001_CM4IO-KiCAD.zip)
    * README.TXT  
      These files have been created in prerelease version 6 of KiCAD. If Version 6 isn't released yet then to use them you will need to download a nightly build of KiCAD. NB Nightly builds my have issues so please check the issue tracker. 
    * 使用KiCAD Version 6打开，目前稳定版只到Version 5，所以要用nightly build版本，经测试，确实是这样的
* [KiCAD Windows Download](https://kicad.org/download/windows/)
  * Nightly Development Builds
    * https://kicad-downloads.s3.cern.ch/index.html?prefix=windows/nightly/
* [getting_started_in_kicad.pdf](refers/0001_getting_started_in_kicad.pdf)
  * https://docs.kicad.org/master/en/getting_started_in_kicad/getting_started_in_kicad.html

![0001_KiCad_open_cm4_project.png](images/0001_KiCad_open_cm4_project.png)
