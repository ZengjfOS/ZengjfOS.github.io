# README

使用LXC（Linux Containers）理解类似Docker容器系统底层工作体系架构

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0022 | [LXC_veth_NAT](docs/0022_LXC_veth_NAT.md) | LXC通过虚拟网卡NAT到Wifi获取网络
0021 | [Android_iptables_netd](docs/0021_Android_iptables_netd.md) | 理解firewall整体架构及netd所处的位置
0020 | [LXC_Template_Download](docs/0020_LXC_Template_Download.md) | Busybox系统用于LXC原理分析，Ubuntu用于容器性能分析
0019 | [LXC_Network](docs/0019_LXC_Network.md) | 理解LXC创建虚拟网卡流程
0018 | [Process_Share_File_Descriptor](docs/0018_Process_Share_File_Descriptor.md) | 进程间传递文件描述符
0017 | [LXC_Console_get_ptmx_master](docs/0017_LXC_Console_get_ptmx_master.md) | lxc-console是怎么做到跟容器内console通信的
0016 | [LXC_ptmx_Console](docs/0016_LXC_ptmx_Console.md) | lxc-console为什么能像串口一样工作？
0015 | [LXC_chroot_fs_isolate](docs/0015_LXC_chroot_fs_isolate.md) | 对于rootfs隔离，使用pivot_root切换到根文件系统目录，chroot一样
0014 | [LXC_AF_UNIX_Local_Socket](docs/0014_LXC_AF_UNIX_Local_Socket.md) | AF_UNIX跨Namespace通信，父子进程可以用pipe
0013 | [Virtual_Ethernet_And_Bridge](docs/0013_Virtual_Ethernet_And_Bridge.md) | 本地以太网隧道，Linux container中用到一个叫做veth的东西，这是一种新的设备，专门为container所建。
0012 | [Input_mouse_driver_analysis](docs/0012_Input_mouse_driver_analysis.md) | 基于usb mouse理解Input子系统架构
0011 | [device_namespace](docs/0011_device_namespace.md) | 理解device namespace工作原理
0010 | [namespace_CLONE_NEWIPC_pipe](docs/0010_namespace_CLONE_NEWIPC_pipe.md) | IPC通信隔离，父子进程怎么通信管理，可以使用匿名pipe
0009 | [LXC_namespace_cgroup](docs/0009_LXC_namespace_cgroup.md) | namespace做资源隔离, cgroup做资源限制，cgroup也是一种namespace
0008 | [LXC_Compile_From_Source](docs/0008_LXC_Compile_From_Source.md) | LXC编译、运行
0007 | [lxc_devices_cgroup_mount](docs/0007_lxc_devices_cgroup_mount.md) | 查看devices cgroup可否自己手动mount
0006 | [Android_binder_bctest](docs/0006_Android_binder_bctest.md) | bctest程序没有根据servicemanager更新通信协议，Android版本导致的
0005 | [Android_cmd_static](docs/0005_Android_cmd_static.md) | Android编译static cmd命令可执行程序
0004 | [LXC_binder](docs/0004_LXC_binder.md) | 尝试容器中使用binder
0003 | [build_cmd_for_Android](docs/0003_build_cmd_for_Android.md) | 树莓派的busybox可以在Android上使用，那么树莓派编译的static程序应该也能在Android上使用
0002 | [LXC_busybox](docs/0002_LXC_busybox.md) | busybox lxc工作原理分析
0001 | [Linux_Container_LXC](docs/0001_Linux_Container_LXC.md) | 理解容器LXC的本质
