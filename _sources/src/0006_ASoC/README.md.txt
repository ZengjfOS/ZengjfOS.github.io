# ASoC

分析i.MX6 CS42888 ASoC驱动工作原理

# 参考文档

* [Linux Source Code Online](https://elixir.bootlin.com/linux/latest/source)
* [ALSA SoC Layer](https://www.kernel.org/doc/html/v4.11/sound/soc/index.html)
* [sound-cs42888 dts](https://github.com/torvalds/linux/blob/master/arch/arm/boot/dts/imx6qdl-sabreauto.dtsi#L124)
* [Tiny library to interface with ALSA in the Linux kernel](https://github.com/tinyalsa/tinyalsa)

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0022 | [sound-xtor](docs/0022_sound-xtor/README.md) | 蓝牙PCM连接对应的声卡配置
0021 | [Android_Bluetooth_HFP](docs/0021_Android_Bluetooth_HFP.md) | Android P蓝牙语音通话时，声道怎么切换的？
0020 | [PCM_Interface_I2S_Master-Slave](docs/0020_PCM_Interface_I2S_Master-Slave.md) | PCM接口I2S数据格式，主从I2S谁来发送BCLK/LRCLK?
0019 | [Generate_wavfile](docs/0019_Generate_wavfile/README.md) | 如何生成特定wav文件来测试声卡
0018 | [ALSA_Period](docs/0018_ALSA_Period.md) | 理解ALSA中Period的概念，理解它才能理解应用层软件如何操作声卡
0017 | [I2S_Frame](docs/0017_I2S_Frame.md) | I2S进行声音数据传输的时候，如何表示一帧声音数据，在Linux应用层软件进行PCM数据存储的时候，也是一帧一帧的对数据进行储存
0016 | [tinycap](docs/0016_tinycap.md) | 主要是了解一下一般的录音的用户层是如何操作的
0015 | [dapm-event](docs/0015_dapm-event.md) | dapm并没有外部设备节点控制，如何进行操作的呢？
0014 | [widget_dapm-control](docs/0014_widget_dapm-control.md) | widget和widget连接的route中的control在哪里进行操作？
0013 | [tinymix](docs/0013_tinymix.md) | 主要是分析tinymix如何获取声卡的controls以及如果要操作control的时候，系统的调用流程
0012 | [Control_Device](docs/0012_Control_Device.md) | 声卡的control设备节点是怎么生成的，回调函数在哪里？
0011 | [tinyplay](docs/0011_tinyplay.md) | aplay代码量有点大，分析一下tinyplay，看看wav文件数据是如何写道PCM设备节点中去的
0010 | [snd_pcm_new](docs/0010_snd_pcm_new.md) | 看一下pcm的创建过程
0009 | [RPI_ALSA_Tinyalsa](docs/0009_RPI_ALSA_Tinyalsa.md) | 看一下树莓派的声卡情况
0008 | [widget-control-route_Add_To_Card](docs/0008_widget-control-route_Add_To_Card.md) | component中widget/contorl/route添加到Card中的流程
0007 | [component_probe](docs/0007_component_probe.md) | 了解一下component中的那些widgets/controls/routes/dai/probe等如何被调用起作用的
0006 | [bind_dai_link](docs/0006_bind_dai_link.md) | pcm runtime(rtd)在这里绑定需要dai_link涉及到的CPU/Platform/Codec component
0005 | [dai_link_component](docs/0005_dai_link_component.md) | dai_link的真实面目
0004 | [ASoC_Machine_Driver](docs/0004_ASoC_Machine_Driver.md) | 主板声卡功能注册
0003 | [ASoC_Platform_Driver](docs/0003_ASoC_Platform_Driver.md) | 芯片平台声卡接口设备注册
0002 | [ASoC_Codec_Class_Driver](docs/0002_ASoC_Codec_Class_Driver.md) | Codec compnent信息注册
0001 | [DTS](docs/0001_DTS.md) | CS42888声卡设备树示例
