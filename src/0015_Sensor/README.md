# README

理解Android Sensor体系架构

# docs

NO.|文件名称|摘要
:--:|:--|:--
0014| [visible_ir_diode](docs/0014_visible_ir_diode.md) | 可见光、红外二极管融合数据才是光感，驱动获取数据之后会做ratio融合
0013| [i2c_dma](docs/0013_i2c_dma.md) | 当需要连续发送大量数据，考虑采用DMA进行数据传输，fifo最大才8 byte
0012| [scp_log_buffer](docs/0012_scp_log_buffer.md) | 修改scp log buffer，MTK debuglogger UI抓log要等一段时间，如果log太多会被覆盖，注意裁减log
0011| [scp_debug_log](docs/0011_scp_debug_log.md) | 打印更多的scp调试log，注意CFG_OVERLAY_INIT_SUPPORT
0010| [Android_SensorHub_APP](docs/0010_Android_SensorHub_APP.md) | Sensor应用层校正操作
0009| [Android_alsps_Sensor](docs/0009_Android_alsps_Sensor.md) | 快速获取近距、光感传感器数值
0008| [Android_Sensor_Power](docs/0008_Android_Sensor_Power.md) | 在PL阶段访问PMIC，配置Sensor电源输出
0007| [Android_SCP_IPI](docs/0007_Android_SCP_IPI.md) | Inter-Processor Communication (IPC) and Inter-Processor Interrupt (IPI)
0006| [Android_SCP](docs/0006_Android_SCP.md) | SCP(Sensor-hub Control Processor)，CHRE(Context Hub Runtime Environment), System Companion Processor (SCP)
0005| [Android_Sensors](docs/0005_Android_Sensors.md) | Android传感器架构
0004| [Android_BitTube](docs/0004_Android_BitTube.md) | BitTube本质是socketpair，Binder实现了sendmsg传递fd的功能
0003| [Android_C++_CallStack](docs/0003_Android_C++_CallStack.md) | Android C++ backtrace
0002| [Android_g_Sensor](docs/0002_Android_g_Sensor.md) | 理解加速度计是如何校准的
0001| [Sensor_xyz_Direction](docs/0001_Sensor_xyz_Direction.md) | PCBA板传感器贴片位置不同，怎么确定及调整xyz
