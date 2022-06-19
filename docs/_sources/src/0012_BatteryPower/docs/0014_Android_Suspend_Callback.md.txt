# Android Suspend Callback

Android系统是如何被唤醒的

# 参考文档

* [0013_Android_Suspend.md](0013_Android_Suspend.md)

# Suspend Callback

* BatteryStatsService通过binder注册回调函数到suspend进程；
* 在系统写入mem到/sys/power/state，如果能够进入休眠，此时系统会卡住，等这个函数返回的时候就是唤醒了；
* 内核系统唤醒了，会继续执行后续处理函数，也就是调用notify wakeup了，BatteryStatsService注册的回调函数就被处理；
* 从上面处理流程可知，比较难知道系统什么时候休眠，因为也存在写入了mem后，休不下去了，就是suspend abort；

```
* frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
  * static jint nativeWaitWakeup(JNIEnv *env, jobject clazz, jobject outBuf)
    * suspendControl->registerCallback(new WakeupCallback(), &isRegistered);
      * frameworks/base/services/core/jni/com_android_server_am_BatteryStatsService.cpp
        * class WakeupCallback : public BnSuspendCallback
          * binder::Status notifyWakeup(bool success, const std::vector<std::string>& wakeupReasons) override
            * ALOGI("In wakeup_callback: %s", success ? "resumed from suspend" : "suspend aborted");
      * system/hardware/interfaces/suspend/1.0/default/SuspendControlService.cpp
        * binder::Status SuspendControlService::registerCallback(const sp<ISuspendCallback>& callback, bool* _aidl_return)
          * sp<IBinder> cb = IInterface::asBinder(callback);
          * mCallbacks.push_back(callback);
* system/hardware/interfaces/suspend/1.0/default/SystemSuspend.cpp
  * void SystemSuspend::initAutosuspend()
    * bool success = WriteStringToFd(kSleepState, mStateFd);
    * mControlService->notifyWakeup(success);
      * system/hardware/interfaces/suspend/1.0/default/SuspendControlService.cpp
        * auto callbacksCopy = mCallbacks;
        * for (const auto& callback : callbacksCopy)
          * callback->notifyWakeup(success).isOk();
```

# 唤醒时的log

```
BatteryStatsService: In wakeup_callback: resumed from suspend
```
