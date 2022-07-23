# README

热电偶（NTC）温控系统与CPU自动调频

# MTK kernel

* https://github.com/MediaTek-Labs/common-kernel-4.19
* https://github.com/xiaomi-mt6765/android_kernel_xiaomi_mt6765
* https://github.com/mediatek-android-development/android_kernel_mediatek_mt6761-62-4.9

# docs

NO.|文件名称|摘要
:--:|:--|:--
0015| [CPUFreq_schedutil](docs/0015_CPUFreq_schedutil.md) | scheduler和调频建立起更加紧密的联系，同时提升了性能和功耗表现
0014| [CPUFreq](docs/0014_CPUFreq.md) | 理解CPU自动调频
0013| [thermal_core](docs/0013_thermal_core.md) | 理解struct thermal_zone_device(framework)和struct __thermal_zone(NTC)的差异
0012| [thermal_hwmon](docs/0012_thermal_hwmon.md) | the linux hardware monitoring kernel api
0011| [btscharger温控处理](docs/0011_btscharger温控处理.md) | 触发thermal温度设置，cool设备进行温控处理
0010| [thermal_config](docs/0010_thermal_config.md) | 温控配置
0009| [thermal采样周期调节](docs/0009_thermal采样周期调节.md) | 通过当前温度调节采样周期
0008| [thermal_manager](docs/0008_thermal_manager.md) | mtk thermal manager加载MTK温控策略
0007| [thermal_monitor](docs/0007_thermal_monitor.md) | thermal monitor注册thermal zone设备、thermal cooling设备
0006| [DELAYED_WORK](docs/0006_DELAYED_WORK.md) | 每一个work对应一个处理函数，一个workqueue可以挂在多个work
0005| [thermal_zones_btscharger](docs/0005_thermal_zones_btscharger.md) | btscharger温度控制系统工作原理
0004| [NTC温度计算](docs/0004_NTC温度计算.md) | NTC温度方法
0003| [Thermal_Zone](docs/0003_Thermal_Zone.md) | 温控管理框架
0002| [ftrace_CPU_Frequency](docs/0002_ftrace_CPU_Frequency.md) | 理解CPU自动调频
0001| [temperature_frequence_CPU](docs/0001_temperature_frequence_CPU.md) | 获取CPU温度、频率
