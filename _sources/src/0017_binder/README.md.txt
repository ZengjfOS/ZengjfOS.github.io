# README

Android Binder通信

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0014 | [HIDL_generates返回值](docs/0014_HIDL_generates返回值.md) | HIDL中的函数带有generates是怎么处理的
0013 | [aidl_parcelable_cpp](docs/0013_aidl_parcelable_cpp.md) | aidl直接定义parcelable数据，用数组替代list parcelable类型的数据
0012 | [Binder_Native_Call_AIDL](docs/0012_Binder_Native_Call_AIDL.md) | 从Native调用AIDL接口，实现C、C++如何访问aidl接口
0011 | [Binder_Native_Services](docs/0011_Binder_Native_Services.md) | 分析Binder通信Native服务区启动原理，ProcessState、IPCThreadState如何做到不同service的调用、处理
0010 | [Thread_Specific_Data](docs/0010_Thread_Specific_Data.md) | 多线程独立拥有全局变量
0009 | [Android_Parcelable](docs/0009_Android_Parcelable.md) | 理解Parcelable类实现原因
0008 | [Android_Manager_Service](docs/0008_Android_Manager_Service.md) | Manager是Binder Client，Service是Binder Service
0007 | [Android_BitTube](docs/0007_Android_BitTube.md) | BitTube本质是socketpair，Binder实现了sendmsg传递fd的功能
0006 | [Process_Share_File_Descriptor](docs/0006_Process_Share_File_Descriptor.md) | 进程间传递文件描述符
0005 | [socketpair](docs/0005_socketpair.md) | socketpair用于创建一对无名的、相互连接的套接字，于进程间通信。
0004 | [Android_binder_bctest](docs/0004_Android_binder_bctest.md) | bctest程序没有根据servicemanager更新通信协议，Android版本导致的
0003 | [Linux_Splice](docs/0003_Linux_Splice.md) | 理解零拷贝有助于理解Android Binder通信
0002 | [bclient_bservice](docs/0002_bclient_bservice.md) | Android binder cmd调试工具
0001 | [Android_Binder](docs/0001_Android_Binder.md) | 移植Android Binder到树莓派
