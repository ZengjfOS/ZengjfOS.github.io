# Android Wakeup Reason

Android层如何获取唤醒原因，最终读取内核提供的文件节点获取信息

# 参考文档

* [0013_Android_Suspend.md](0013_Android_Suspend.md)
* [0014_Android_Suspend_Callback.md](0014_Android_Suspend_Callback.md)


# Android获取Wakeup Reason

```CPP
// frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp

#define LAST_RESUME_REASON "/sys/kernel/wakeup_reasons/last_resume_reason"

// ...省略

class WakeupCallback : public BnSuspendCallback {
   public:
    binder::Status notifyWakeup(bool success) override {
        ALOGI("In wakeup_callback: %s", success ? "resumed from suspend" : "suspend aborted");
        int ret = sem_post(&wakeup_sem);
        if (ret < 0) {
            char buf[80];
            strerror_r(errno, buf, sizeof(buf));
            ALOGE("Error posting wakeup sem: %s\n", buf);
        }
        return binder::Status::ok();
    }
};

static jint nativeWaitWakeup(JNIEnv *env, jobject clazz, jobject outBuf)
{
    // ...省略

    // Wait for wakeup.
    ALOGV("Waiting for wakeup...");
    // TODO(b/116747600): device can suspend and wakeup after sem_wait() finishes and before wakeup
    // reason is recorded, i.e. BatteryStats might occasionally miss wakeup events.
    int ret = sem_wait(&wakeup_sem);
    if (ret < 0) {
        char buf[80];
        strerror_r(errno, buf, sizeof(buf));
        ALOGE("Error waiting on semaphore: %s\n", buf);
        // Return 0 here to let it continue looping but not return results.
        return 0;
    }

    FILE *fp = fopen(LAST_RESUME_REASON, "r");
    if (fp == NULL) {
        ALOGE("Failed to open %s", LAST_RESUME_REASON);
        return -1;
    }

    // ...省略
}
```

nativeWaitWakeup调用关系如下所示，理解BatteryStats为什么可以显示唤醒源

```
* frameworks/base/services/java/com/android/server/SystemServer.java
  * private void startBootstrapServices(@NonNull TimingsTraceAndSlog t)
    * mActivityManagerService.initPowerManagement();
      * frameworks/base/services/core/java/com/android/server/am/ActivityManagerService.java
        * public void initPowerManagement()
          * mBatteryStatsService.initPowerManagement();
            * frameworks/base/services/core/java/com/android/server/am/BatteryStatsService.java
              * public void initPowerManagement()
                * (new WakeupReasonThread()).start();
                  * final class WakeupReasonThread extends Thread
                    * public void run()
                      * while ((reason = waitWakeup()) != null)
                        * private String waitWakeup()
                          * int bytesWritten = nativeWaitWakeup(mUtf8Buffer);
                            * frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
                              * class WakeupCallback : public BnSuspendCallback
                                * binder::Status notifyWakeup(bool success) override
                                  * int ret = sem_post(&wakeup_sem);
                              * static jint nativeWaitWakeup(JNIEnv *env, jobject clazz, jobject outBuf)
                                * ALOGV("Waiting for wakeup...");
                                * int ret = sem_wait(&wakeup_sem);
                                * FILE *fp = fopen(LAST_RESUME_REASON, "r");
                                  * #define LAST_RESUME_REASON "/sys/kernel/wakeup_reasons/last_resume_reason"
                                * while (fgets(reasonline, sizeof(reasonline), fp) != NULL)
                        * mStats.noteWakeupReasonLocked(reason, SystemClock.elapsedRealtime(), SystemClock.uptimeMillis());
                          * frameworks/base/core/java/com/android/internal/os/BatteryStatsImpl.java
                            * public void noteWakeupReasonLocked(String reason, long elapsedRealtimeMs, long uptimeMs)
                              * if (DEBUG_HISTORY) Slog.v(TAG, "Wakeup reason \"" + reason +"\": " + Integer.toHexString(mHistoryCur.states));
                                * 想要通过logcat查看原因，可以打开这个调试开关
```

# adb shell

* cat /sys/kernel/wakeup_reasons/last_resume_reason
  ```
  26 type_c_port0-IRQ
  177 SPM
  ```

# show wakeup reason

打开隐藏log

```diff
diff --git a/frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp b/frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
index b08868e2c7f..be9df8b1663 100644
--- a/frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
+++ b/frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
@@ -15,7 +15,7 @@
  */

 #define LOG_TAG "BatteryStatsService"
-//#define LOG_NDEBUG 0
+#define LOG_NDEBUG 0

 #include <climits>
 #include <errno.h>
@@ -233,6 +233,7 @@ static jint nativeWaitWakeup(JNIEnv *env, jobject clazz, jobject outBuf)
         i++;
     }

+    ALOGV("reasons: %s", reasonline);
     ALOGV("Got %d reasons", i);
     if (i > 0) {
         *mergedreasonpos = 0;
```

logcat输出信息

```
I BatteryStatsService: In wakeup_callback: resumed from suspend
V BatteryStatsService: Reading wakeup reasons
D BatteryService: healthInfoChanged_2_1 props={.legacy = {.legacy = {.chargerAcOnline = false, .chargerUsbOnline = false, .chargerWirelessOnline = false, .maxChargingCurrent = 0, .maxChargingVoltage = 0, .batteryStatus = DISCHARGING, .batteryHealth = GOOD, .batteryPresent = true, .batteryLevel = 99, .batteryVoltage = 4282, .batteryTemperature = 298, .batteryCurrent = -278400, .batteryCycleCount = 1, .batteryFullCharge = 3013000, .batteryChargeCounter = 2982870, .batteryTechnology = Li-ion, .chargerVoltage = 0, .chargerCurrent = 0, .batteryStateOfHealth = 100, .batteryManufactuer = M50-Icon-Energy, .batterySerialNumber = IBS012NA-202021004029}, .batteryCurrentAverage = -278400, .diskStats = [], .storageInfos = []}, .batteryCapacityLevel = HIGH, .batteryChargeTimeToFullNowSeconds = 498, .batteryFullChargeDesignCapacityUah = 301000}
V BatteryStatsService: reasons: 332 mt6397-rtc
V BatteryStatsService: Got 2 reasons
```

也可通过下面这个开关输出Wakeup reason

```
* frameworks/base/core/java/com/android/internal/os/BatteryStatsImpl.java
  * public class BatteryStatsImpl extends BatteryStats
    * private static final boolean DEBUG_HISTORY = false;
  * public void noteWakeupReasonLocked(String reason, long elapsedRealtimeMs, long uptimeMs)
    * if (DEBUG_HISTORY) Slog.v(TAG, "Wakeup reason \"" + reason +"\": " + Integer.toHexString(mHistoryCur.states));
```
