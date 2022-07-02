# Android SensorHub APP

Sensor应用层校正操作

# 参考文档

* [0005_Android_Sensors.md](0005_Android_Sensors.md)

# SensorHub工具

* vendor/mediatek/proprietary
  * packages/apps/SensorHub
    * Android APP
  * external/sensor-tools/calibration_tool
    * 命令行工具
  * external/sensor-tools/libhwm.c
    * 共享库

# Engineer Mode校正报错

* log
  ```
  07-26 20:27:00.639  3417  3417 D SH/CalibrationN: start static calibration
  07-26 20:27:00.639  1111  1238 V PlayerBase: baseStart() piid=15
  07-26 20:27:00.639  1111  1238 V AudioService.PlaybackActivityMonitor: playerEvent(piid=15, event=2)
  07-26 20:27:00.640  3417  3508 D SH/CalibrationN: startCalibration(), operation 2
  07-26 20:27:00.640  3417  3508 D SENSOR-JNI: Enter gyroscope_start_static_calibration()
  07-26 20:27:00.640  3417  3508 E HWMLIB  : gyroscope_start_static_calibration: Couldn't find or open file sensor (Permission denied)
  07-26 20:27:00.640  3417  3508 D SENSOR-JNI: gyroscope_start_static_calibration() returned -13
  07-26 20:27:00.641  3417  3508 D SH/CalibrationN: startCalibration(), ret -13
  07-26 20:27:00.641  3417  3417 D SH/CalibrationN: set fail
  ```
  * gyroscope_start_static_calibration: Couldn't find or open file sensor (Permission denied)
    ```
    * vendor/mediatek/proprietary/external/sensor-tools/include/libhwm.h
      * #define GYROSCOPE_NAME                  "/dev/gyroscope"
    ```
* adb root
* adb shell chmod 777 /dev/gyroscope

# SensorHub APP调用关系

```
* vendor/mediatek/proprietary/packages/apps/SensorHub
  * vendor/mediatek/proprietary/packages/apps/SensorHub/src/com/mediatek/sensorhub/sensor/SensorCalibrationNew.java
    * public class SensorCalibrationNew extends Activity implements OnClickListener
      * private SensorEventListener mSensorEventListener = new SensorEventListener()
        * public void onSensorChanged(SensorEvent event)
          * mCurrentData.setText(String.format(Locale.ENGLISH, "%+8.4f,%+8.4f,%+8.4f", event.values[0], event.values[1], event.values[2]));
          * status = status + "Medium";
      * public void onCreate(Bundle savedInstanceState)
        * mStartCalibration = (Button) findViewById(R.id.button_sensor_calibration_start);
        * mStartCalibration.setOnClickListener(this);
        * mHandler = new Handler(mHandlerThread.getLooper())
          * MSG_START_CALIBRARION == msg.what
            * startCalibration(msg.what);
              * mType == GSENSOR
                * result = EmSensor.startGsensorCalibration();
                  * vendor/mediatek/proprietary/packages/apps/SensorHub/src/com/mediatek/sensorhub/sensor/EmSensor.java
                    * public static native int startGsensorCalibration();
                      * vendor/mediatek/proprietary/packages/apps/SensorHub/jni/sensor/com_mediatek_sensorhub_sensor.cpp
                        * JNIEXPORT jint JNICALL Java_com_mediatek_sensorhub_sensor_EmSensor_startGsensorCalibration(JNIEnv *, jclass)
                          * int ret = gsensor_start_static_calibration();
                            * vendor/mediatek/proprietary/external/sensor-tools/libhwm.c
                                * int gsensor_start_static_calibration(void)
                                  * 下面介绍
      * public void onClick(View arg0)
        * mHandler.sendEmptyMessage(MSG_START_CALIBRARION);
* vendor/mediatek/proprietary/packages/apps/SensorHub/jni/sensor/Android.mk
  * LOCAL_C_INCLUDES += $(MTK_PATH_SOURCE)/external/sensor-tools
* vendor/mediatek/proprietary/external/sensor-tools
  * vendor/mediatek/proprietary/external/sensor-tools/libhwm.c
    * int gsensor_start_static_calibration(void)
      * fd = open(GSENSOR_NAME, O_RDONLY);
        * vendor/mediatek/proprietary/external/sensor-tools/include/libhwm.h
          * #define GSENSOR_NAME                    "/dev/gsensor"
          * #define GYROSCOPE_NAME                  "/dev/gyroscope"
          * #define ALSPS_NAME                      "/dev/als_ps"
          * #define MSENSOR_NAME                    "/dev/msensor"
        * adb shell ls -al /dev/gsensor
          * crw-rw---- 1 radio system 10,  12 2010-01-01 00:00 gsensor
     * if (fd < 0) {
        * HWMLOGE("Couldn't find or open file sensor (%s)", strerror(errno));
          * HWMLIB  : gsensor_start_static_calibration: Couldn't find or open file sensor (Permission denied)
            * adb shell chmod 666 /dev/gsensor
* vendor/app/SensorHub/SensorHub.apk
```
