# Android Suspend

Android输入休眠模式到`/sys/power/state`让机器进入深度休眠

# 参考文档

* [Suspend to RAM和Suspend to Idle分析，以及在HiKey上性能对比](https://www.cnblogs.com/arnoldlu/p/6253665.html)
* [Suspend to Idle](https://www.linaro.org/blog/suspend-to-idle/)

# adb shell to freeze

* cat /sys/power/state
  ```
  freeze mem
  ```
* echo freeze > /sys/power/state
  ```
  [63980.172031] (5)[17549:sh]PM: suspend entry (s2idle)
  [63980.172074] (5)[17549:sh]PM: Syncing filesystems ... done.
  [63980.278444] (5)[17549:sh]vcodec_suspend_notifier ok action = 3
  [63980.278469] (5)[17549:sh]rtc_pm_event = 3
  [63980.278564] (5)[17549:sh][name:spm&][SPM] PM: suspend entry 2021-08-31 05:35:15.722221178 UTC
  [63980.278584] (5)[17549:sh][xxxxEEM] Start EEM suspend
  [63980.278900] (5)[17549:sh]charger_pm_event: enter PM_SUSPEND_PREPARE
  [63980.278951] (5)[17549:sh][name:spm&][SPM] PM: suspend entry 2021-08-31 05:35:15.722612947 UTC
  [63980.278975] (5)[17549:sh][MTK-BT]bt_pm_notifier_callback: bt_pm_notifier_callback: btonflag[1], event[3]
  [63980.279051] (5)[17549:sh][MTK-BT]bt_read_cr: HOST_MAILBOX_BT_ADDR[0x18007124], read[0x00000000]
  [63980.279117] (4)[17549:sh]Freezing user space processes ... (elapsed 0.011 seconds) done.
  [63980.291134] (4)[17549:sh]OOM killer disabled.
  [63980.291152] (4)[17549:sh]Freezing remaining freezable tasks ... (elapsed 0.005 seconds) done.
  [63980.296316] (4)[17549:sh][name:spm&]NO spm_get_is_cpu_pdn !!!
  [63980.296328] (4)[17549:sh][name:spm&]NO spm_get_is_infra_pdn !!!
  [63980.296339] (4)[17549:sh][name:spm&][SLP] @@@@@@@@@@@@\x09Chip_pm_begin(0)(0)\x09@@@@@@@@@@@@@
  [63980.299365] -(4)[17549:sh][MUSB]musb_hub_control 355: port status 00000100,devctl=0x99
  [63980.299549] (4)[17549:sh][wlan][17549]mtk_cfg_suspend:(REQ WARN) driver is not ready
  [63980.299794] (4)[17549:sh][HPS] hps_suspend
  [63980.299809] (4)[17549:sh][HPS] state:2,enabled:1,suspend_enabled:1,rush_boost_enabled:1,ret:0
  [63980.299913] (4)[17549:sh]******** mtk_battery_suspend!! iavg=0 ***GM3 disable:0 0 0 0 tmp_intr:0***
  [63980.317627] (4)[17549:sh][msdc]msdc power off
  [63980.329798] (4)[17549:sh]mt6370_i2c_suspend WAIT HRESET DONE(0) - SUSPEND
  [63980.330084] (4)[17549:sh][ALS/PS] ltr559_i2c_suspend
  [63980.331063] (4)[17549:sh][ALS/PS] ALS(1): disable als only
  [63980.341618] (4)[17549:sh][ALS/PS] ltr559_ps_enable() ...start!
  [63980.342183] (4)[17549:sh][ALS/PS] PS: disable ps only
  [63980.353026] (4)[17549:sh][Gsensor] sc7a20_suspend
  [63980.353039] (4)[17549:sh][Gsensor] SC7A20_SetPowerMode
  [63980.354637] (4)[17549:sh][mt_udi] UDI suspend
  [63980.355035] (4)[17549:sh]dpm_run_callback(): platform_pm_suspend+0x0/0x60 returns -16
  [63980.355058] (4)[17549:sh]PM: Device alarmtimer failed to suspend: error -16
  [63980.355077] (4)[17549:sh]suspend of devices aborted after 55.932 msecs
  [63980.355090] (4)[17549:sh]PM: Some devices failed to suspend, or early wake event detected
  [63980.355336] (4)[17549:sh][mt_udi] UDI resume
  [63980.356165] (4)[17549:sh][Gsensor] sc7a20_resume
  [63980.356178] (4)[17549:sh][Gsensor] SC7A20_Init
  [63980.356189] (4)[17549:sh][Gsensor] SC7A20_CheckDeviceID
  [63980.356634] (4)[17549:sh]SC7A20_CheckDeviceID 17 pass!\x0a
  [63980.356885] (4)[17549:sh][Gsensor] SC7A20_SetPowerMode
  [63980.359481] (4)[17549:sh][ALS/PS] ltr559_i2c_resume
  [63980.360226] -(4)[17549:sh]mt635x_auxadc_read_raw: 16 callbacks suppressed
  [63980.360245] (4)[17549:sh]mt635x-auxadc mt635x-auxadc: name:IMIX_R, channel=0, adc_out=0xb9, adc_result=185
  [63980.360263] (4)[17549:sh][dlpt] imix_r=185
  [63980.360314] (4)[17549:sh]******** mtk_battery_resume!! iavg=0 ***GM3 disable:0 0 0 0***
  [63980.360338] (4)[17549:sh][fg_update_sw_iavg]diff time:2
  [63980.360508] (4)[17549:sh][HPS] hps_resume
  [63980.360523] (4)[17549:sh][HPS] state: 1, enabled: 1, suspend_enabled: 1, rush_boost_enabled: 1
  [63980.360716] (4)[17549:sh][wlan][17549]mtk_cfg_resume:(REQ WARN) driver is not ready
  [63980.360827] -(4)[17549:sh][MUSB]musb_hub_control 355: port status 00000100,devctl=0x99
  [63980.360930] (4)[17549:sh]resume of devices complete after 5.823 msecs
  [63980.363549] (4)[17549:sh]OOM killer enabled.
  [63980.363563] (6)[3191:Binder:418_2]Restarting tasks ...
  [63980.365265] (6)[3191:Binder:418_2]active wakeup source: alarmtimer
  [63980.365288] (6)[3191:Binder:418_2]active wakeup source: USB suspend lock
  [63980.371121] done.
  [63980.371146] (4)[17549:sh][CMDQ]cmdq_core_resume_notifier
  [63980.371155] (4)[17549:sh][cmdq] mdp buffer pool already created
  [63980.371673] (4)[17549:sh]mt635x-auxadc mt635x-auxadc: name:VCORE_TEMP, channel=4, adc_out=0x60a, adc_result=679
  [63980.371718] (4)[17549:sh][Thermal/TZ/PMIC] [tsbuck1_raw_to_temp] 679, 392833, 1000000, -1863
  [63980.371745] (4)[17549:sh][Thermal/TZ/PMIC] [tsbuck1_raw_to_temp] t_current=28368
  [63980.371776] (4)[17549:sh][Thermal/TZ/PMIC] mt6357tsbuck1_get_hw_temp raw=679 T=28368
  [63980.371801] (4)[17549:sh][Thermal/TZ/PMIC] mt6357tsbuck1_get_hw_temp pre_tsbuck1_temp1=28368
  [63980.372244] (4)[17549:sh]mt635x-auxadc mt635x-auxadc: name:VPROC_TEMP, channel=4, adc_out=0x602, adc_result=675
  [63980.372279] (4)[17549:sh][Thermal/TZ/PMIC] [tsbuck2_raw_to_temp] 675, 392296, 1000000, -1863
  [63980.372305] (4)[17549:sh][Thermal/TZ/PMIC] [tsbuck2_raw_to_temp] t_current=29978
  [63980.372332] (4)[17549:sh][Thermal/TZ/PMIC] mt6357tsbuck2_get_hw_temp raw=675 T=29978
  [63980.372370] (4)[17549:sh][Thermal/TZ/PMIC] mt6357tsbuck2_get_hw_temp pre_tsbuck2_temp1=29978
  [63980.373016] (4)[17549:sh]mt635x-auxadc mt635x-auxadc: name:BAT_TEMP, channel=3, adc_out=0x5e2, adc_result=661
  [63980.373253] (4)[17549:sh][reg_to_current] 0x347 0x347 0x347 0xa4d 0xa4d 1
  [63980.374012] (0)[17549:sh]mt635x-auxadc mt635x-auxadc: name:VBIF, channel=11, adc_out=0xfeb, adc_result=1790
  [63980.374050] (0)[17549:sh][BattThermistorConverTemp] 10000 8315 9834 25 30 254
  [63980.374079] (0)[17549:sh][BattVoltToTemp] 657 16900 1786 -4
  [63980.374103] (0)[17549:sh][force_get_tbat_internal] 661,657,1,263,100,254 r:75 100 0
  [63980.374117] (0)[17549:sh]battery_psy_get_property psp:46 ret:0 val:254
  [63980.374131] (0)[17549:sh]psy_charger_get_property psp:46
  [63980.374148] (0)[17549:sh]psy_charger_get_property psp:46
  [63980.374476] (0)[17549:sh][Thermal/TZ/PMIC] [pmic_raw_to_temp] t_current=30139
  [63980.374498] (0)[17549:sh][Thermal/TZ/PMIC] [pmic_debug] Raw=700, T=30139
  [63980.374509] (0)[17549:sh][Thermal/TZ/PMIC] [mtktspmic_get_hw_temp] pre_temp1=30139
  [63980.375396] (4)[17549:sh][reg_to_current] 0x35e 0x35e 0x35e 0xa95 0xa95 1
  [63980.375759] (4)[17549:sh][BattThermistorConverTemp] 10000 8315 9834 25 30 254
  [63980.375792] (4)[17549:sh][BattVoltToTemp] 657 16900 1786 -4
  [63980.375826] (4)[17549:sh][force_get_tbat_internal] 661,657,1,270,100,254 r:75 100 0
  [63980.375855] (4)[17549:sh]battery_psy_get_property psp:46 ret:0 val:254
  [63980.375926] (4)[17549:sh]psy_charger_get_property psp:46
  [63980.377262] (4)[17549:sh]vcodec_suspend_notifier ok action = 4
  [63980.377270] (4)[17549:sh]rtc_pm_event = 4
  [63980.377302] -(4)[17549:sh]Abort: Callback failed on alarmtimer in platform_pm_suspend+0x0/0x60 returned -16
  [63980.377332] (4)[17549:sh][name:spm&][SPM] PM: suspend exit 2021-08-31 05:35:15.821012255 UTC
  [63980.377337] (4)[17549:sh][xxxxEEM] Start EEM resume
  [63980.378317] (4)[17549:sh]charger_pm_event: enter PM_POST_SUSPEND
  [63980.378329] (4)[17549:sh][name:spm&][SPM] PM: suspend exit 2021-08-31 05:35:15.822011717 UTC
  [63980.378438] (4)[17549:sh][MTK-BT]bt_pm_notifier_callback: bt_pm_notifier_callback: btonflag[1], event[4]
  [63980.378463] (4)[17549:sh][MTK-BT]bt_read_cr: HOST_MAILBOX_BT_ADDR[0x18007124], read[0x00000000]
  [63980.378479] (4)[17549:sh]PM: suspend exit
  ```
* 由于插着USB线，无法进入休眠，所以可以在调试串口触发休眠，这是一个很好的调试方法，节省时间
  ```
  [63980.365288] (6)[3191:Binder:418_2]active wakeup source: USB suspend lock
  ```

# Android内核Suspend分析

* 参考文档：[Suspend to RAM和Suspend to Idle分析，以及在HiKey上性能对比](https://www.cnblogs.com/arnoldlu/p/6253665.html)
* suspend关键函数
  ```CPP
  // kernel-4.19/kernel/power/suspend.c
  
  static int suspend_enter(suspend_state_t state, bool *wakeup)
  {
          // ...省略
  
          system_state = SYSTEM_SUSPEND;
          error = syscore_suspend();
          if (!error) {
                  *wakeup = pm_wakeup_pending();
                  if (!(suspend_test(TEST_CORE) || *wakeup)) {
                          trace_suspend_resume(TPS("machine_suspend"),
                                  state, true);
                          error = suspend_ops->enter(state);
                          trace_suspend_resume(TPS("machine_suspend"),
                                  state, false);
                  } else if (*wakeup) {
                          error = -EBUSY;
                  }
                  syscore_resume();
          }
  
          // ...省略
  }
  ```
* 添加函数栈打印：
  ```diff
  diff --git a/kernel-4.19/kernel/power/suspend.c b/kernel-4.19/kernel/power/suspend.c
  index 230cb727b8b..7a8f87bff58 100644
  --- a/kernel-4.19/kernel/power/suspend.c
  +++ b/kernel-4.19/kernel/power/suspend.c
  @@ -403,6 +403,7 @@ void __weak arch_suspend_enable_irqs(void)
   static int suspend_enter(suspend_state_t state, bool *wakeup)
   {
          int error, last_dev;
  +       dump_stack();
  
          error = platform_suspend_prepare(state);
          if (error)
  ```
* 内核dump信息：
  ```
  <4>[   44.510445] -(4)[3212:Binder:420_1]CPU: 4 PID: 3212 Comm: Binder:420_1 Tainted: P        W  O      4.19.127 #5
  <4>[   44.510485] -(4)[3212:Binder:420_1]Hardware name: MT6762V/WD (DT)
  <4>[   44.510523] -(4)[3212:Binder:420_1]Call trace:
  <4>[   44.510594] -(4)[3212:Binder:420_1] dump_backtrace+0x0/0x164
  <4>[   44.510649] -(4)[3212:Binder:420_1] show_stack+0x20/0x2c
  <4>[   44.510705] -(4)[3212:Binder:420_1] dump_stack+0xb8/0xf0
  <4>[   44.510759] -(4)[3212:Binder:420_1] suspend_devices_and_enter+0x15c/0x8f0
  <4>[   44.510808] -(4)[3212:Binder:420_1] pm_suspend+0x51c/0x664
  <4>[   44.510856] -(4)[3212:Binder:420_1] state_store+0xb0/0x108
  <4>[   44.510905] -(4)[3212:Binder:420_1] kobj_attr_store+0x14/0x24
  <4>[   44.510962] -(4)[3212:Binder:420_1] sysfs_kf_write+0x50/0x68
  <4>[   44.511014] -(4)[3212:Binder:420_1] kernfs_fop_write+0x138/0x1d4
  <4>[   44.511067] -(4)[3212:Binder:420_1] __vfs_write+0x54/0x15c
  <4>[   44.511116] -(4)[3212:Binder:420_1] vfs_write+0xe4/0x1a0
  <4>[   44.511165] -(4)[3212:Binder:420_1] ksys_write+0x78/0xd8
  <4>[   44.511214] -(4)[3212:Binder:420_1] __arm64_sys_write+0x20/0x2c
  <4>[   44.511265] -(4)[3212:Binder:420_1] el0_svc_common+0x9c/0x14c
  <4>[   44.511315] -(4)[3212:Binder:420_1] el0_svc_handler+0x68/0x84
  <4>[   44.511362] -(4)[3212:Binder:420_1] el0_svc+0x8/0xc
  ```
  * 有上可知，操作的如下函数，也就是操作了`/sys/power/state`节点
    ```CPP
    // kernel-4.19/kernel/power/main.c
    
    static ssize_t state_store(struct kobject *kobj, struct kobj_attribute *attr,
                               const char *buf, size_t n)
    {
            suspend_state_t state;
            int error;
    
            error = pm_autosleep_lock();
            if (error)
                    return error;
    
            if (pm_autosleep_state() > PM_SUSPEND_ON) {
                    error = -EBUSY;
                    goto out;
            }
    
            state = decode_state(buf, n);
            if (state < PM_SUSPEND_MAX) {
                    if (state == PM_SUSPEND_MEM)
                            state = mem_sleep_current;
    
                    error = pm_suspend(state);
            } else if (state == PM_SUSPEND_MAX) {
                    error = hibernate();
            } else {
                    error = -EINVAL;
            }
    
     out:
            pm_autosleep_unlock();
            return error ? error : n;
    }
    
    power_attr(state);
    ```

# Android Framework Suspend

* 主要是解决谁操作了`/sys/power/state`
* [Android休眠流程总结](https://www.cnblogs.com/rainey-forrest/p/13292638.html)
* ps -A | grep suspend
  ```
  system          420      1 10863200  4760 binder_ioctl_write_read 0 S android.system.suspend@1.0-service
  ```
* 电源管理服务是如何操作到`/sys/power/state`？
  ```
  * frameworks/base/services/core/java/com/android/server/power/PowerManagerService.java
    * public void goToSleep(long eventTime, int reason, int flags)
      * goToSleepInternal(eventTime, reason, flags, uid);
        * updatePowerStateLocked();
          * updateSuspendBlockerLocked();
            * setHalAutoSuspendModeLocked(false);
              * mNativeWrapper.nativeSetAutoSuspend(enable);
                * frameworks/base/services/core/jni/com_android_server_power_PowerManagerService.cpp
                  * static void nativeSetAutoSuspend(JNIEnv* /* env */, jclass /* clazz */, jboolean enable)
                    * enableAutoSuspend();
                      * sp<system::suspend::internal::ISuspendControlServiceInternal> suspendControl = getSuspendControlInternal();
                      * suspendControl->enableAutosuspend(&enabled);
                        * system/hardware/interfaces/suspend/1.0/default/SuspendControlService.cpp
                          * binder::Status SuspendControlServiceInternal::enableAutosuspend(bool* _aidl_return)
                            * return retOk(suspendService != nullptr && suspendService->enableAutosuspend(), _aidl_return);
                              * system/hardware/interfaces/suspend/1.0/default/SystemSuspend.cpp
                                * initAutosuspend();
                                  * bool success = WriteStringToFd(kSleepState, mStateFd);
                                    * static const char kSleepState[] = "mem";
                                    * mStateFd是构造函数传递的文件描述符
                                      * system/hardware/interfaces/suspend/1.0/default/main.cpp
                                      * sp<SystemSuspend> suspend = new SystemSuspend( std::move(wakeupCountFd), std::move(stateFd), std::move(suspendStatsFd), kStatsCapacity, std::move(kernelWakelockStatsFd), std::move(wakeupReasonsFd), std::move(suspendTimeFd), sleepTimeConfig, suspendControl, suspendControlInternal, true /* mUseSuspendCounter*/);
                                        * unique_fd stateFd{TEMP_FAILURE_RETRY(open(kSysPowerState, O_CLOEXEC | O_RDWR))};
                                          * static constexpr char kSysPowerState[] = "/sys/power/state";
  ```
