# thermal zones btscharger

btscharger温度控制系统工作原理

# 代码位置

kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones

```
.
├── Makefile
├── mtk_ts_6311buck.c
├── mtk_tsAll.c
├── mtk_ts_battery.c
├── mtk_ts_bif.c
├── mtk_ts_bts.c
├── mtk_ts_btscharger.c
├── // ...省略
├── mtk_ts_wmt_766x.c
├── mtk_ts_wmt.c
└── ts_da.c

0 directories, 27 files
```

# Makefile

kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones/Makefile

```makefile
ifneq (,$(filter $(CONFIG_MTK_PLATFORM), "mt6761"))

obj-$(CONFIG_THERMAL) += mtk_ts_battery.o

obj-$(CONFIG_THERMAL) += mtk_ts_bts.o
obj-$(CONFIG_THERMAL) += mtk_ts_btsmdpa.o

obj-$(CONFIG_THERMAL) += mtk_ts_cpu_noBank.o
obj-$(CONFIG_THERMAL) += mtk_ts_pa.o
obj-$(CONFIG_THERMAL) += mtk_ts_pa_thput.o
obj-$(CONFIG_THERMAL) += mtk_ts_pmic.o
ifneq (,$(findstring tb8766, $(CONFIG_ARCH_MTK_PROJECT)))
ifneq ($(CONFIG_CHARGER_BQ25601),)
obj-$(CONFIG_THERMAL) += mtk_ts_btscharger.o
else
obj-$(CONFIG_THERMAL) += mtk_ts_charger.o
endif
else
obj-$(CONFIG_THERMAL) += mtk_ts_charger.o
endif
obj-$(CONFIG_THERMAL) += mtk_ts_charger2.o

ifneq ($(CONFIG_MTK_COMBO_WIFI),)
    obj-$(CONFIG_THERMAL) += mtk_ts_wmt.o
endif

obj-$(CONFIG_THERMAL) += mtk_tsAll.o
obj-$(CONFIG_THERMAL) += mtk_ts_imgsensor.o
obj-$(CONFIG_THERMAL) += mtk_ts_dctm.o
endif
```

* cat /sys/class/thermal/thermal_zone*/type
  ```
  mtktsbattery
  mtktsAP
  mtktsdctm
  // ...省略
  ```
  * mtktscharger
    * 18
* ls -1 thermal_zone*/type
  ```
  thermal_zone0/type
  thermal_zone1/type
  thermal_zone10/type
  // ...省略
  ```
  * thermal_zone24/type
    * 18
* ls /proc/driver/thermal
  ```
  clVR_FPS_status          mdm_timeout      tzcpu_Tj_out_via_HW_pin  tzimgs4
  cl_cam_dual_off_setting  mdm_value        tzcpu_cal                tzimgs5
  // ...省略
  mdm_sw                   tzcpu            tzimgs3                  wifi_in_soc
  ```

# MTK_THERMAL_WRAPPER_BYPASS

MTK替换了Linux默认的热管控的注册处理代码

```C
/*
 *  MTK_THERMAL_WRAPPER_BYPASS = 1 (use original Linux Thermal API)
 *  MTK_THERMAL_WRAPPER_BYPASS = 0 (use MTK Thermal API Monitor)
 */
#define MTK_THERMAL_WRAPPER_BYPASS 0

#if MTK_THERMAL_WRAPPER_BYPASS
/* Original LTF API */
#define mtk_thermal_zone_device_register      thermal_zone_device_register
#define mtk_thermal_zone_device_unregister    thermal_zone_device_unregister
#define mtk_thermal_cooling_device_unregister thermal_cooling_device_unregister
#define mtk_thermal_cooling_device_register   thermal_cooling_device_register
#define mtk_thermal_zone_bind_cooling_device  thermal_zone_bind_cooling_device

#else
// ...省略
#define mtk_thermal_zone_device_register    \
        mtk_thermal_zone_device_register_wrapper

#define mtk_thermal_zone_device_unregister  \
        mtk_thermal_zone_device_unregister_wrapper

#define mtk_thermal_cooling_device_unregister   \
        mtk_thermal_cooling_device_unregister_wrapper

#define mtk_thermal_cooling_device_register \
        mtk_thermal_cooling_device_register_wrapper

#define mtk_thermal_zone_bind_cooling_device    \
        mtk_thermal_zone_bind_cooling_device_wrapper

#endif
```

# driver

log

```
[ 8912.940174] (2)[4531:kworker/2:3][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 363, temperature = 25
[ 8923.180126] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 363, temperature = 25
[ 8933.420137] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 364, temperature = 25
[ 8943.660130] (2)[4531:kworker/2:3][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 364, temperature = 25
[ 8953.900116] (2)[4531:kworker/2:3][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 364, temperature = 25
[ 8964.140080] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 363, temperature = 25
[ 8974.379622] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 8984.620085] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 364, temperature = 25
[ 8994.860176] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9005.100112] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9015.340118] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9025.580084] (2)[4531:kworker/2:3][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9035.820114] (2)[4531:kworker/2:3][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9046.060065] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9056.299681] (2)[4525:kworker/2:2][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9066.539617] (2)[4734:kworker/2:1][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9066.564829] (2)[4735:cat][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9076.779662] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 365, temperature = 25
[ 9087.020103] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9097.260112] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9107.500108] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9117.740117] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 366, temperature = 25
[ 9127.980193] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9138.219786] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9148.460160] (2)[4734:kworker/2:1][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9158.700133] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9168.116669] (0)[4746:cat][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9168.940097] (2)[4733:kworker/2:0][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
[ 9172.562219] (2)[4747:cat][name:mtk_ts_btscharger&][name:mtk_ts_btscharger&][Thermal/tzcharger]BTSCHARGER ret = 367, temperature = 25
```

* btscharger最终通过mtk_auxadc.c提供的adc接口获取温度电压
* 通过mtktscharger_register_cooler()注册冷却操作
* 通过mtktscharger_register_thermal()注册热电偶设备
* 注册proc文件系统接口，用于向用户空间获取提供信息
  * /proc/driver/thermal/tzcharger
  * /proc/driver/thermal/tzcharger_param

```
* kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones/mtk_ts_btscharger.c
  └── late_initcall(mtktscharger_init);
      └── static int __init mtktscharger_init(void)
          ├── mtkts_btscharger_prepare_table(g_RAP_ntc_table);
          │   └── switch (table_num)
          │       └── case 1:
          │           ├── BTSCHARGER_Temperature_Table = BTSCHARGER_Temperature_Table1;
          │           └── ntc_tbl_size = sizeof(BTSCHARGER_Temperature_Table1);
          ├── err = mtktscharger_register_cooler();
          │   ├── cl_dev_sysrst = mtk_thermal_cooling_device_register("mtktscharger-sysrst", NULL, &mtktscharger_cooling_sysrst_ops);
          │   │   └── mtktscharger_cooling_sysrst_ops
          │   │       └── static struct thermal_cooling_device_ops mtktscharger_cooling_sysrst_ops
          │   │           └── .set_cur_state = mtktscharger_sysrst_set_cur_state,
          │   │               └── static int mtktscharger_sysrst_set_cur_state(struct thermal_cooling_device *cdev, unsigned long state)
          │   │                   ├── cl_dev_sysrst_state = state;
          │   │                   └── if (cl_dev_sysrst_state == 1)
          │   │                       └── pr_notice("[Thermal/mtktscharger_sysrst] reset, reset, reset!!!\n");
          │   └── mtk_thermal_cooling_device_register
          │       └── kernel-4.19/drivers/misc/mediatek/include/mt-plat/mtk_thermal_monitor.h
          │           └── #define mtk_thermal_cooling_device_register mtk_thermal_cooling_device_register_wrapper
          │               └── kernel-4.19/drivers/misc/mediatek/thermal/mtk_thermal_monitor.c
          │                   ├── mcdata = kzalloc(sizeof(struct mtk_thermal_cooler_data), GFP_KERNEL);
          │                   ├── mcdata->ops = (struct thermal_cooling_device_ops *)ops;
          │                   └── ret = thermal_cooling_device_register(type, mcdata, &mtk_cooling_wrapper_dev_ops);
          ├── err = mtktscharger_register_thermal();
          │   ├── thz_dev = mtk_thermal_zone_device_register("mtktscharger", num_trip, NULL, &mtktscharger_dev_ops, 0, 0, 0, interval * 1000);
          │   │   └── mtktscharger_dev_ops
          │   │       └── static struct thermal_zone_device_ops mtktscharger_dev_ops
          │   │           ├── .get_temp = mtktscharger_get_temp,
          │   │           │   └── static int mtktscharger_get_temp(struct thermal_zone_device *thermal, int *t)
          │   │           │       └── *t = mtktscharger_get_hw_temp() * 1000;
          │   │           │           ├── Channel = g_RAP_ADC_channel
          │   │           │           │   └── static int g_RAP_ADC_channel = BTSCHARGER_RAP_ADC_CHANNEL;
          │   │           │           │       └── #define BTSCHARGER_RAP_ADC_CHANNEL      AUX_IN2_NTC
          │   │           │           │           └── #define AUX_IN2_NTC (2)
          │   │           │           └── ret_value = IMM_GetOneChannelValue(Channel, data, &ret_temp);
          │   │           │               └── kernel-4.19/drivers/misc/mediatek/auxadc/mtk_auxadc.c
          │   │           │                   └── return IMM_auxadc_GetOneChannelValue(dwChannel, data, rawdata);
          │   │           └── .get_trip_temp = mtktscharger_get_trip_temp,
          │   │               └── static int mtktscharger_get_trip_temp(struct thermal_zone_device *thermal, int trip, int *temp)
          │   │                   └── *temp = trip_temp[trip];
          │   │                       └── static int trip_temp[10] = { 125000, 110000, 100000, 90000, 80000, 70000, 65000, 60000, 55000, 50000 };
          │   └── mtk_thermal_zone_device_register
          │       └── #define mtk_thermal_zone_device_register    mtk_thermal_zone_device_register_wrapper
          │           └── kernel-4.19/drivers/misc/mediatek/thermal/mtk_thermal_monitor.c
          │               └── struct thermal_zone_device *mtk_thermal_zone_device_register_wrapper(char *type, int trips, void *devdata, const struct thermal_zone_device_ops *ops, int tc1, int tc2, int passive_delay, int polling_delay)
          ├── mtktscharger_dir = mtk_thermal_get_proc_drv_therm_dir_entry();
          └── } else {
              ├── entry = proc_create("tzcharger", 0664, mtktscharger_dir, &tktscharger_fops);
              │   └── static const struct file_operations mtktscharger_fops
              │       └── .open = mtktscharger_open,
              └── entry = proc_create("tzcharger_param", 0664, mtktscharger_dir, &mtkts_btscharger_param_fops);
                  └── static const struct file_operations mtkts_btscharger_param_fops
                      └── .open = mtkts_btscharger_param_open,
                          └── return single_open(file, mtkts_btscharger_param_read, NULL);
                              ├── seq_printf(m, "%d\n", g_RAP_pull_up_R);
                              │   └── static int g_RAP_pull_up_R = BTSCHARGER_RAP_PULL_UP_R;
                              │       └── #define BTSCHARGER_RAP_PULL_UP_R        390000
                              │           └── 390K, pull up resister
                              ├── seq_printf(m, "%d\n", g_RAP_pull_up_voltage);
                              │   └── static int g_RAP_pull_up_voltage = BTSCHARGER_RAP_PULL_UP_VOLTAGE;
                              │       └── #define BTSCHARGER_RAP_PULL_UP_VOLTAGE  1800
                              │           └── 1.8V ,pull up voltage
                              ├── seq_printf(m, "%d\n", g_TAP_over_critical_low);
                              │   └── static int g_TAP_over_critical_low = BTSCHARGER_TAP_OVER_CRITICAL_LOW;
                              │       └── #define BTSCHARGER_TAP_OVER_CRITICAL_LOW    4397119
                              │           └── base on 100K NTC temp default value -40 deg
                              ├── seq_printf(m, "%d\n", g_RAP_ntc_table);
                              │   └── static int g_RAP_ntc_table = BTSCHARGER_RAP_NTC_TABLE;
                              │       └── #define BTSCHARGER_RAP_NTC_TABLE        7
                              │           └── default is NCP15WF104F03RC(100K)
                              └── seq_printf(m, "%d\n", g_RAP_ADC_channel);
                                  └── static int g_RAP_ADC_channel = BTSCHARGER_RAP_ADC_CHANNEL;
                                      └── #define BTSCHARGER_RAP_ADC_CHANNEL      AUX_IN2_NTC
                                          └── #define AUX_IN2_NTC (2)
                                              └── default is 2
```

* cat /proc/driver/thermal/tzcharger
  ```
  log=0
  polling delay=2000
  no of trips=1
  00      120000  0       mtktscharger-sysrst
  01      110000  0       no-cooler
  02      100000  0       no-cooler
  03      90000   0       no-cooler
  04      80000   0       no-cooler
  05      70000   0       no-cooler
  06      65000   0       no-cooler
  07      60000   0       no-cooler
  08      55000   0       no-cooler
  09      50000   0       no-cooler
  ```
  * log=0: 是否输出更多调试log
  * polling delay=2000:
  * no of trips=1
  * 之后的是触发温度，以及其对应的处理操作
* cat /proc/driver/thermal/tzcharger_param
  ```
  390000
  1800
  4397119
  7
  2
  ```
  * 390000: 上拉电阻
  * 1800: 上拉参考电压
  * 4397119: 最低温阻值
  * 7: ntc table总共有多少个，使用的时候会使用其中一个，可以认为是器件兼容
  * 2: adc channel
