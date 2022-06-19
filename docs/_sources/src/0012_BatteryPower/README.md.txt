# README

Android休眠功耗分析，休眠原理

# docs

NO.|文件名称|摘要
:--:|:--|:--
0017| [Android_SystemUI_Battery](docs/0017_Android_SystemUI_Battery.md) | 分析SystemUI Battery电量变化的原理
0016| [Android_Battery_Animation](docs/0016_Android_Battery_Animation.md) | 关机充电动画怎么工作的，如何获取电量信息，无mobile log，只能看uart port
0015| [Android_Wakeup_Reason](docs/0015_Android_Wakeup_Reason.md) | Android层如何获取唤醒原因，最终读取内核提供的文件节点获取信息
0014| [Android_Suspend_Callback](docs/0014_Android_Suspend_Callback.md) | Android系统是如何被唤醒的
0013| [Android_Suspend](docs/0013_Android_Suspend.md) | Android输入休眠模式到`/sys/power/state`让机器进入深度休眠
0012| [Android_wake_lock](docs/0012_Android_wake_lock.md) | 测试软件自动关屏，adb查看测试软件wake lock，查看是否有额外的进程持锁，adb的USB是正常的，忽略
0011| [Power_Monitor](docs/0011_Power_Monitor.md) | 通过功耗分布和resume分布可以知道哪些resume导致的问题，进而看对应的resume的log就可以知道系统做了什么导致的功耗问题
0010| [Android_Docker_New](docs/0010_Android_Docker_New.md) | 学习如何创建自己的Docker，后续准备自己处理Docker
0009| [Android_BatteryStats_Docker](docs/0009_Android_BatteryStats_Docker.md) | 采用Docker形式的Battery Historian v3.1分析BatteryStats，以及电源分析示例
0008| [Android_BatteryStats](docs/0008_Android_BatteryStats.md) | 参考文档对BatteryStats中的信息说明的很详细
0007| [Android_res_Overlay](docs/0007_Android_res_Overlay.md) | Android Overlay机制允许在不修改packages中apk的情况下，来自定义framework和package中的资源文件，实现资源的定制。
0006| [Android_Battery_Current](docs/0006_Android_Battery_Current.md) | 通过查看电池电流情况，了解系统深度休眠功耗情况
0005| [Android_Low_Power](docs/0005_Android_Low_Power.md) | 开了MTK debugger log系统也是能够进入深度休眠，3C Battery Manager.apk记录电池电流使用
0004| [Android_Typc-C_Charger](docs/0004_Android_Typc-C_Charger.md) | Android Type-C 充电
0003| [USB_PD_Protocol](docs/0003_USB_PD_Protocol.md) | 理解USB快充工作原理
0002| [SPM_Power_Analysis](docs/0002_SPM_Power_Analysis.md) | System Power Manager功耗分析
0001| [Deep_Sleep](docs/0001_Deep_Sleep.md) | 深睡眠机制，貌似树莓派上没使用
