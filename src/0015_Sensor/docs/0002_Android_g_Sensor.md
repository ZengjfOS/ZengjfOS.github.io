# Android g Sensor

理解加速度计是如何校准的

# 参考文档

* [无人机高级篇系列第七讲：陀螺仪校准](https://zhuanlan.zhihu.com/p/65550540)

# G sensor两个中断pin的配置

* 重力传感器一般有引出2个中断pin脚，该如何配置
  * 这2个中断脚是不使用的，不需要配置

# G sensor校准流程

* 如何进行g sensor校准：进入工厂模式后，单项测试中，选择 g sensor校准选项，平放手机，校准即可
* 工模下校准流程，工模下的数据通过ioctl和driver层进行交互
  * 在第1步中进行校准后，通过ioctl读取20个数据，取平均做校准
  * 计算得到校准数据后，通过ioctl 把校准的数据写入driver内
  * 同时把校准数据保存到nvram中
* 校准一次，重新开机时如何把校准数据保存：
  * 在做校准时，会把数据保存到nvram中；开机时，会先从nvram中读取之前校准的数据，然后通过ioctl把校准数据设置到driver，所以校准一次就可以实现sensor的使用。
  * 开机过程中的nvram_daemon会去读取nvram中的值写入driver，从而生效
