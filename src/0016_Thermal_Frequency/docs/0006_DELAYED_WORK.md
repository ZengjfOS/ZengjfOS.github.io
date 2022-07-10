# DELAYED_WORK

每一个work对应一个处理函数，一个workqueue可以挂在多个work

# 参考文档

* [2021-06-09 Linux INIT_DELAYED_WORK 延时队列使用学习](https://blog.csdn.net/qq_37858386/article/details/117733197)
* [Linux Workqueue](http://kernel.meizu.com/linux-workqueue.html)
* [Linux Thermal 框架解析](http://kernel.meizu.com/linux-thermal-framework-intro.html)

# 简述

在中断中处理太多的操作是非常危险的，对中断的及时响应有很大的影响，在linux中我们经常会用到INIT_DELAYED_WORK，仔细看里面会有个定时器，用队列的形式来处理中断下半部分需要响应的操作
