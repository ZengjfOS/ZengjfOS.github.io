# USB

之前有看过几次USB方面的书，也移植过USB驱动，不过一直也没什么时间投入来研究USB底层通信里面的东西，这次打算花点时间系统性刨根究底的分析一次

# 参考文档

* [EZ-USB FX2LP CY7C68013A USB 开发板 逻辑分析仪YourCee](https://item.taobao.com/item.htm?spm=a230r.1.14.34.36aa2429c1z3Fr&id=522553287560&ns=1&abbucket=6#detail)
* [CY7C68013A-56PVXC](http://www.cypress.com/part/cy7c68013a-56pvxc)
* [AN65209 - Getting Started with FX2LP™](http://www.cypress.com/documentation/application-notes/an65209-getting-started-fx2lp)
* [AN65209 Getting Started with FX2LP(Chinese).pdf](http://www.cypress.com/file/44946/download)
* [CY3684 EZ-USB FX2LP Development Kit](http://www.cypress.com/documentation/development-kitsboards/cy3684-ez-usb-fx2lp-development-kit)
* [EZ-USB® Technical Reference Manual](http://www.cypress.com/documentation/technical-reference-manuals/ez-usb-technical-reference-manual)
* [SuiteUSB 3.4 - USB Development tools for Visual Studio](http://www.cypress.com/documentation/software-and-drivers/suiteusb-34-usb-development-tools-visual-studio)
* [Drivers for EZ-USB® FX1™, FX2LP™ , and FX3 - KBA94413](https://community.cypress.com/docs/DOC-12366)
* [USB Hi-Speed Code Examples](http://www.cypress.com/documentation/code-examples/usb-hi-speed-code-examples)
* [USB Type-C™ and Power Delivery Minidock With Video and Charging Support Reference Design](http://www.ti.com/tool/TIDA-01243?tdsourcetag=s_pcqq_aiomsg)

# 开发工具、示例

[CY3684 EZ-USB FX2LP DVK Setup (Kit Design Files, Kiel IDE,GPIF Designer, Host applications, Documentation, Examples)](http://www.cypress.com/file/135301)

# Schematic

![0000_CY7C68013A_Schematic.png](docs/images/0000_CY7C68013A_Schematic.png)

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0024 | [USB_Keyboard](docs/0024_USB_Keyboard.md) | USB键盘驱动分析
0023 | [USB_Camera_UVC](docs/0023_USB_Camera_UVC.md) | USB Camera数据通信原理
0022 | [Vendor_Command](docs/0022_Vendor_Command.md) | 如何定义Vendor命令
0021 | [GPIF](docs/0021_GPIF.md) | GPIF接口使用
0020 | [Keil](docs/0020_Keil.md) | Keil使用方法
0019 | [Linux_Compile](docs/0019_Linux_Compile.md) | Linux编译DSLogic-fw
0018 | [CY7C68013A_FPGA](docs/0018_CY7C68013A_FPGA.md) | CY7C68013A与FPGA
0017 | [Type-C](docs/0017_Type-C.md) | Type-C参考
0016 | [Isochronous_Transfers](docs/0016_Isochronous_Transfers.md) | 一步传输示例
0015 | [Send_Setup_Packet](docs/0015_Send_Setup_Packet.md) | 如何发送Setup包
0014 | [Why_StreamExample_Always_Select_Alt6](docs/0014_Why_StreamExample_Always_Select_Alt6.md) | 流传输如何设置备选项
0013 | [USB_Descriptors_AlternateSetting](docs/0013_USB_Descriptors_AlternateSetting.md) | USB描述符备用选择
0012 | [CYStream_Compile](docs/0012_CYStream_Compile.md) | USB流模式示例编译
0011 | [HID_Compliant_Device](docs/0011_HID_Compliant_Device.md) | HID兼容设备
0010 | [HID_Keyboard_Modify](docs/0010_HID_Keyboard_Modify.md) | USB控制器会采用伪中断进行对设备进行轮询，Wireshare只有在有数据传输才会在总线上有Interrupt IN包，也就是说如果设备没有准备好数据，那么USB控制器是不会去轮询的。
0009 | [Wireshark_Filter](docs/0009_Wireshark_Filter.md) | Wireshark过滤使用
0008 | [HID_Keyboard](docs/0008_HID_Keyboard.md) | HID键盘示例
0007 | [Bulkloop_Example](docs/0007_Bulkloop_Example.md) | USB Bulk传输示例
0006 | [CY3684_EZ-USB_FX2LP_DVK](docs/0006_CY3684_EZ-USB_FX2LP_DVK.md) | 配置Firmware开发环境，使用Keil UV2进行开发，不过需要配置环境才能使用，而不是安装完成了直接能够使用，目前是在Windows 10上进行配置环境是OK，说明在Windows 10上可以正常工作。
0005 | [Wireshark_GET_DESCRIPTOR_Analyzer](docs/0005_Wireshark_GET_DESCRIPTOR_Analyzer.md) | 使用Wireshark分析USB协议
0004 | [Capturing_USB_Traffic](docs/0004_Capturing_USB_Traffic.md) | USB抓包工具
0003 | [Quick_Start](docs/0003_Quick_Start.md) | 开发板快速入门
0002 | [EZ-USB_Integrated_Microprocessor](docs/0002_EZ-USB_Integrated_Microprocessor.md) | EZ-USB一些参考文档
0001 | [USB_Specification](docs/0001_USB_Specification.md) | 了解USB一些基本标准概念
