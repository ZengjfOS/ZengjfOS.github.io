# temperature frequence CPU

获取CPU温度、频率

## 温度

* cd /sys/class/thermal
* ls -al
  ```
  total 0
  drwxr-xr-x  2 root root 0 Jun 12 10:21 .
  drwxr-xr-x 64 root root 0 Feb 14  2019 ..
  lrwxrwxrwx  1 root root 0 Jun 12 10:21 thermal_zone0 -> ../../devices/virtual/thermal/thermal_zone0
  ```
* cat /sys/class/thermal/thermal_zone0/temp
  ```
  34563
  ```

## 频率

* /sys/devices/system/cpu
  * sudo cat cpu0/cpufreq/cpuinfo_cur_freq
  * sudo cat cpu1/cpufreq/cpuinfo_cur_freq
  * sudo cat cpu2/cpufreq/cpuinfo_cur_freq
  * sudo cat cpu3/cpufreq/cpuinfo_cur_freq
