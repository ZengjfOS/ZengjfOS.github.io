# 匿名Binder

理解Binder传递Binder的本质，类似注册回调函数

# 参考文档

* [Android Binder框架实现之何为匿名/实名Binder](https://blog.csdn.net/tkwxty/article/details/108343847)

# 简述

* 匿名Binder，即没有向servicemanagerI进程注册的Binder都是匿名Binder(虽然没有向servicemanager进程注册，但是依然可以借助Binder框架进行通信)；
* 匿名Binder进程端可以通过已经建立的Binder连接将创建的Binder实体传给目的端，当然这条已经建立的Binder连接必须是通过实名Binder实现；
* 由于这个Binder没有向servicemanager进程注册名字，所以是个匿名Binder。目的端将会收到这个匿名Binder的引用，可以通过这个引用向位于匿名Binder实体进进程中的中的实体发送请求；
* 匿名Binder为通信双方建立一条私密通道，只要目的端没有把匿名Binder发给别的进程，别的进程就无法通过穷举或猜测等任何方式获得该Binder的引用，向该Binder发送请求；
* 当然通过service list也查询不到了；
* 跨进程的回调函数属于匿名Binder；
