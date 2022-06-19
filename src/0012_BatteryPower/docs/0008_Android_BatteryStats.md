# Android BatteryStats

参考文档对BatteryStats中的信息说明的很详细

# 参考文档

* [电量统计(1)-原理](https://duanqz.github.io/2015-07-21-batterystats-part1)
* [电量统计(2)-日志](https://duanqz.github.io/2015-07-21-batterystats-part2)
* [0006_Android_Battery_Current.md](0006_Android_Battery_Current.md)

# 模块耗电配置

* frameworks/base/core/res/res/xml/power_profile.xml
  * 一般会被overlay
  * [0007_Android_res_Overlay.md](0007_Android_res_Overlay.md)

# 简述

手机有很多硬件模块：CPU，蓝牙，GPS，显示屏，Wifi，射频(Cellular Radio)等，在手机使用过程中，这些硬件模块可能处于不同的状态，譬如Wifi打开或关闭，屏幕是亮还是暗，CPU运行或休眠。 硬件模块在不同的状态下的耗电量是不同的。Android在进行电量统计时，并不是采用直接记录电流消耗量的方式，而是跟踪硬件模块在不同状态下的使用时间，收集一些可用信息，用来近似的计算出电池消耗量。

从用户使用层面来看，Android需要统计出应用程序的耗电量。应用程序的耗电量由很多部分组成，可能使用了GPS，蓝牙等模块，可能应用程序要求长时间亮屏(譬如游戏、视频类应用)。 一个应用程序的电量统计，可以采用累计应用程序使用所有硬件模块时间这种方式近似计算出来。

举一个例子，假定某个APK的使用了GPS，使用时间用 t 表示。GPS模块单位时间的耗电量用 w 表示，那么，这个APK使用GPS的耗电量就可以按照如下方式计算：

```
耗电量 = 单位时间耗电量(w) × 使用时间(t)
```

Android框架层通过一个名为batterystats的系统服务，实现了电量统计的功能。batterystats获取电量的使用信息有两种方式：

* 被动(push)：有些硬件模块(wifi, 蓝牙)在发生状态改变时，通知batterystats记录状态变更的时间点
* 主动(pull)：有些硬件模块(cpu)需要batterystats主动记录时间点，譬如记录Activity的启动和终止时间，就能计算出Activity使用CPU的时间

batterystats有主动和被动收集电量使用信息的方式，收集的信息基本都包含硬件模块的状态和被使用的时间两个维度。为什么仅仅是收集不同硬件模块的使用时间呢？ 前面我们说过，手机电压通常是恒定的，耗电量是通过 "单位时间电流量(I) × 使用时间(t)" 来计算，而单位时间电流量是由厂商给定的，定义在power_profile.xml中， 所以，只需要收集不同硬件模块的使用时间，就可以近似的计算出耗电量了

收集信息被组织起来，在内存中的数据结构是由BatteryStats类描述的。 为了能够从不同维度统计耗电量，这个数据结构设计得比较复杂，我们不在这里展开讨论，仅通过一个收集应用程序前台运行时间的例子，来说明信息收集过程。

# 术语

* realtime：正常流逝的时间，通常把这个时间叫做"墙上时间(walltime)"，就像挂在墙上的时钟一样，走过了一小时就是小时
* uptime：CPU工作的时间。“墙上时间”经过一小时，但CPU可能就工作了一分钟，其他时间CPU都在休眠
* 休眠率： (realtime-uptime)/realtime，既手机休眠的时间占整个待机时间的比率。休眠率越高，就表明越省电
* Total partial wakelock time：应用层持有wakelock的总时间
* Time on battery screen off：在灭屏状态下，电池的使用时间。通常，在灭屏时，我们希望手机可以快速进入休眠状态，所以，这里计算出的休眠率使我们考察耗电问题的重要指标
* kernel active time：射频模块的kernel层活跃时间。如果长时间处于活跃，那会比较快的消耗电量
* Radio Access Technology：接入的网络类型(none未插卡、umts、hspa、lte、hspap等)
* Rx signal strength：信号强度。如果长时间处于信号不好的情况，射频模块会提高功率，从而引起更大的耗电
* Sleep time/Idle time/Rx time/Tx time：射频模块分别处于休眠、空闲、接收数据、发送数据这几种不同状态下的时间Wifi和Bluetooth的使用统计与Cellular大同小异，不再赘述。

# dumpsys batterystats

`dumpsys batterystats`

![0008_Android_batterystats_structure.png](images/0008_Android_batterystats_structure.png)

* Battery History: 耗电统计的历史记录，每一条记录以HistoryItem的形式存在
* Per-PID Stats: 每个进程唤醒工作的时间
* Discharge step durations: 每掉一隔电的时间点和设备的状态
* Daily stats: 以天为单位展示每掉一隔电的时间点和设备状态
* Statistics since last charge: 从上次充电以来的统计详情，包含很多子板块
  * Cellular Statistics: 移动数据网络状态和使用情况
  * Wifi Statistics: WIFI的网络状态和使用情况
  * Bluetooth: 蓝牙在不同工作状态下的使用情况
  * Estimated power use (mAh): 近似计算出的各个用户(uid)的耗电量，一个APK通常对应到一个用户，当然，也有多个APK共享一个用户的情况
  * All kernel wake locks: 内核锁的使用统计
  * All partial wake locks: 应用锁的使用统计
  * All wakeup reasons: 所有的唤醒原因
  * Statistics by uid: 每一个uid的耗电细节

# Battery History

![0008_Android_batterystats_history.png](images/0008_Android_batterystats_history.png)

* https://duanqz.github.io/2015-07-21-batterystats-part2#21-battery-history

# x86-64 docker

* sudo apt-get update
* curl -fsSL https://get.docker.com -o get-docker.sh
* sudo sh get-docker.sh
* sudo docker -- run -p 5555:9999 gcr.io/android-battery-historian/stable:3.0 --port 9999
  * 无法获取
  * https://hub.docker.com/r/bhaavan/battery-historian
  * sudo docker pull bhaavan/battery-historian
    * https://github.com/bhaavanmerchant/battery-historian-docker
    * sudo docker run -d -p 9999:9999 bhaavan/battery-historian
    * x86-64的系统，不是ARM的系统
  * 存在无法解析的现象，无法使用，主要是版本旧了，有些数据解析不出来；
* sudo docker -- run -p 9999:9999 gcr.io/android-battery-historian/stable:3.1 --port 9999
  * https://hub.docker.com/search?q=android-battery-historian&type=image
    * 靠后一点有3.1版本的
    * 详细实现方式参考： https://github.com/gusha915/no-ssr-battery-historian
  * sudo docker pull runcare/battery-historian
  * sudo docker run -it -d -p 9999:9999 runcare/battery-historian --port 9999
  * http://192.168.182.129:9999/
    * 要支持能够访问google才行，否者加载文件会出问题，导致加载不了文件，正常能够分析出来；

![0006_Battery_Historian_Bugreport_Home.png](images/0006_Battery_Historian_Bugreport_Home.png)

# go build

* https://github.com/google/battery-historian
* sudo apt-get install golang
* export GOPATH=$HOME/work
* export GOBIN=$GOPATH/bin
* export PATH=$PATH:$GOBIN
* go get -d -u github.com/google/battery-historian/...
  * [go get 找不到 google.golang.org/protobuf 解决办法](https://blog.csdn.net/weixin_44448273/article/details/105571483)
  * 方法一：
    * git clone https://e.coding.net/robinqiwei/googleprotobuf.git $GOPATH/src/google.golang.org/protobuf
  * 方法二：
    * https://pkg.go.dev/google.golang.org/protobuf
      * https://github.com/protocolbuffers/protobuf-go
    * mkdir -p $GOPATH/src/google.golang.org
    * cd $GOPATH/src/google.golang.org
    * git clone git@github.com:protocolbuffers/protobuf-go.git
    * cp protobuf-go protobuf -r
* cd $GOPATH/src/github.com/google/battery-historian
* go run setup.go
  * error 1
    ```
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/ui/tree/typeahead_test.js:151: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/ui/tree/typeahead_test.js:161: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/ui/tree/typeahead_test.js:166: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/ui/tree/typeahead_test.js:176: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/ui/tree/typeahead_test.js:181: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/window/window.js:123: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/window/window_test.js:35: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/window/window_test.js:59: WARNING - Parse error. unknown @suppress parameter: strictMissingProperties
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/module/modulemanager_test.js:281: ERROR - Parse error. '}' expected
    /home/pi/work/src/github.com/google/battery-historian/third_party/closure-library/closure/goog/streams/full_test_cases.js:631: ERROR - Parse error. '(' expected
    2 error(s), 1128 warning(s)
    ```
    * [closure-library/closure/goog/streams/full_test_cases.js:635: ERROR - Parse error. '(' expected #988](https://github.com/google/closure-library/issues/988)
    * cd third_party/closure-library/
    * git reset --hard v20170409
    * go run setup.go
* go run cmd/battery-historian/battery-historian.go
  ```
  2021/06/22 04:26:42 Listening on port:  9999
  ```
  * 不加后面的port参数，默认端口号是9999
  * go run cmd/battery-historian/battery-historian.go [--port \<default:9999\>]
* http://192.168.137.2:9999/
* 上传bug report文件，submit，查看分析内容
  ```
  error getting appID from string: strconv.Atoi: parsing "u0ai9000": invalid syntax
  strconv.ParseInt: parsing "0.0": invalid syntax
  ...省略
  could not parse aggregated battery stats
  device capacity is 0
  ```
  * 详细实现方式参考： https://github.com/gusha915/no-ssr-battery-historian
    * base.html 替换原码下的 battery-historian/templates/base.html
    * cdn目录 放入到battery-historian/third_party 目录
    * go run setup.go
  * 自己编译的存在各种问题，貌似不能解析显示，数据可能存在问题，其实本质应该是Google没有发布后续版本，采用了docker的形式；
  * 荣耀10手机导出的bug report显示是正常的，可能还是跟Android系统版本有关系
    * [Battery Historian2.0使用过程中遇到的一些问题](https://blog.csdn.net/lhd201006/article/details/54287494)
      * 其实",vers,"，",bt,"和",bt,"都是在-- CHECKIN BATTERYSTATS (dumpsys batterystats -c) --下的，只不过这里这三行并不连续，中间穿插一大段数据内容，而刚才删除的那三行却是连续的，而且后面带的参数都是0，经过比较发现，后面带的参数本应该是uid，进程名等参数，这些参数是不可能都为0的所以就猜测刚才删除的那些数据可能是异常数据，也许就是这里导致视图分析报错，于是就把那一整段都全部删除：
    * 解压zip文件；
    * 删除压缩文件中的`bugreport-xxx-RP1A.200720.011-2021-06-21-15-31-54.txt`中的下面这段数据，然后图形显示正常
      ```
      9,0,i,ctr,0
      9,0,l,bt,0,90749,12551,242110,163911,1624260578842,80495,2297,3013,3013000,3013000,0
      9,0,l,gn,0,0,0,0,0,0,0,0,0,0
      9,0,l,gmcd,2937,385,0.0,0.0,0,0,0,0,0
      9,0,l,gwfl,0,0,0,0,0
      9,0,l,m,10254,0,0,324,0,0,10074,0,0,0,0,0,0,0,0,0,0,0,0,0,0
      9,0,l,br,2237,0,8017,0,0
      9,0,l,sgt,0,0,90749,0,0
      9,0,l,sst,0
      9,0,l,sgc,0,0,0,0,0
      9,0,l,dct,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
      9,0,l,dcc,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
      9,0,l,wst,0,0,0,0,0,0,0,0
      9,0,l,wsc,0,0,0,0,0,0,0,0
      9,0,l,wsst,0,0,0,0,0,0,0,0,0,0,0,0,0
      9,0,l,wssc,0,0,0,0,0,0,0,0,0,0,0,0,0
      9,0,l,wsgt,0,0,0,0,0
      9,0,l,wsgc,0,0,0,0,0
      9,0,l,wmct,0,0
      9,0,l,dc,0,0,0,0,0,0,0,0,0,0
      ```
    * Battery Historian加载bugreport-xxx-RP1A.200720.011-2021-06-21-15-31-54.txt解析显示
      * ![0008_Android_BatteryStats_Data_Modified.png](images/0008_Android_BatteryStats_Data_Modified.png)
      * Historian V2显示正常，Historian显示还是存在问题，这个貌似不是那么重要；

# Battery Historian Online

* https://bathist.ef.lc/
* 其他的方式貌似多少都是存在问题的，docker和自行编译都无法显示完整；

![0008_Android_BatteryStats_Online.png](images/0008_Android_BatteryStats_Online.png)

* Errors
  ```
  error getting appID from string: strconv.ParseInt: parsing "u0ai9000": invalid syntax
  strconv.ParseInt: parsing "0.0": invalid syntax
  open /usr/lib/go-1.6/lib/time/zoneinfo.zip: no such file or directory
  ** Error in 9,h,0,Bl=100,Bs=d,Bh=g,Bp=n,Bt=289,Bv=4279,Bcc=3013,Mrc=0,Wrc=0,+r,+w,+S,Pss=2,Sb=2,+Ud,Epr=0 with Mrc=0 : unknown key Mrc
  ** Error in 9,h,0,Bl=100,Bs=d,Bh=g,Bp=n,Bt=289,Bv=4279,Bcc=3013,Mrc=0,Wrc=0,+r,+w,+S,Pss=2,Sb=2,+Ud,Epr=0 with Wrc=0 : unknown key Wrc
  ** Error in 9,h,0,Bl=100,Bs=d,Bh=g,Bp=n,Bt=289,Bv=4279,Bcc=3013,Mrc=0,Wrc=0,+r,+w,+S,Pss=2,Sb=2,+Ud,Epr=0 with +Ud : unknown key Ud
  ** Error in 9,h,834,-Ud,+Ewl=33 with -Ud : unknown key Ud
  ** Error in 9,h,0,+Ud,-Ewl=40 with +Ud : unknown key Ud
  open /usr/lib/go-1.6/lib/time/zoneinfo.zip: no such file or directory
  ```
* 有报错，但依然能够正常显示，自己弄的服务器就无法显示正常

# bug report

* battery可以查看电池信息，batterystats可以查看电池消耗信息；
* 打开开发者模式
* adb shell dumpsys battery
  ```
  Current Battery Service state:
    AC powered: false
    USB powered: true
    Wireless powered: false
    Max charging current: 500000
    Max charging voltage: 5000000
    Charge counter: 2092360
    status: 2
    health: 2
    present: true
    level: 68
    scale: 100
    voltage: 3913
    temperature: 311
    technology: Li-ion
  ```
* adb shell dumpsys batterystats --enable full-wake-history
* adb shell dumpsys batterystats --reset
* 拔出USB
  * 为什么要拔出USB? 因为如果你一直插着USB，如果电充满了，你的数据会被清空的。batterystats只会记录最后一次充满电后的记录，因此强烈建议先把电充满，完成以上操作后，拔出USB电源。
* 等个几分钟
* 插入USB
* adb shell dumpsys batterystats --history
  ```
  Battery History (0% used, 784 used of 4096KB, 14 strings using 770):
                      0 (14) RESET:TIME: 2021-06-01-18-04-06
                      0 (1) 070 status=charging health=good plug=usb temp=311 volt=4017 charge=2153 modemRailChargemAh=0 wifiRailChargemAh=0 +running +plugged +usb_data
                      0 (2) 070 fg=u0a58:"com.debug.loggerui"
                      0 (2) 070 top=1001:"com.mediatek.engineermode"
                      0 (2) 070 user=0:"0"
                      0 (2) 070 userfg=0:"0"
                   +4ms (2) 070 stats=0:"wakelock-change"
                  +75ms (3) 070 +wake_lock=1000:"*alarm*:TIME_TICK" stats=0:"dump"
               +1s751ms (1) 070 -wake_lock
               +5s404ms (4) 070 +wake_lock=-1:"screen" +screen brightness=medium screenwake=1000:"android.server.power:PLUGGED:false"
               +5s439ms (2) 070 stats=0:"battery-state"
               +5s543ms (4) 070 status=discharging plug=none temp=319 volt=3927 -plugged -usb_data stats=0:"screen-state"
               +8s191ms (3) 070 -wake_lock -screen brightness=dark stats=0:"screen-state"
              +10s868ms (2) 070 wake_reason=0:"Abort:noirq suspend of  device failed"
              +12s335ms (1) 070 -running
            +1m02s280ms (2) 070 +running +wake_lock=1000:"*alarm*:TIME_TICK" wake_reason=0:"179:SPM"
            +1m02s362ms (1) 070 -wake_lock
            +1m03s782ms (1) 070 -running
            +2m03s296ms (2) 070 +running +wake_lock=1000:"*alarm*:TIME_TICK" wake_reason=0:"179:SPM"
            +2m03s345ms (1) 070 -wake_lock
            +2m03s382ms (3) 070 volt=3905 wake_reason=0:"Abort:Last active Wakeup Source: bat_percent_notify_lock wakelock"
            +2m05s012ms (1) 070 -running
            +2m09s333ms (4) 070 +running +wake_lock=-1:"screen" +screen brightness=medium wake_reason=0:"179:SPM" screenwake=1000:"android.server.power:PLUGGED:true"
            +2m10s018ms (2) 070 stats=0:"battery-state"
            +2m10s082ms (3) 070 status=charging plug=usb temp=314 volt=3933 +plugged
            +2m10s105ms (4) 070 volt=4004 +audio +usb_data stats=0:"screen-state"
            +2m14s071ms (2) 070 -audio
            +2m17s964ms (2) 070 brightness=dark
            +2m20s303ms (3) 070 -wake_lock -screen stats=0:"screen-state"
            +2m28s937ms (2) 070 stats=0:"dump"
  
  Total cpu time reads: 0
  Batched cpu time reads: 0
  Batching Duration (min): 187
  All UID cpu time reads since the later of device start or stats reset: 36
  UIDs removed since the later of device start or stats reset: 0
  ```
* adb shell dumpsys batterystats > batterystats.txt
* adb bugreport
  ```
  /data/user_de/0/com.android.shell/files/bugreports/bugrepo...file pulled, 0 skipped. 7.1 MB/s (3062878 bytes in 0.413s)
  Bug report copied to X:\log\bugreport-xxx-RP1A.200720.011-2021-06-21-15-31-54.zip
  ```
  * Battery Historian针对Batterystats进行电池用量分析
  * adb bugreport bugreport.zip
* 手机端操作
  * 在Developer选项中，点击`Bug report`
  * 选择所需的错误报告类型，然后点击"report"
  * 在下拉状态栏就可以看到Bug report正在生成，等到生成完成
  * 可以看到进度条和前面个的`adb bugreport`有交互运行；
* [0008_bugreport-xxx-RP1A.200720.011-2021-06-21-15-31-54.zip](refers/0008_bugreport-xxx-RP1A.200720.011-2021-06-21-15-31-54.zip)

# 模块耗电配置

* frameworks/base/core/res/res/xml/power_profile.xml
  * 一般会被overlay
  * [0007_Android_res_Overlay.md](0007_Android_res_Overlay.md)
