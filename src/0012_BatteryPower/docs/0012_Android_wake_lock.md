# Android wake lock

测试软件自动关屏，adb查看测试软件wake lock，查看是否有额外的进程持锁，adb的USB是正常的，忽略

# 参考文档

* [0005_Android_Low_Power.md](0005_Android_Low_Power.md)
* [[FAQ07421] [lowpower]AP suspend异常debug及log分析](https://online.mediatek.com/FAQ#/SW/FAQ07421)
* [Keep the CPU on](https://developer.android.com/training/scheduling/wakelock#java)
* [PowerManager.WakeLock](https://developer.android.com/reference/android/os/PowerManager.WakeLock)

# 尝试查看

* adb shell
* cat /sys/kernel/debug/wakeup_sources | sed -e 's/"^ "/"unnamed"/g' | awk '{print $6 "\t" $1}' | grep -v "^0" | sort -n
  ```
  active_since    name
  451487  PowerManagerService.WakeLocks
  461121  ws_charge
  ```
* dumpsys power | grep "PARTIAL_WAKE_LOCK"
  ```
    PARTIAL_WAKE_LOCK              'ZZZBatteryManagerService' ACQ=-7m57s516ms LONG (uid=1000 pid=1005)
  ```

# 实战查看

* adb shell
* cat /sys/kernel/debug/wakeup_sources | sed -e 's/"^ "/"unnamed"/g' | awk '{print $6 "\t" $1}' | grep -v "^0" | sort -n
g' | awk '{print $6 "\t" $1}' | grep -v "^0" | sort -n
  ```
  active_since    name
  195     WLAN
  216583  PowerManagerService.WakeLocks
  342052  ws_charge
  ```
* dumpsys power | grep "PARTIAL_WAKE_LOCK"
  ```
    PARTIAL_WAKE_LOCK              'ICC WackLock' ACQUIRE_CAUSES_WAKEUP ON_AFTER_RELEASE ACQ=-4m10s769ms LONG (uid=1000 pid=1748)
  ```
  * ICC进程占有wake lock，导致系统无法休眠

# 代码中怎么处理WakeLock

```Java
// packages/ZZZManager/src/com/zzz/daemon/observer/ServerService.java

public void onCreate() {
    super.onCreate();
    ZZZLog.w(TAG,"onCreate");
    isrun = true;
    mTaskHandler = new TaskHandler(); // Handler
    /* 获取powermanager服务 */
    PowerManager powerMg = (PowerManager) getSystemService(Context.POWER_SERVICE);
    // PowerManager.ACQUIRE_CAUSES_WAKEUP是唤醒屏幕的一个参数
    mWakeLock = powerMg.newWakeLock(PowerManager.FULL_WAKE_LOCK
            | PowerManager.ACQUIRE_CAUSES_WAKEUP
            | PowerManager.ON_AFTER_RELEASE, "PED WackLock");

    mIccWakeLock = powerMg.newWakeLock(PowerManager.PARTIAL_WAKE_LOCK
            | PowerManager.ACQUIRE_CAUSES_WAKEUP
            | PowerManager.ON_AFTER_RELEASE,"ICC WackLock");

    notifyMg = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

    // ...省略
}

/************
 * 插卡状态通知
 */
private void smartCardNotify(){
    if(getCurrentSmartCardStatus()==SMART_CARD_INSERTION){
        // ...省略

        if ((mIccWakeLock != null) && (!mIccWakeLock.isHeld())) {
            ZZZLog.v(TAG, "acquire wakelock");
            try {
                mIccWakeLock.acquire();
            } catch (Throwable th) {
            }
        } else {
            // should never happen during normal workflow
            ZZZLog.d(TAG, "The sp reported event may be abnormal,so do not acquire wakeLock!");
        }
        isIccRemove = false;
    }else if(getCurrentSmartCardStatus()==SMART_CARD_REMOVEL){
        // ...省略

        if (mIccWakeLock != null && mIccWakeLock.isHeld()) {
            ZZZLog.v(TAG, "Releasing wakelock");
            try {
                mIccWakeLock.release();
            } catch (Throwable th) {
                // ignoring this exception, probably wakeLock was already released
            }
        } else {
            // should never happen during normal workflow
            ZZZLog.d(TAG, "The sp reported event may be abnormal,so do not release wakeLock!");
        }
    }
}

@Override
public void onDestroy() {
    // ...省略

    if (mIccWakeLock != null && mIccWakeLock.isHeld()) {
        ZZZLog.v(TAG, "Releasing wakelock");
        try {
            mIccWakeLock.release();
        } catch (Throwable th) {
            // ignoring this exception, probably wakeLock was already released
        }
    } else {
        // should never happen during normal workflow
    }
}
```
