# thermal monitor

thermal monitor注册thermal zone设备、thermal cooling设备

# thermal zone device

* 注册thermal zone设备流程，最终相当于注册一个work，用于加入到workqueue
  * passive_delay: 触发后的检测周期
  * polling_delay: 未触发的检测周期
* 注册完成后，就会开始处理更新温度数据
  * [thermal子系统概述](http://tianyu-code.top/Linux%E5%86%85%E6%A0%B8/thermal/)
    * 温控肯定要循环监控设备温度，该操作在注册时就会开启，并循环执行
  * 注册设备时，调用一次该函数：thermal_zone_device_update(tz, THERMAL_EVENT_UNSPECIFIED);
    * 这里特别需要注意，这里会将poll_queue注册到system_freezable_wq中，这里也就是循环执行的入口

```
* kernel-4.19/drivers/misc/mediatek/thermal/mtk_thermal_monitor.c
  └── struct thermal_zone_device *mtk_thermal_zone_device_register_wrapper(char *type, int trips, void *devdata, const struct thermal_zone_device_ops *ops, int tc1, int tc2, int passive_delay, int polling_delay)
      ├── tzdata = kzalloc(sizeof(struct mtk_thermal_tz_data), GFP_KERNEL);
      ├── tz = thermal_zone_device_register(type, ...)
      │   └── kernel-4.19/drivers/thermal/thermal_core.c
      │       └── struct thermal_zone_device *thermal_zone_device_register(const char *type, int trips, int mask, void *devdata, struct thermal_zone_device_ops *ops, struct thermal_zone_params *tzp, int passive_delay, int polling_delay)
      │           ├── atomic_set(&tz->need_update, 1);
      │           ├── result = ida_simple_get(&thermal_tz_ida, 0, 0, GFP_KERNEL);
      │           ├── tz->id = result;
      │           ├── dev_set_name(&tz->device, "thermal_zone%d", tz->id);
      │           ├── result = device_register(&tz->device);
      │           ├── INIT_DELAYED_WORK(&tz->poll_queue, thermal_zone_device_check);
      │           ├── bind_tz(tz);
      │           └── if (atomic_cmpxchg(&tz->need_update, 1, 0))
      │               └── thermal_zone_device_update(tz, THERMAL_EVENT_UNSPECIFIED);
      │                   └── for (count = 0; count < tz->trips; count++)
      │                       └── handle_thermal_trip(tz, count);
      │                           └── monitor_thermal_zone(tz);
      │                               └── else if (tz->polling_delay)
      │                                   └── thermal_zone_device_set_polling(tz, tz->polling_delay);
      │                                       └── else if (delay)
      │                                           └── mod_delayed_work(system_freezable_wq, &tz->poll_queue, msecs_to_jiffies(delay));
      └── tzidx = mtk_thermal_get_tz_idx(type);
          └── else if (strncmp(type, "mtktscharger", 12) == 0)
              └── return MTK_THERMAL_SENSOR_CHARGER;
```
# thermal cooling device

注册thermal冷却设备

```
* kernel-4.19/drivers/misc/mediatek/thermal/mtk_thermal_monitor.c
  └── struct thermal_cooling_device *mtk_thermal_cooling_device_register_wrapper(char *type, void *devdata, const struct thermal_cooling_device_ops *ops)
      ├── mcdata = kzalloc(sizeof(struct mtk_thermal_cooler_data), GFP_KERNEL);
      └── ret = thermal_cooling_device_register(type, mcdata, &mtk_cooling_wrapper_dev_ops);
          └── kernel-4.19/drivers/thermal/thermal_core.c
              └── struct thermal_cooling_device *thermal_cooling_device_register(const char *type, void *devdata, const struct thermal_cooling_device_ops *ops)
                  └── return __thermal_cooling_device_register(NULL, type, devdata, ops);
                      ├── cdev = kzalloc(sizeof(*cdev), GFP_KERNEL);
                      ├── result = ida_simple_get(&thermal_cdev_ida, 0, 0, GFP_KERNEL);
                      ├── cdev->id = result;
                      ├── dev_set_name(&cdev->device, "cooling_device%d", cdev->id);
                      └── result = device_register(&cdev->device);
```

# thermal poll_queue

* 根据pm notifier来打开、关闭wokequeue工作
* pm notifier是机器休眠、唤醒的时候会调用处理的
  * [Linux Thermal机制源码分析之Governor](https://blog.csdn.net/weixin_43555423/article/details/105930766)
  * [thermal子系统概述](http://tianyu-code.top/Linux%E5%86%85%E6%A0%B8/thermal/)

```
* kernel-4.19/drivers/thermal/thermal_core.c
  └── fs_initcall(thermal_init);
      └── static int __init thermal_init(void)
          └── result = register_pm_notifier(&thermal_pm_nb);
              └── static struct notifier_block thermal_pm_nb
                  └── .notifier_call = thermal_pm_notify,
                      └── static int thermal_pm_notify(struct notifier_block *nb, unsigned long mode, void *_unused)
                          └── list_for_each_entry(tz, &thermal_tz_list, node)
                              ├── thermal_zone_device_init(tz);
                              └── thermal_zone_device_update(tz, THERMAL_EVENT_UNSPECIFIED);
                                  ├── update_temperature(tz);
                                  │   └── 获取温度
                                  ├── thermal_zone_set_trips(tz);
                                  │   └── 设置触发
                                  └── for (count = 0; count < tz->trips; count++)
                                      └── handle_thermal_trip(tz, count);
                                          └── monitor_thermal_zone(tz);
                                              └── thermal_zone_device_set_polling(tz, tz->polling_delay);
                                                  └── mod_delayed_work(system_freezable_wq, &tz->poll_queue, msecs_to_jiffies(delay));
                                                      └── poll_queue
                                                          └── static void thermal_zone_device_check(struct work_struct *work)
                                                              └── thermal_zone_device_update(tz, THERMAL_EVENT_UNSPECIFIED);
```
