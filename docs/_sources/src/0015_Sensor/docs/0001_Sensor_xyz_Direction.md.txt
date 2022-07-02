# Sensor xyz Direction

PCBA板传感器贴片位置不同，怎么确定及调整xyz

# 方位确定

参考文档: [0001_cell_phone_sensor_calibration.pdf](refers/0001_cell_phone_sensor_calibration.pdf)

# 方向校正

* kernel-4.9/drivers/misc/mediatek/sensors-1.0/hwmon/hwmsen/hwmsen_helper.c
  ```C
  struct hwmsen_convert map[] = {
      { { 1, 1, 1}, {0, 1, 2} },
      { {-1, 1, 1}, {1, 0, 2} },
      { {-1, -1, 1}, {0, 1, 2} },
      { { 1, -1, 1}, {1, 0, 2} },
  
      { {-1, 1, -1}, {0, 1, 2} },
      { { 1, 1, -1}, {1, 0, 2} },
      { { 1, -1, -1}, {0, 1, 2} },
      { {-1, -1, -1}, {1, 0, 2} },
  
  };
  ```
* 如上map为:
  * xyz正负方向变换
  * xyz轴位置重映射
* cd /sys/bus/platform/drivers/gsensor
  * echo 6 > layout
