# README

# 常用链接

<!-- table src/0000_Template/docs/refers/0000_BasicWebInfo.json -->
NO.  | 简介 | 链接
-----|-----|-----
0001 | 文档信息汇总 | * [早期博客园(cnblogs)文档](https://www.cnblogs.com/zengjfgit/)<br> * [GitHub账号: ZengjfOS](https://github.com/ZengjfOS)
0002 | Android 代码检索 | * [Android 官方代码检索](https://cs.android.com/)<br> * [Android 7 ~ latest OpenGrok Search](http://aospxref.com/)<br> * [Android 1 ~ 9 OpenGrok Search](http://androidxref.com/)
0003 | Linux内核源代码 | * [Linux 源代码在线检索](https://elixir.bootlin.com/linux/latest/source)<br> * [realme MTK 4.19源代码](https://github.com/realme-kernel-opensource/realme_C21-AndroidR-kernel-source)<br> * [荣耀 Open Source](https://www.hihonor.com/global/opensource/)<br> * [华为 Open Source](https://consumer.huawei.com/en/opensource/)
0004 | Android vendor源代码 | * [MTK vendor](https://github.com/OpenWatchProject/android_vendor_mediatek)<br> * [QCOM qti sdm660](https://github.com/ZengjfOS/android-firmware-qti-sdm660)

# 独立开源工具仓库

<!-- table src/0000_Template/docs/refers/0000_RepoInfo.json -->
NO.  | 仓库 | 主要编程语言 | 包管理 | LICENSE | 备注
-----|-----|-----|-----|-----|-----
0001 | [MDPlant](https://github.com/ZengjfOS/MDPlant) | TypeScript | [vscode extension](https://marketplace.visualstudio.com/items?itemName=zengjf.mdplant) | MIT | VSCode Markdown文档辅助工具插件，支持Windows、Linux、mac OS
0002 | [MDPlantLib](https://github.com/ZengjfOS/MDPlantLib) | Node.js | [npm](https://www.npmjs.com/package/mdplantlib) | MIT | MDPlantLib is lib for VSCode MDPlant Extension
0003 | [anpp](https://github.com/ZengjfOS/anpp) | Bash Script、Python3 | [PyPI](https://pypi.org/project/anpp/) | MIT | anpp(android project product)，解决android BSP多项目目录跳转问题
0004 | [PluginsPy](https://github.com/ZengjfOS/PluginsPy) | Python3 | [PyPI](https://pypi.org/project/PluginsPy/) | MIT | Python3插件化脚本框架，便于制作一些小的数据分析工具
0005 | [VisualLog](https://github.com/ZengjfOS/VisualLog) | Python3 | [PyPI](https://pypi.org/project/VisualLog/) | MIT | Android log数据提取框架，可用于性能对比分析
0006 | [AlogAnalyze](https://github.com/ZengjfOS/AlogAnalyze) | Python3 | None | Private | Android Kernel/Logcat log图形界面可视化分析工具

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0021 | [LXC](src/0021_LXC/README.md) | 使用LXC（Linux Containers）理解类似Docker容器系统底层工作体系架构
0020 | [macOS](src/0020_macOS/README.md) | 记录macOS上的一些使用技巧
0019 | [SW6106](src/0019_SW6106/README.md) | SW6106电源管理芯片分析
0018 | [keystore](src/0018_keystore/README.md) | Android keystore安全相关内容分析
0017 | [binder](src/0017_binder/README.md) | Android Binder通信
0016 | [matplotlib](src/0016_matplotlib/README.md) | matplotlib基本使用
0015 | [MediaPipe](src/0015_MediaPipe/README.md) | 通过MeidaPipe Android/树莓派4B运行理解所谓的AI
0014 | [Android](src/0014_Android/README.md) | Android一些零散的文档
0013 | [KiCad](src/0013_KiCad/README.md) | PCB画板工具KiCad
0012 | [fastboot](src/0012_fastboot/README.md) | Android fastboot工作原理
0011 | [MediaWiki](src/0011_MediaWiki/README.md) | 使用MediaWiki作为周报系统
0010 | [Linux](src/0010_Linux/README.md) | 记录一些零散的Linux方面的使用文档
0009 | [Terminal_UI](src/0009_Terminal_UI/README.md) | 终端cmd下图形界面
0008 | [SurfaceFlinger](src/0008_SurfaceFlinger/README.md) | Android SurfaceFlinger分析
0007 | [V4L2](src/0007_V4L2/README.md) | 分析V4L2的架构，其中包括显示部分和摄像头部分
0006 | [ASoC](src/0006_ASoC/README.md) | 分析i.MX6 CS42888 ASoC驱动工作原理
0005 | [Yocto](src/0005_Yocto/README.md) | 分析Yocto编译原理，能做的事情和Buildroot类似，不过更重要的是芯片大厂都参与维护，知名度更高
0004 | [Bluetooth_Protocol](src/0004_Bluetooth_Protocol/README.md) | 就目前而言，设备带有蓝牙功能已经是很普遍的事情了，所以花点时间研究一下底层是如何实现的。在遇到问题的时候，了解底层工作原理可以更快速的定位问题可能出在数据处理的哪个阶段
0003 | [USB_Protocol](src/0003_USB_Protocol/README.md) | 之前有看过几次USB方面的书，也移植过USB驱动，不过一直也没什么时间投入来研究USB底层通信里面的东西，这次打算花点时间系统性刨根究底的分析一次
0002 | [DebugHAT](src/0002_DebugHAT/README.md) | 制作硬件调试扩展板
0001 | [RaspberryPi](src/0001_RaspberryPi/README.md) | 个人认为，树莓派应该算是目前开源硬件里学习嵌入式Linux系统最好的工具，里面的设计思路和一些工具是很值得借鉴的，这里主要使用Raspberry Pi 4B进行系统架构分析。
0000 | [Template](src/0000_Template/README.md) | 这个是一个plan的文档模板目录示例架构
