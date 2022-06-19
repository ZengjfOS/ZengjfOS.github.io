# Android Battery Current

通过查看电池电流情况，了解系统深度休眠功耗情况

# 参考文档

* [0002_SPM_Power_Analysis.md](0002_SPM_Power_Analysis.md)
* [0004_Android_Typc-C_Charger.md](0004_Android_Typc-C_Charger.md)
* [0005_Android_Low_Power.md](0005_Android_Low_Power.md)
* https://www.kernel.org/doc/Documentation/ABI/testing/sysfs-class-power
* [[FAQ09903] Fuel Gauge兼容多电池，软件&硬件上应该怎么做？](https://online.mediatek.com/FAQ#/SW/FAQ09903)
* [Android 电量测试-电量分析（二）](https://www.jianshu.com/p/4a296481149a)

# 简要说明

* Battery current (Ibat) 
* Battery voltage (Vbat) 
* Battery State-of-Charge (SoC)
* NTC: 热敏电阻，根据电阻产生的分压不同，得到温度；
* ID: 根据不同内阻，判断不同的电池
* Rsense: 采样电阻

# 电池充放电

* 3CBatteryManager.apk
* 在设置选项中，电池可以将记录的数据保存出来
  * [History]
  * [左上角三条杠] -> [Settings] -> [Battery] -> [Export battery history]
* 修改监听参数
  * [左上角三条杠] -> [Settings] -> [Battery] -> [Monitoring]

# sysfs

* cd /sys/devices/platform/battery/power_supply/battery
* ls
  ```
  capacity       charge_full current_now device power   status    technology type   voltage_now
  charge_counter current_avg cycle_count health present subsystem temp       uevent
  ```
  * current_avg

# battery id

* 如果需要兼容多个电池，硬件上首先要有一个独立的电池ID pin，供软件做区分。一般做法，是电池端，制作多一个pin，该pin连接的阻值不同，通过BB端的ADC，获取的电压值就不同。从而软件上可以做区分。
* Android Q
  ```CPP
  // kernel-4.9/drivers/power/supply/mediatek/battery/mtk_battery_core.c
  
  void fgauge_get_profile_id(void)
  {
      int id_volt = 0;
      //int id = 0;
      int ret = 0;
  
      ret = IMM_GetOneChannelValue_Cali(BATTERY_ID_CHANNEL_NUM, &id_volt);
      if (ret != 0)
          bm_debug("[%s]id_volt read fail\n", __func__);
      else
          bm_debug("[%s]id_volt = %d\n", __func__, id_volt);
  
      if ((sizeof(g_battery_id_voltage) /
          sizeof(int)) != TOTAL_BATTERY_NUMBER) {
          bm_debug("[%s]error! voltage range incorrect!\n",
              __func__);
          return;
      }
  /*
      for (id = 0; id < TOTAL_BATTERY_NUMBER; id++) {
          if (id_volt < g_battery_id_voltage[id]) {
              gm.battery_id = id;
              break;
          } else if (g_battery_id_voltage[id] == -1) {
              gm.battery_id = TOTAL_BATTERY_NUMBER - 1;
          }
      }
  */
      if (id_volt < Vekan_Battery_Volt) {
          bm_err("select Veken Battery\n");
          gm.battery_id = 1;
      }
      else if (id_volt < Icon_Battery_Volt) {
          bm_err("select Icon Energy Battery\n");
          gm.battery_id = 0;
      }
      else
      {
          bm_err("[%s]error! voltage range incorrect!\n",
              __func__);
      }
  
      bm_debug("[%s]Battery id (%d)\n",
          __func__,
          gm.battery_id);
  }
  ```
* Android R
  ```CPP
  // drivers/power/supply/mtk_battery.c
  
  int fgauge_get_profile_id(void)
  {
          const char *battery_id_cmd;
          int battery_id = 0;
  
          battery_id_cmd = cmdline_get_value("androidboot.battery.id");
          if(strcmp(battery_id_cmd, "0") == 0)
          {
                  battery_id = 0;
          }
          else if (strcmp(battery_id_cmd, "1") == 0)
          {
                  battery_id = 1;
          }
          printk("battery_id = %d\n",battery_id);
          return battery_id;
  }
  ```

# 电池的信息

* lk
  * vendor/mediatek/proprietary/bootable/bootloader/lk/target/k62v1_64_bsp/include/target/cust_battery.h
* Kernel
  * Android Q
    * kernel-4.9/drivers/misc/mediatek/include/mt-plat/mt6765/include/mach/mtk_battery_table.h
  * Android R
    * kernel-4.9/drivers/power/supply/mtk_battery_table.h
