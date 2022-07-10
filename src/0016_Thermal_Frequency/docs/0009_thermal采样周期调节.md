# thermal 采用周期调节

通过当前温度调节采样周期

# 采样周期调节

kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones/mtk_ts_btscharger.c

```C
/* This is to preserve last temperature readings from charger driver.
 * In case mtk_ts_charger.c fails to read temperature.
 */
/**
 * If curr_temp >= polling_trip_temp1, use interval
 * else if cur_temp >= polling_trip_temp2 && curr_temp < polling_trip_temp1,
 *  use interval*polling_factor1
 * else, use interval*polling_factor2
 */
static int polling_trip_temp1 = 40000;
static int polling_trip_temp2 = 20000;
static int polling_factor1 = 5000;
static int polling_factor2 = 10000;

// ...省略

static int mtktscharger_get_temp(struct thermal_zone_device *thermal, int *t)
{
    *t = mtktscharger_get_hw_temp() * 1000;
    mtktscharger_dprintk("%s %d\n", __func__, *t);

    if (*t >= 85000)
        mtktscharger_dprintk_always("HT %d\n", *t);

    if ((int)*t >= polling_trip_temp1)
        thermal->polling_delay = interval * 1000;
    else if ((int)*t < polling_trip_temp2)
        thermal->polling_delay = interval * polling_factor2;
    else
        thermal->polling_delay = interval * polling_factor1;

    return 0;
}
```

* interval是在系统启动的，由thermal manager加载emmc中的vendor/etc/.tp/thermal.conf，写入驱动的参数
  * [0010_thermal.txt](refers/0010_thermal.txt)
    ```
    /proc/driver/thermal/tzcharger
    1 120000 0 mtktscharger-sysrst 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 2000
    ```
    * Polling interval: 2000
      * kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones/mtk_ts_charger.c
        * `static unsigned int interval; /* seconds, 0 : no auto polling */`
