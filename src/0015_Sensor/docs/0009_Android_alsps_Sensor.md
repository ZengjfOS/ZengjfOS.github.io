# Android alsps

快速获取近距、光感传感器数值

# p sensor 阈值如何设置

* PS一般都支持中断模式
* 通过过程中，当靠近psensor时，屏幕灭屏，靠近的距离主要和psensor设定的阈值有关。
* 阈值的设定方法如下，可以在工厂模式下，进入alsps测试选项，可观察到psensor的数值变化，此即为从p sensor寄存器读出来的数值，靠近和远离的时候观察对应数值，取对应距离下的数值作为阈值即可，一般为3cm或者4cm。
* 阈值可在cust_alsps.c内设定，high的阈值为靠近时灭屏的阈值，low阈值为远离时亮屏的阈值。
* 阈值不一定是固定的，采用的是自动校正，过一段时间校正一次，因为譬如在红外线充足的地方和在红外线少的情况下是不一样的，譬如夜间、太阳底下；

# Light sensor level和value的设置

* 在cust_alsps.c中，Als_level是从sensor读到的raw data，als_value是由als_level转换为上报android的值
* 这个对照关系暂时不知道怎么处理的

# i2ctools

* i2cget -f -y 1 0x23 0x87

# 寄存器读取

* adb shell
* cd /sys/bus/i2c/drivers/ltr559
* cat ps
* cat als
* cat reg
  ```
  reg:0x0080 value: 0x0000
  reg:0x0081 value: 0x0003
  reg:0x0082 value: 0x007F
  reg:0x0083 value: 0x0004
  reg:0x0084 value: 0x0002
  reg:0x0085 value: 0x0003
  reg:0x0086 value: 0x0092
  reg:0x0087 value: 0x0005
  reg:0x0088 value: 0x0000
  reg:0x0089 value: 0x0000
  reg:0x008A value: 0x0000
  reg:0x008B value: 0x0000
  reg:0x008C value: 0x0001
  reg:0x008D value: 0x0070
  reg:0x008E value: 0x0001
  reg:0x008F value: 0x0001
  reg:0x0090 value: 0x0003
  reg:0x0091 value: 0x0002
  reg:0x0092 value: 0x0000
  reg:0x0093 value: 0x0000
  reg:0x0094 value: 0x0000
  reg:0x0095 value: 0x0000
  reg:0x0097 value: 0x00FF
  reg:0x0098 value: 0x00FF
  reg:0x0099 value: 0x0000
  reg:0x009A value: 0x0000
  reg:0x009E value: 0x0020
  ```

# ps

近距传感器主要是玻璃的折射率和透光性影响比较大，自动校正解决噪声问题

## 静态配置

```diff
diff --git a/kernel-4.9/arch/arm64/boot/dts/mediatek/k62v1_64_bsp.dts b/kernel-4.9/arch/arm64/boot/dts/mediatek/k62v1_64_bsp.dts
index d227eed1240..fd67378e5cc 100755
--- a/kernel-4.9/arch/arm64/boot/dts/mediatek/k62v1_64_bsp.dts
+++ b/kernel-4.9/arch/arm64/boot/dts/mediatek/k62v1_64_bsp.dts
@@ -119,8 +119,8 @@
                power_vol                               = <0>;
                als_level = <0 328 861 1377 3125 7721 7767 12621 23062 28430 33274 47116 57694 57694 65535>;
                als_value = <0 133 304 502 1004 2005 3058 5005 8008 10010 12000 16000 20000 20000 20000 20000>;
-               ps_threshold_high               =  <70>;
-               ps_threshold_low                =  <40>;
+               ps_threshold_high               =  <300>;
+               ps_threshold_low                =  <245>;
                is_batch_supported_ps   = <0>;
                is_batch_supported_als  = <0>;
 };
diff --git a/kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c b/kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c
index 0b3c8003990..5c3f7afb0c9 100755
--- a/kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c
+++ b/kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c
@@ -20,7 +20,7 @@
 #include "ltr559.h"
 #include "alsps.h"

-#define GN_MTK_BSP_PS_DYNAMIC_CALI
+// #define GN_MTK_BSP_PS_DYNAMIC_CALI^M
  //#define DELAYED_PS_CALI
 //#define DEMO_BOARD
```

## 动态校正

* kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c

```C
#ifdef GN_MTK_BSP_PS_DYNAMIC_CALI
static int ltr559_dynamic_calibrate(void)
{
        //int ret = 0;
        int i = 0;
        int data;
        int data_total = 0;
        //ssize_t len = 0;
        int noise = 0;
        int count = 5;
        //int max = 0;
        int ps_thd_val_low, ps_thd_val_high;
        struct ltr559_priv *obj = ltr559_obj;

        if (!ltr559_obj)
        {
                APS_ERR("ltr559_obj is null!!\n");
                //len = sprintf(buf, "ltr559_obj is null\n");
                return -1;
        }

        for (i = 0; i < count; i++) {
                // wait for ps value be stable
                msleep(120);

                data = ltr559_ps_read(ltr559_obj->client, &ltr559_obj->ps);
                if (data < 0) {
                        i--;
                        continue;
                }

                if (data & 0x8000) {
                        break;
                }

                data_total += data;
        }

        noise = data_total / count;
        dynamic_calibrate = noise;

        if (noise < 100) {
                ps_thd_val_high = noise + 100;
                ps_thd_val_low  = noise + 50;
        }
        else if (noise < 200) {
                ps_thd_val_high = noise + 150;
                ps_thd_val_low  = noise + 60;
        }
        else if (noise < 300) {
                ps_thd_val_high = noise + 150;
                ps_thd_val_low  = noise + 60;
        }
        else if (noise < 400) {
                ps_thd_val_high = noise + 150;
                ps_thd_val_low  = noise + 60;
        }
        else if (noise < 600) {
                ps_thd_val_high = noise + 180;
                ps_thd_val_low  = noise + 90;
        }
        else if (noise < 1000) {
                ps_thd_val_high = noise + 300;
                ps_thd_val_low  = noise + 180;
        }
        else if (noise < 1250) {
                ps_thd_val_high = noise + 400;
                ps_thd_val_low  = noise + 300;
        }
        else {
                ps_thd_val_high = 1600;
                ps_thd_val_low  = 1400;
                APS_ERR("dynamic calibrate fails!!\n");
        }

        atomic_set(&obj->ps_thd_val_high, ps_thd_val_high);
        atomic_set(&obj->ps_thd_val_low, ps_thd_val_low);

        APS_LOG("%s:noise = %d\n", __func__, noise);
        APS_LOG("%s:obj->ps_thd_val_high = %d\n", __func__, ps_thd_val_high);
        APS_LOG("%s:obj->ps_thd_val_low = %d\n", __func__, ps_thd_val_low);

        return 0;
}
#endif
```

## 中断校正

`dynamic_calibrate - 50`测量值比噪声小这么多才会重新校准
```C
static void ltr559_eint_work(struct work_struct *work) 
{
        // ...省略
#ifndef DELAYED_PS_CALI
#ifdef GN_MTK_BSP_PS_DYNAMIC_CALI
        if(obj->ps > 20 && obj->ps < (dynamic_calibrate - 50)){
                if(obj->ps < 100){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+50);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+35);
                }else if(obj->ps < 200){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+50);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+35);
                }else if(obj->ps < 300){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+50);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+35);
                }else if(obj->ps < 400){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+50);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+35);
                }else if(obj->ps < 600){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+100);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+70);
                }else if(obj->ps < 1000){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+280);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+140);
                }else if(obj->ps < 1250){
                        atomic_set(&obj->ps_thd_val_high,  obj->ps+400);
                        atomic_set(&obj->ps_thd_val_low, obj->ps+240);
                }
                else{
                        atomic_set(&obj->ps_thd_val_high,  1400);
                        atomic_set(&obj->ps_thd_val_low, 1000);
                }

                dynamic_calibrate = obj->ps;
        }
#endif
        // ...省略
}
```

## 调试方法

* adb shell
* cd /sdcard/debuglogger/mobilelog
* grep ltr559_dynamic_calibrate * -R
* grep ltr559_eint_work * -R

# als

光感适配主要是要设置好光感的采集的数据和实际数据的mapper值，上层不用修改

## gain

将这里的64K量程修改成8K量程

`kernel-4.9/drivers/misc/mediatek/sensors-1.0/alsps/ltr559/ltr559.c`
```C
static int ltr559_init_client(void)
{
        // ...省略

        // Enable ALS to Full Range at startup
        als_gainrange = ALS_RANGE_64K;
        init_als_gain = als_gainrange;
        APS_ERR("ALS sensor gainrange %d!\n", init_als_gain);

        switch (init_als_gain)
        {
        case ALS_RANGE_64K:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range1);
                break;

        case ALS_RANGE_32K:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range2);
                break;

        case ALS_RANGE_16K:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range3);
                break;

        case ALS_RANGE_8K:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range4);
                break;

        case ALS_RANGE_1300:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range5);
                break;

        case ALS_RANGE_600:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range6);
                break;

        default:
                res = ltr559_i2c_write_reg(LTR559_ALS_CONTR, MODE_ALS_Range1);
                break;
        }

        // ...省略
}
```

## 传感器注册

```
* frameworks/base/services/core/java/com/android/server/display/DisplayPowerController.java
  * public DisplayPowerController(Context context, DisplayPowerCallbacks callbacks, Handler handler, SensorManager sensorManager, DisplayBlanker blanker)
    * String lightSensorType = resources.getString(com.android.internal.R.string.config_displayLightSensorType);
    * Sensor lightSensor = findDisplayLightSensor(lightSensorType);
    * mBrightnessMapper = BrightnessMappingStrategy.create(resources);
      * frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java
        * public static BrightnessMappingStrategy create(Resources resources)
          * isValidMapping(luxLevels, brightnessLevelsBacklight)
            * return new SimpleMappingStrategy(luxLevels, brightnessLevelsBacklight, autoBrightnessAdjustmentMaxGamma);
              * float[] luxLevels = getLuxLevels(resources.getIntArray(com.android.internal.R.array.config_autoBrightnessLevels));
                * mediatek/proprietary/packages/overlay/vendor/FrameworkResOverlay/brightness_adaptive_support/res/values/config.xml
                  ```
                  <integer-array name="config_autoBrightnessLevels">
                      <item>128</item>
                      <item>256</item>
                      <item>384</item>
                      <item>512</item>
                      <item>640</item>
                      <item>768</item>
                      <item>896</item>
                      <item>1024</item>
                      <item>2048</item>
                      <item>4096</item>
                      <item>6144</item>
                      <item>8192</item>
                      <item>10240</item>
                      <item>12288</item>
                      <item>14336</item>
                      <item>16384</item>
                      <item>18432</item>
                  </integer-array>
                  ```
              * int[] brightnessLevelsBacklight = resources.getIntArray(com.android.internal.R.array.config_autoBrightnessLcdBacklightValues);
                * mediatek/proprietary/packages/overlay/vendor/FrameworkResOverlay/brightness_adaptive_support/res/values/config.xml
                  ```
                  <integer-array name="config_autoBrightnessLcdBacklightValues">
                      <item>8</item>
                      <item>64</item>
                      <item>98</item>
                      <item>104</item>
                      <item>110</item>
                      <item>116</item>
                      <item>122</item>
                      <item>128</item>
                      <item>134</item>
                      <item>182</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                      <item>255</item>
                  </integer-array>
                  ```
    * mAutomaticBrightnessController = new AutomaticBrightnessController(this, handler.getLooper(), sensorManager, lightSensor, mBrightnessMapper, lightSensorWarmUpTimeConfig, mScreenBrightnessRangeMinimum, mScreenBrightnessRangeMaximum, dozeScaleFactor, lightSensorRate, initialLightSensorRate, brighteningLightDebounce, darkeningLightDebounce, autoBrightnessResetAmbientLuxAfterWarmUp, ambientBrightnessThresholds, screenBrightnessThresholds, shortTermModelTimeout, context.getPackageManager());
      * frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
        * public AutomaticBrightnessController(Callbacks callbacks, Looper looper, SensorManager sensorManager, Sensor lightSensor, BrightnessMappingStrategy mapper, int lightSensorWarmUpTime, int brightnessMin, int brightnessMax, float dozeScaleFactor, int lightSensorRate, int initialLightSensorRate, long brighteningLightDebounceConfig, long darkeningLightDebounceConfig, boolean resetAmbientLuxAfterWarmUpConfig, HysteresisLevels ambientBrightnessThresholds, HysteresisLevels screenBrightnessThresholds, long shortTermModelTimeout, PackageManager packageManager)
          * mHandler = new AutomaticBrightnessHandler(looper);
            * frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
              * private final class AutomaticBrightnessHandler extends Handler
                * public void handleMessage(Message msg)
                  * case MSG_UPDATE_AMBIENT_LUX:
                    * updateAmbientLux();
                      * updateAmbientLux(time);
          * mLightSensor = lightSensor;
          * private boolean setLightSensorEnabled(boolean enable)
            * mSensorManager.registerListener(mLightSensorListener, mLightSensor, mCurrentLightSensorRate * 1000, mHandler);
              * private final SensorEventListener mLightSensorListener = new SensorEventListener() {}
                * final float lux = event.values[0];
                * handleLightSensorEvent(time, lux);
                  * applyLightSensorMeasurement(time, lux);
                  * updateAmbientLux(time);
                    * updateAutoBrightness(true /* sendUpdate */, false /* isManuallySet */);
                      * float value = mBrightnessMapper.getBrightness(mAmbientLux, mForegroundAppPackageName, mForegroundAppCategory);
                        * int newScreenAutoBrightness = clampScreenBrightness(Math.round(value * PowerManager.BRIGHTNESS_ON));
                        * mScreenAutoBrightness = newScreenAutoBrightness;
                        * mCallbacks.updateBrightness();
              * mHandler是前面的定义的
```

## Framework调试

git diff frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java

```diff
diff --git a/frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java b/frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
index 31632dc007a..7f80e9de34e 100644
--- a/frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
+++ b/frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
@@ -128,7 +128,7 @@ class AutomaticBrightnessController {
     private final HysteresisLevels mAmbientBrightnessThresholds;
     private final HysteresisLevels mScreenBrightnessThresholds;

-    private boolean mLoggingEnabled;
+    private boolean mLoggingEnabled = true;

     // Timeout after which we remove the effects any user interactions might've had on the
     // brightness mapping. This timeout doesn't start until we transition to a non-interactive
@@ -920,6 +920,7 @@ class AutomaticBrightnessController {
             if (mLightSensorEnabled) {
                 final long time = SystemClock.uptimeMillis();
                 final float lux = event.values[0];
+               Slog.d(TAG, "zengjf SensorEventListener lux: " + lux);
                 handleLightSensorEvent(time, lux);
             }
         }
diff --git a/frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java b/frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java
index 171cc5abdb9..02f52d99855 100644
--- a/frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java
+++ b/frameworks/base/services/core/java/com/android/server/display/BrightnessMappingStrategy.java
@@ -82,9 +82,13 @@ public abstract class BrightnessMappingStrategy {
             }
             BrightnessConfiguration.Builder builder = new BrightnessConfiguration.Builder(
                     luxLevels, brightnessLevelsNits);
+            Slog.w(TAG, "PhysicalMappingStrategy");
             return new PhysicalMappingStrategy(builder.build(), nitsRange, backlightRange,
                     autoBrightnessAdjustmentMaxGamma);
         } else if (isValidMapping(luxLevels, brightnessLevelsBacklight)) {
+            Slog.w(TAG, "SimpleMappingStrategy");
+            Slog.w(TAG, "luxLevels: " + Arrays.toString(luxLevels));
+            Slog.w(TAG, "brightnessLevelsBacklight: " + Arrays.toString(brightnessLevelsBacklight));
             return new SimpleMappingStrategy(luxLevels, brightnessLevelsBacklight,
                     autoBrightnessAdjustmentMaxGamma);
         } else {
```


# 背光

* /sys/devices/platform/leds-mt65xx/leds/lcd-backlight
* cat max_brightness
  ```
  255
  ```
* echo 128 > brightness
* cat brightness
* 使用手机手电筒照着光感传感器，经过一定时间，能过达到255的亮度等级
* 通过settings调节背光发现百分比不是线性百分比：
  * adb shell settings put system screen_brightness 130
  * 130的时候亮度达到了85%
  * 参考文档
    * [Android 9.0 (P版本) 亮度进度条变化等级更新](https://blog.csdn.net/su749520/article/details/84585672?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromMachineLearnPai2-1.channel_param)
    * 新的关系由 GAMMA_SPACE_MAX、经过 convertGammaToLinear 和 convertLinearToGamma 共同决定
    * [android P 亮度调解修改为线性变化](https://blog.csdn.net/wangjicong_215/article/details/103066698)
    * [MTK 平台 CABC 背光控制机制](https://blog.csdn.net/sinat_30545941/article/details/72874775)
* adb shell
  * cd /sdcard/debuglogger/mobilelog
  * grep updateAutoBrightness * -R
  * grep calculateAmbientLux * -R
  * grep newScreenAutoBrightness * -R


# 调光时间


* [Android 8.1 DisplayPowerController(四) 自动调节亮度(1)——流程](https://blog.csdn.net/FightFightFight/article/details/83626332)

创建自动调光对象

`frameworks/base/services/core/java/com/android/server/display/DisplayPowerController.java`
```java
public DisplayPowerController(Context context,
            DisplayPowerCallbacks callbacks, Handler handler,
            SensorManager sensorManager, DisplayBlanker blanker) {
    // ...省略

    long brighteningLightDebounce = resources.getInteger(
            com.android.internal.R.integer.config_autoBrightnessBrighteningLightDebounce);
    long darkeningLightDebounce = resources.getInteger(
            com.android.internal.R.integer.config_autoBrightnessDarkeningLightDebounce);

    // ...省略

    mBrightnessMapper = BrightnessMappingStrategy.create(resources);
    if (mBrightnessMapper != null) {
        mAutomaticBrightnessController = new AutomaticBrightnessController(this,
                handler.getLooper(), sensorManager, lightSensor, mBrightnessMapper,
                lightSensorWarmUpTimeConfig, mScreenBrightnessRangeMinimum,
                mScreenBrightnessRangeMaximum, dozeScaleFactor, lightSensorRate,
                initialLightSensorRate, brighteningLightDebounce, darkeningLightDebounce,
                autoBrightnessResetAmbientLuxAfterWarmUp, ambientBrightnessThresholds,
                screenBrightnessThresholds, shortTermModelTimeout,
                context.getPackageManager());
    } else {
        mUseSoftwareAutoBrightnessConfig = false;
    }

    // ...省略
}
```

查看调光延时实际配置

`frameworks/base/core/res/res/values/config.xml`
```xml
    <!-- Stability requirements in milliseconds for accepting a new brightness level.  This is used
         for debouncing the light sensor.  Different constants are used to debounce the light sensor
         when adapting to brighter or darker environments.  This parameter controls how quickly
         brightness changes occur in response to an observed change in light level that exceeds the
         hysteresis threshold. -->
    <integer name="config_autoBrightnessBrighteningLightDebounce">4000</integer>
    <integer name="config_autoBrightnessDarkeningLightDebounce">8000</integer>
```

[Android 9.0 自动背光机制分析](https://blog.csdn.net/FightFightFight/article/details/85797336)

lux亮度等级映射调节

`frameworks/base/core/res/res/values/config.xml`
```xml
    <!-- Array of light sensor lux values to define our levels for auto backlight brightness support.
         The N entries of this array define N + 1 control points as follows:
         (1-based arrays)

         Point 1:            (0, value[1]):             lux <= 0
         Point 2:     (level[1], value[2]):  0        < lux <= level[1]
         Point 3:     (level[2], value[3]):  level[2] < lux <= level[3]
         ...
         Point N+1: (level[N], value[N+1]):  level[N] < lux

         The control points must be strictly increasing.  Each control point
         corresponds to an entry in the brightness backlight values arrays.
         For example, if lux == level[1] (first element of the levels array)
         then the brightness will be determined by value[2] (second element
         of the brightness values array).

         Spline interpolation is used to determine the auto-brightness
         backlight values for lux levels between these control points.

         Must be overridden in platform specific overlays -->
    <integer-array name="config_autoBrightnessLevels">
    </integer-array>
```

上面文件修改无效，MTK存放的文件是该文件`mediatek/proprietary/packages/overlay/vendor/FrameworkResOverlay/brightness_adaptive_support/res/values/config.xml`


# 传感器数据

```
* frameworks/base/services/core/java/com/android/server/display/DisplayPowerController.java
  └── public DisplayPowerController(Context context, DisplayPowerCallbacks callbacks, Handler handler, SensorManager sensorManager, DisplayBlanker blanker)
      ├── String lightSensorType = resources.getString(com.android.internal.R.string.config_displayLightSensorType);
      ├── Sensor lightSensor = findDisplayLightSensor(lightSensorType);
      └── mAutomaticBrightnessController = new AutomaticBrightnessController(this, handler.getLooper(), sensorManager, lightSensor, mBrightnessMapper, lightSensorWarmUpTimeConfig, mScreenBrightnessRangeMinimum, mScreenBrightnessRangeMaximum, dozeScaleFactor, lightSensorRate, initialLightSensorRate, brighteningLightDebounce, darkeningLightDebounce, autoBrightnessResetAmbientLuxAfterWarmUp, ambientBrightnessThresholds, screenBrightnessThresholds, shortTermModelTimeout, context.getPackageManager());
          └── frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
              ├── mLightSensor = lightSensor;
              └── private boolean setLightSensorEnabled(boolean enable)
                  └── mSensorManager.registerListener(mLightSensorListener, mLightSensor, mCurrentLightSensorRate * 1000, mHandler);
                      └── private final SensorEventListener mLightSensorListener = new SensorEventListener()
                          └── public void onSensorChanged(SensorEvent event) 
                              └── final float lux = event.values[0];
                                  └── handleLightSensorEvent(time, lux);
                                      └── updateAmbientLux(time);
```

# 自动调光多次强制最大

```
* frameworks/base/services/core/java/com/android/server/display/AutomaticBrightnessController.java
  └── private void updateAmbientLux(long time)
      ├── long nextBrightenTransition = nextAmbientLightBrighteningTransition(time);
      └── long nextDarkenTransition = nextAmbientLightDarkeningTransition(time);
          └── mAmbientLightRingBuffer.getLux(i) <= mAmbientBrighteningThreshold
              └── mAmbientBrighteningThreshold
                  └── private void setAmbientLux(float lux)
                      └── mAmbientBrighteningThreshold = mAmbientBrightnessThresholds.getBrighteningThreshold(lux);
                          └── frameworks/base/services/core/java/com/android/server/display/HysteresisLevels.java
                              └── float darkConstant = getReferenceLevel(value, mDarkeningThresholds);
                                  └── float darkThreshold = value * (1.0f - darkConstant);
```
