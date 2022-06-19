# Android SystemUI Battery

分析SystemUI Battery电量变化的原理

## 参考文档

* [Android8.1 SystemUI源码分析之 电池时钟刷新](https://www.cnblogs.com/cczheng-666/p/10958920.html)
* [电源 | Battery系列(一) BatteryService分析](https://www.jianshu.com/p/041cbdc9edfe)
* [Android Healthd电池服务分析](https://www.cnblogs.com/linhaostudy/p/12002068.html)
* [Android10.0电源框架源码分析](http://www.cjcbill.com/2020/03/01/battery-frame/)

## SystemUI

* 监听ACTION_BATTERY_CHANGED广播
* 收到广播后会更新图标；

```
* frameworks/base/packages/SystemUI/src/com/android/systemui/statusbar/policy/BatteryControllerImpl.java
  * public void init()
    * registerReceiver();
      * IntentFilter filter = new IntentFilter();
        * filter.addAction(Intent.ACTION_BATTERY_CHANGED);
        * filter.addAction(PowerManager.ACTION_POWER_SAVE_MODE_CHANGED);
        * filter.addAction(ACTION_LEVEL_TEST);
        * mBroadcastDispatcher.registerReceiver(this, filter);
  * public void onReceive(final Context context, Intent intent)
    * if (action.equals(Intent.ACTION_BATTERY_CHANGED))
      * fireBatteryLevelChanged();
        * for (int i = 0; i < N; i++)
          * mChangeCallbacks.get(i).onBatteryLevelChanged(mLevel, mPluggedIn, mCharging);
            * frameworks/base/packages/SystemUI/src/com/android/systemui/BatteryMeterView.java
              * public void onBatteryLevelChanged(int level, boolean pluggedIn, boolean charging)
                * mDrawable.setCharging(pluggedIn);
                * mDrawable.setBatteryLevel(level);
                * mCharging = pluggedIn;
                * mLevel = level;
                * updatePercentText();
```

## BatteryService

* 向Health注册IHealthInfoCallback Binder回调函数；
* 当Health监听到电池变化的时候，会通过IHealthInfoCallback运行到BatteryService进程，最终发ACTION_BATTERY_CHANGED广播出去；

```
* frameworks/base/services/core/java/com/android/server/BatteryService.java
  * public void onStart()
    * registerHealthCallback();
      * mHealthHalCallback = new HealthHalCallback();
        * private final class HealthHalCallback extends IHealthInfoCallback.Stub implements HealthServiceWrapper.Callback
          * public void healthInfoChanged(android.hardware.health.V2_0.HealthInfo props)
            * BatteryService.this.update(propsLatest);
              * private void update(android.hardware.health.V2_1.HealthInfo info)
                * processValuesLocked(false);
                  * sendBatteryChangedIntentLocked();
                    * final Intent intent = new Intent(Intent.ACTION_BATTERY_CHANGED);
                    * mHandler.post(() -> ActivityManager.broadcastStickyIntent(intent, UserHandle.USER_ALL));
      * mHealthServiceWrapper.init(mHealthHalCallback, new HealthServiceWrapper.IServiceManagerSupplier() {}, new HealthServiceWrapper.IHealthSupplier() {});
        * void init(@Nullable Callback callback, IServiceManagerSupplier managerSupplier, IHealthSupplier healthSupplier)
          * if (callback != null)
            * mCallback = callback;
            * mCallback.onRegistration(null, newService, mInstanceName);
              * private final class HealthHalCallback extends IHealthInfoCallback.Stub implements HealthServiceWrapper.Callback
                * public void onRegistration(IHealth oldService, IHealth newService, String instance)
                  * int r = newService.registerCallback(this);
                  * newService.update();
```

## 低电量

在BatteryService启动的时候会监听低电量属性，从而可以及时发送低电量问题

```
* frameworks/base/services/core/java/com/android/server/BatteryService.java
  * public void onBootPhase(int phase)
    * ContentObserver obs = new ContentObserver(mHandler)
      * public void onChange(boolean selfChange)
        * updateBatteryWarningLevelLocked();
    * final ContentResolver resolver = mContext.getContentResolver();
    * resolver.registerContentObserver(Settings.Global.getUriFor(Settings.Global.LOW_POWER_MODE_TRIGGER_LEVEL), false, obs, UserHandle.USER_ALL);
    * updateBatteryWarningLevelLocked();
```

## Healthd如何调用到BatteryService

* [Android10.0电源框架源码分析](http://www.cjcbill.com/2020/03/01/battery-frame/)
* 在以往的Android平台中，该服务名为Healthd,Android 10.0使用了"android.hardware.health@2.0-service"来代替了服务Healthd。但后续为了方便分析，还是将android.hardware.health@2.0-service简称为healthd；
* system/core/healthd/

```
* system/core/healthd/HealthServiceDefault.cpp
  * int main()
    * return health_service_main();
      * hardware/interfaces/health/2.0/utils/libhealthservice/HealthServiceCommon.cpp
        * int health_service_main(const char* instance)
          * healthd_mode_ops = &healthd_mode_service_2_0_ops;
            * static struct healthd_mode_ops healthd_mode_service_2_0_ops
              * .battery_update = healthd_mode_service_2_0_battery_update,
                * void healthd_mode_service_2_0_battery_update(struct android::BatteryProperties* prop)
                  * convertToHealthInfo(prop, info.legacy);
                  * Health::getImplementation()->notifyListeners(&info);
                    * hardware/interfaces/health/2.0/default/Health.cpp
                      * void Health::notifyListeners(HealthInfo* healthInfo)
                        * for (auto it = callbacks_.begin(); it != callbacks_.end();)
                          * auto ret = (*it)->healthInfoChanged(*healthInfo);
                            * 这里调用到了BatteryService注册的回调函数中
          * return healthd_main();
            * hardware/interfaces/health/2.0/default/healthd_common_adapter.cpp
              * int healthd_main()
                * health_loop = std::make_unique<HealthLoopAdapter>();
                * int ret = health_loop->StartLoop();
                  * hardware/interfaces/health/utils/libhealthloop/HealthLoop.cpp
                    * int HealthLoop::StartLoop()
                      * ret = InitInternal();
                        * Init(&healthd_config_);
                        * WakeAlarmInit();
                          * wakealarm_fd_.reset(timerfd_create(CLOCK_BOOTTIME_ALARM, TFD_NONBLOCK));
                            * CLOCK_BOOTTIME_ALARM
                              * This clock is like CLOCK_BOOTTIME, but will wake the system if it is suspended. The caller must have the CAP_WAKE_ALARM capability in order to set a timer against this clock.
                          * if (RegisterEvent(wakealarm_fd_, &HealthLoop::WakeAlarmEvent, EVENT_WAKEUP_FD))
                            * int HealthLoop::RegisterEvent(int fd, BoundFunction func, EventWakeup wakeup)
                              * auto* event_handler = event_handlers_.emplace_back(std::make_unique<EventHandler>(EventHandler{this, fd, func})).get();
                              * ev.data.ptr = reinterpret_cast<void*>(event_handler);
                              * epoll_ctl(epollfd_, EPOLL_CTL_ADD, fd, &ev)
                          * WakeAlarmSetInterval(healthd_config_.periodic_chores_interval_fast);
                            * hardware/interfaces/health/utils/libhealthloop/utils.cpp
                              * void InitHealthdConfig(struct healthd_config* healthd_config)
                                * *healthd_config
                                  * .periodic_chores_interval_fast = DEFAULT_PERIODIC_CHORES_INTERVAL_FAST,
                                    * #define DEFAULT_PERIODIC_CHORES_INTERVAL_FAST (60 * 1)
                                      * Periodic chores fast interval in seconds
                            * 现在知道为什么有Alarm唤醒了
                        * UeventInit();
                      * MainLoop();
                        * while (1)
                          * nevents = epoll_wait(epollfd_, events, eventct, timeout);
                          * for (int n = 0; n < nevents; ++n)
                            * if (events[n].data.ptr)
                              * auto* event_handler = reinterpret_cast<EventHandler*>(events[n].data.ptr);
                              * event_handler->func(event_handler->object, events[n].events);
                                * void HealthLoop::WakeAlarmEvent(uint32_t /*epevents*/)
                                  * PeriodicChores();
                                    * ScheduleBatteryUpdate();
                                      * hardware/interfaces/health/2.0/default/healthd_common_adapter.cpp
                                        * void ScheduleBatteryUpdate() override { Health::getImplementation()->update(); }
                                          * hardware/interfaces/health/2.0/default/Health.cpp
                                            * Return<Result> Health::update()
                                              * battery_monitor_->updateValues();
                                              * const HealthInfo_1_0& health_info = battery_monitor_->getHealthInfo_1_0();
                                              * convertFromHealthInfo(health_info, &props);
                                              * healthd_mode_ops->battery_update(&props);
                                                * hardware/interfaces/health/2.0/utils/libhealthservice/HealthServiceCommon.cpp
                                                  * static struct healthd_mode_ops healthd_mode_service_2_0_ops
                                                    * .battery_update = healthd_mode_service_2_0_battery_update,
                                                      * void healthd_mode_service_2_0_battery_update(struct android::BatteryProperties* prop)
                                                        * convertToHealthInfo(prop, info.legacy);
                                                        * Health::getImplementation()->notifyListeners(&info);
                                                          * hardware/interfaces/health/2.0/default/Health.cpp
                                                            * void Health::notifyListeners(HealthInfo* healthInfo)
                                                              * for (auto it = callbacks_.begin(); it != callbacks_.end();)
                                                                * auto ret = (*it)->healthInfoChanged(*healthInfo);
                                                                  * 这里调用到了BatteryService注册的回调函数中
```

## Alarm唤醒周期

从下面唤醒周期来看分两种：

* 1分钟唤醒一次叫FAST；
* 10分钟唤醒一次叫SLOW；

```CPP
// hardware/interfaces/health/utils/libhealthloop/utils.cpp

// Periodic chores fast interval in seconds
#define DEFAULT_PERIODIC_CHORES_INTERVAL_FAST (60 * 1)
// Periodic chores fast interval in seconds
#define DEFAULT_PERIODIC_CHORES_INTERVAL_SLOW (60 * 10)

void InitHealthdConfig(struct healthd_config* healthd_config) {
    *healthd_config = {
            .periodic_chores_interval_fast = DEFAULT_PERIODIC_CHORES_INTERVAL_FAST,
            .periodic_chores_interval_slow = DEFAULT_PERIODIC_CHORES_INTERVAL_SLOW,
            .energyCounter = NULL,
            .boot_min_cap = 0,
            .screen_on = NULL,
    };
}
```
