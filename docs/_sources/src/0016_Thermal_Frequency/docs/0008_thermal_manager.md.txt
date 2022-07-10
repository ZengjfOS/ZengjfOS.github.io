# thermal manager

mtk thermal manager加载MTK温控策略

# Android.mk

vendor/mediatek/proprietary/external/thermal_managerlib/Android.mk

```makefile
LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)
LOCAL_MULTILIB := 32
LOCAL_MODULE_TAGS := optional
LOCAL_SRC_FILES := thermal_manager.c
LOCAL_SHARED_LIBRARIES := libdl libcutils liblog
LOCAL_MODULE := thermal_manager
LOCAL_PROPRIETARY_MODULE := true
LOCAL_MODULE_OWNER := mtk
LOCAL_INIT_RC := init.thermal_manager.rc
include $(MTK_EXECUTABLE)

include $(CLEAR_VARS)
LOCAL_MODULE:= libmtcloader
LOCAL_PROPRIETARY_MODULE := true
LOCAL_MODULE_OWNER := mtk
LOCAL_MODULE_CLASS := SHARED_LIBRARIES
LOCAL_SRC_FILES_arm :=lib/libmtcloader.so
LOCAL_SRC_FILES_arm64 :=lib64/libmtcloader.so
LOCAL_SHARED_LIBRARIES := libc++ libc libcutils libdl liblog libm

#bobule workaround pdk build error, needing review
LOCAL_MULTILIB := both
LOCAL_MODULE_SUFFIX := .so

include $(BUILD_PREBUILT)
```

# rc

* [0008_init.thermal_manager.rc](refers/0008_init.thermal_manager.rc)
  * 只运行一次

# thermal_manager

* [0008_thermal_manager.c](refers/0008_thermal_manager.c)
  * 这个程序加载完策略之后就退出了，其他的貌似没做什么

# log

```
2728:<14>[    6.707723] .(0)[1:init]init 22: Parsing file /vendor/etc/init/init.thermal_manager.rc...
4493:<14>[   15.054742] .(0)[1:init]init 28: [14542][0]starting service 'thermal_manager'...
4506:<14>[   15.170902] .(0)[267:init]init 22: [15161][24]ReapLogC PropSet [vendor.MB.sublog]=[0x001AD581]15004 [vendor.mtklog.netlog.Running]=[0]15019 [init.svc.camerahalserver]=[running]15023 [ro.boottime.camerahalserver]=[15007018692]15024 [init.svc_debug_pid.camerahalserver]=[656]15024 [vendor.MB.ftrace.log]=[bsp]15033 [init.svc.thermal]=[running]15044 [ro.boottime.thermal]=[15028360308]15045 [init.svc_debug_pid.thermal]=[660]15045 [persist.vendor.connsys.patch.version]=[220428180500000]15071 [init.svc.thermal_manager]=[running]15087 [ro.boottime.thermal_manager]=[15062463692]15088 [init.svc_debug_pid.thermal_manager]=[663]15088 [init.svc.thermalloadalgod]=[running]15135 [ro.boottime.thermalloadalgod]=[15092915308]15136 [init.svc_debug_pid.thermalloadalgod]=[667]15137 [init.svc.pq-2-2]=[running]15162 Done
4523:<5>[   15.284354] .(0)[663:thermal_manager][Thermal/TZ/BTS] mtkts_bts_prepare_table table_num=7
4524:<5>[   15.285677] .(0)[663:thermal_manager][Thermal/TZ/BTSMDPA] mtkts_btsmdpa_prepare_table table_num=7
4529:<5>[   15.304942] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_write_atm_setting input 0 2000 10 15 1 685 0 280 0
4530:<5>[   15.306310] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_write_dtm_setting applied 0 2000 10 15 1 685 697 287 727
4531:<5>[   15.308083] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_write_atm_setting input 1 1000 10 15 1 400 0 220 0
4532:<5>[   15.319008] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_write_dtm_setting applied 1 1000 10 15 1 400 697 287 727
4533:<5>[   15.320839] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_write_ctm input 2 85000 55000 43000 46000 75000 51000 515000 10000 419000 8000 500 500 13500 -1
4534:<5>[   15.323961] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_unbind unbinding OK
4535:<5>[   15.324957] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_unbind unbinding OK
4536:<5>[   15.326012] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_unbind unbinding OK
4537:<5>[   15.326998] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_unbind unbinding OK
4541:<5>[   15.356513] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_bind binding OK, 0
4542:<5>[   15.357508] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_bind binding OK, 2
4543:<5>[   15.358630] .(0)[663:thermal_manager][Thermal/TZ/CPU]tscpu_bind binding OK, 1
4544:<5>[   15.359908] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_write] mtktspmic_unregister_thermal
4545:<5>[   15.361120] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_unregister_thermal]
4550:<5>[   15.395753] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_write] g_THERMAL_TRIP_0=0,g_THERMAL_TRIP_1=0,g_THERMAL_TRIP_2=0,
4551:<5>[   15.395761] .(0)[663:thermal_manager][Thermal/TZ/PMIC] g_THERMAL_TRIP_3=0,g_THERMAL_TRIP_4=0,g_THERMAL_TRIP_5=0,g_THERMAL_TRIP_6=0,
4552:<5>[   15.397284] .(0)[663:thermal_manager][Thermal/TZ/PMIC] g_THERMAL_TRIP_7=0,g_THERMAL_TRIP_8=0,g_THERMAL_TRIP_9=0,
4555:<5>[   15.440800] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_write] cooldev0=mtktspmic-sysrst,cooldev1=no-cooler,cooldev2=no-cooler,cooldev3=no-cooler,cooldev4=no-cooler,
4556:<5>[   15.440812] .(0)[663:thermal_manager][Thermal/TZ/PMIC] cooldev5=no-cooler,cooldev6=no-cooler,cooldev7=no-cooler,cooldev8=no-cooler,cooldev9=no-cooler
4557:<5>[   15.444611] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_write] trip_0_temp=136000,trip_1_temp=110000,trip_2_temp=100000,trip_3_temp=90000,
4558:<5>[   15.444618] .(0)[663:thermal_manager][Thermal/TZ/PMIC] trip_4_temp=80000,trip_5_temp=70000,trip_6_temp=65000,trip_7_temp=60000,trip_8_temp=55000,
4559:<5>[   15.446369] .(0)[663:thermal_manager][Thermal/TZ/PMIC] trip_9_temp=50000,time_ms=1000
4560:<5>[   15.476985] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_write] mtktspmic_register_thermal
4561:<5>[   15.479647] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_register_thermal]
4565:<5>[   15.507087] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_bind] mtktspmic-sysrst
4566:<5>[   15.508200] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_bind] binding OK, 0
4569:<4>[   15.527085] -(0)[663:thermal_manager]mt635x_auxadc_read_raw: 25 callbacks suppressed
4570:<6>[   15.527097] .(0)[663:thermal_manager]mt635x-auxadc mt635x-auxadc: name:CHIP_TEMP, channel=4, adc_out=0x61d, adc_result=687
4572:<5>[   15.538781] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [pmic_raw_to_temp] t_current=36018
4575:<5>[   15.542013] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [pmic_debug] Raw=687, T=36018
4576:<5>[   15.543035] .(0)[663:thermal_manager][Thermal/TZ/PMIC] [mtktspmic_get_hw_temp] pre_temp1=36018
4578:<6>[   15.582301] .(0)[663:thermal_manager]mt635x-auxadc mt635x-auxadc: name:BAT_TEMP, channel=3, adc_out=0x5ae, adc_result=638
4580:<6>[   15.598904] .(0)[663:thermal_manager]mt635x-auxadc mt635x-auxadc: name:VBIF, channel=11, adc_out=0xffe, adc_result=1799
4581:<5>[   15.614964] .(0)[663:thermal_manager][Thermal/tzcharger]BTSCHARGER ret = 336, temperature = 27
4718:<4>[   16.437889] .(0)[663:thermal_manager][HIF-SDIO][I]wmt_dev_tm_temp_query:[Thermal] current_temp = 0x1b
4723:<14>[   16.462342] .(0)[1:init]init 28: [16453][0]Service 'thermal_manager' (pid 663) exited with status 0 oneshot service took 1.391000 seconds in background
4724:<14>[   16.464232] .(0)[1:init]init 22: [16453][0]Sending signal 9 to service 'thermal_manager' (pid 663) process group...
4731:<14>[   16.638063] .(0)[267:init]init 31: [16629][91]ReapLogT PropSet [init.svc.usbd]=[stopped]16429 [init.svc_debug_pid.usbd]=[]16434 [init.svc.thermal_manager]=[stopped]16459 [init.svc_debug_pid.thermal_manager]=[]16461 [vendor.MB.running]=[1]16535 [vendor.MB.prdebug]=[1]16537 [log.tag]=[M]16538 Done
```
