# README

SW6106电源管理芯片分析

# 参考文档

* [树莓派锂电池扩展板 SW6106移动电源方案 内置保护电路 带3000mAh大电量锂电池](https://www.waveshare.net/shop/Li-polymer-Battery-HAT.htm)
* [0001_Li-polymer_Battery_HAT_manual_CN.pdf](docs/refers/0001_Li-polymer_Battery_HAT_manual_CN.pdf)
* [SW6106官网](http://www.ismartware.com/details-2-33.html)
  * 官网资料包，含寄存器描述
    * [0001_202207211609549053.zip](docs/refers/0001_202207211609549053.zip)

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0009 | [MTK_discharge_curve](docs/0009_MTK_discharge_curve.md) | MTK平台放电曲线
0008 | [Discharge](docs/0008_Discharge.md) | 充电后放电数据
0007 | [Charge](docs/0007_Charge.md) | 放电后充电数据，发现只支持恒压阶段
0006 | [BatteryInfo](docs/0006_BatteryInfo.md) | 电池电量、电压、充放电电流信息
0005 | [SOC](docs/0005_SOC.md) | SOC: Status of charge，电池电量
0004 | [Current](docs/0004_Current.md) | 充放电电流，电流是经过charger的电流，不是经过battery的电流
0003 | [Voltage](docs/0003_Voltage.md) | 获取当前电池、输出的电压
0002 | [NTC](docs/0002_NTC.md) | NTC温度计算，没有上NTC电阻的料，是一个固定阻值的电阻
0001 | [微雪电池扩展板](docs/0001_微雪电池扩展板.md) | 微雪电池扩展板采用SW6106芯片
