# Bluetooth

就目前而言，设备带有蓝牙功能已经是很普遍的事情了，所以花点时间研究一下底层是如何实现的。在遇到问题的时候，了解底层工作原理可以更快速的定位问题可能出在数据处理的哪个阶段


# 参考文档

* 蓝牙官网：https://www.bluetooth.com/
* 蓝牙官方工具：[Five Essential Tools for Every Bluetooth Low Energy Developer](https://blog.bluetooth.com/five-essential-tools-for-every-bluetooth-low-energy-developer)
* [Bluetooth 4.0 Core specifications - Bluetooth.org](https://www.bluetooth.org/docman/handlers/downloaddoc.ashx?doc_id=229737)
* [BLE节点 蓝牙4.0 CC2540 2541 SmartRF开发板 低功耗](https://detail.tmall.com/item.htm?spm=a230r.1.14.6.551d5c8chc2pC3&id=564867661483&cm_id=140105335569ed55e27b&abbucket=6)
* [蓝牙4.0 BLE开发完全手册 物联网开发技术实战电子书，基于CC2540](https://e2echina.ti.com/question_answer/wireless_connectivity/bluetooth/f/103/t/156405)
* [CC2540 and CC2541 Bluetooth® low energy Software Developer’s (Rev. G)](http://www.ti.com/lit/ug/swru271g/swru271g.pdf)
* [CC2541 (ACTIVE) Bluetooth low energy and proprietary wireless MCU](http://www.ti.com/product/CC2541/technicaldocuments)

* [C2540 and CC2541 Bluetooth low energy Software Developer’s Reference Guide.pdf](./docs/refers/0000_C2540_and_CC2541_Bluetooth_low_energy_Software_Developer’s_Reference_Guide.pdf)

开发板的资料需要购买后问客服要，不过很多的资料也是从TI官网来的。

# Hardware

![Hardware_For_BLE_Learning.jpg](docs/images/Hardware_For_BLE_Learning.jpg)

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0013 | [SmartRF_Packet_Sniffer](docs/0013_SmartRF_Packet_Sniffer.md) | 蓝牙嗅探器空中包抓去
0012 | [BTool](docs/0012_BTool.md) | BTool工具使用
0011 | [HostTestRelease](docs/0011_HostTestRelease.md) | 这部分可以跟的代码貌似不对，很多代码都是在库里调用，没有源代码
0010 | [Bluez_HCI_Principle](docs/0010_Bluez_HCI_Principle.md) | Bluez HCI通信
0009 | [SimpleBLEPeripheral_Init_Hack](docs/0009_SimpleBLEPeripheral_Init_Hack.md) | SimpleBLEPeripheral初始化分析
0008 | [SimpleBLEPeripheral_GATT_Hack](docs/0008_SimpleBLEPeripheral_GATT_Hack.md) | SimpleBLEPeripheral GATT分析
0007 | [SimpleBLEPeripheral_Key_Hack](docs/0007_SimpleBLEPeripheral_Key_Hack.md) | SimpleBLEPeripheral示例分析
0006 | [Android_BLE_Debuger](docs/0006_Android_BLE_Debuger.md) | 使用Android BLE工具连接测试CC2541 BLE
0005 | [CC254x_Reference_Manual](docs/0005_CC254x_Reference_Manual.md) | CC254x芯片参考手册
0004 | [BLE_Protocol_Stack](docs/0004_BLE_Protocol_Stack.md) | TI BLE协议栈
0003 | [OSAL](docs/0003_OSAL.md) | OSAL操作系统
0002 | [BLE_Base](docs/0002_BLE_Base.md) | BLE基本概念
0001 | [Development_Kit_Download](docs/0001_Development_Kit_Download.md) | CC2541开发工具
