# thermal core

理解struct thermal_zone_device(framework)和struct __thermal_zone(NTC)的差异

# 参考文档

* [Linux Hwmon Documentation](http://blog.foool.net/wp-content/uploads/linuxdocs/hwmon.pdf)
* [Linux thermal子系统和lm_sensors用户态工具](https://blog.csdn.net/scarecrow_byr/article/details/104402354)

# struct thermal_zone_device

* 这部分与设备树中的thermal_zones的每个节点对应，由thermal_core初始化，其代表的是所有thermal的thermal_zone的框架
* 其中的devdata会指向struct __thermal_zone，struct __thermal_zone表示一个实际的thermal设备，struct thermal_zone_device是框架，devdata来做到差异化，以及做到分离注册机制

```C
// include/linux/thermal.h

/**
 * struct thermal_zone_device - structure for a thermal zone
 * @id:     unique id number for each thermal zone
 * @type:   the thermal zone device type
 * @device: &struct device for this thermal zone
 * @trip_temp_attrs:    attributes for trip points for sysfs: trip temperature
 * @trip_type_attrs:    attributes for trip points for sysfs: trip type
 * @trip_hyst_attrs:    attributes for trip points for sysfs: trip hysteresis
 * @devdata:    private pointer for device private data
 * @trips:  number of trip points the thermal zone supports
 * @trips_disabled; bitmap for disabled trips
 * @passive_delay:  number of milliseconds to wait between polls when
 *          performing passive cooling.
 * @polling_delay:  number of milliseconds to wait between polls when
 *          checking whether trip points have been crossed (0 for
 *          interrupt driven systems)
 * @temperature:    current temperature.  This is only for core code,
 *          drivers should use thermal_zone_get_temp() to get the
 *          current temperature
 * @last_temperature:   previous temperature read
 * @emul_temperature:   emulated temperature when using CONFIG_THERMAL_EMULATION
 * @passive:        1 if you've crossed a passive trip point, 0 otherwise.
 * @prev_low_trip:  the low current temperature if you've crossed a passive
            trip point.
 * @prev_high_trip: the above current temperature if you've crossed a
            passive trip point.
 * @forced_passive: If > 0, temperature at which to switch on all ACPI
 *          processor cooling devices.  Currently only used by the
 *          step-wise governor.
 * @need_update:    if equals 1, thermal_zone_device_update needs to be invoked.
 * @ops:    operations this &thermal_zone_device supports
 * @tzp:    thermal zone parameters
 * @governor:   pointer to the governor for this thermal zone
 * @governor_data:  private pointer for governor data
 * @thermal_instances:  list of &struct thermal_instance of this thermal zone
 * @ida:    &struct ida to generate unique id for this zone's cooling
 *      devices
 * @lock:   lock to protect thermal_instances list
 * @node:   node in thermal_tz_list (in thermal_core.c)
 * @poll_queue: delayed work for polling
 * @notify_event: Last notification event
 */
struct thermal_zone_device {
    int id;
    char type[THERMAL_NAME_LENGTH];
    struct device device;
    struct attribute_group trips_attribute_group;
    struct thermal_attr *trip_temp_attrs;
    struct thermal_attr *trip_type_attrs;
    struct thermal_attr *trip_hyst_attrs;
    void *devdata;
    int trips;
    unsigned long trips_disabled;   /* bitmap for disabled trips */
    int passive_delay;
    int polling_delay;
    int temperature;
    int last_temperature;
    int emul_temperature;
    int passive;
    int prev_low_trip;
    int prev_high_trip;
    unsigned int forced_passive;
    atomic_t need_update;
    struct thermal_zone_device_ops *ops;
    struct thermal_zone_params *tzp;
    struct thermal_governor *governor;
    void *governor_data;
    struct list_head thermal_instances;
    struct ida ida;
    struct mutex lock;
    struct list_head node;
    struct delayed_work poll_queue;
    enum thermal_notify_event notify_event;
};
```

# struct __thermal_zone

实际thermal设备，对应struct thermal_zone_device中的devdata，一般我们写的驱动是这个，他会和上面的thermal_zone框架中的设备对应、绑定

```C
// drivers/thermal/of-thermal.c

/** 
 * struct __thermal_zone - internal representation of a thermal zone
 * @mode: current thermal zone device mode (enabled/disabled)
 * @passive_delay: polling interval while passive cooling is activated
 * @polling_delay: zone polling interval
 * @slope: slope of the temperature adjustment curve
 * @offset: offset of the temperature adjustment curve
 * @ntrips: number of trip points
 * @trips: an array of trip points (0..ntrips - 1)
 * @num_tbps: number of thermal bind params
 * @tbps: an array of thermal bind params (0..num_tbps - 1)
 * @sensor_data: sensor private data used while reading temperature and trend
 * @ops: set of callbacks to handle the thermal zone based on DT
 */            

struct __thermal_zone {
    enum thermal_device_mode mode;
    int passive_delay;
    int polling_delay;
    int slope;
    int offset;
    
    /* trip data */
    int ntrips;
    struct thermal_trip *trips;
        
    /* cooling binding data */
    int num_tbps;
    struct __thermal_bind_params *tbps;
    
    /* sensor interface */
    void *sensor_data; 
    const struct thermal_zone_of_device_ops *ops;
}; 
```

# thermal zone device

* 一个thermal zone device和设备树中的thermal_zones中的一个配置对应，默认其devdata(struct __thermal_zone)是没有处理函数的，需要对应的devdata设备注册才会填充，也就是thermal zone device只是一个系统性的框架，不同的devdata通过其自身驱动注册绑定到对应的thermal zone device上；
* thermal zone device有自己操作函数，devdata也有自己的操作函数，对于像温度获取，一般是thermal zone device通过devdata来最终获取温度；
* 这里的thermal zone device和devdata需要好好理解，devdata的驱动更多偏向于注册其处理函数；

```
* drivers/thermal/thermal_core.c
  └── fs_initcall(thermal_init);
      └── static int __init thermal_init(void)
          ├── result = thermal_register_governors();
          ├── result = of_parse_thermal_zones();
          │   └── drivers/thermal/of-thermal.c
          │       └── int __init of_parse_thermal_zones(void)
          │           ├── np = of_find_node_by_name(NULL, "thermal-zones");
          │           └── for_each_available_child_of_node(np, child)
          │               ├── tz = thermal_of_build_thermal_zone(child);
          │               │   ├── tz = kzalloc(sizeof(*tz), GFP_KERNEL);
          │               │   ├── ret = of_property_read_u32(np, "polling-delay-passive", &prop);
          │               │   ├── ret = of_property_read_u32(np, "polling-delay", &prop);
          │               │   ├── ret = of_property_read_u32_array(np, "coefficients", coef, 2);
          │               │   ├── child = of_get_child_by_name(np, "trips");
          │               │   └── zone = thermal_zone_device_register(child->name, tz->ntrips, mask, tz, ops, tzp, tz->passive_delay, tz->polling_delay);
          │               └── ops = kmemdup(&of_thermal_ops, sizeof(*ops), GFP_KERNEL);
          │                   └── of_thermal_ops
          │                       └── static struct thermal_zone_device_ops of_thermal_ops
          │                           ├── .get_mode = of_thermal_get_mode,
          │                           ├── .set_mode = of_thermal_set_mode,
          │                           ├── .get_trip_type = of_thermal_get_trip_type,
          │                           ├── .get_trip_temp = of_thermal_get_trip_temp,
          │                           ├── .set_trip_temp = of_thermal_set_trip_temp,
          │                           ├── .get_trip_hyst = of_thermal_get_trip_hyst,
          │                           ├── .set_trip_hyst = of_thermal_set_trip_hyst,
          │                           ├── .get_crit_temp = of_thermal_get_crit_temp,
          │                           ├── .bind = of_thermal_bind,
          │                           └── .unbind = of_thermal_unbind,
          └── result = register_pm_notifier(&thermal_pm_nb);
              └── static struct notifier_block thermal_pm_nb
                  └── .notifier_call = thermal_pm_notify,
                      └── static int thermal_pm_notify(struct notifier_block *nb, unsigned long mode, void *_unused)
                          └── list_for_each_entry(tz, &thermal_tz_list, node)
                              └── thermal_zone_device_update(tz, THERMAL_EVENT_UNSPECIFIED);
                                  ├── update_temperature(tz);
                                  │   └── ret = thermal_zone_get_temp(tz, &temp);
                                  │       └── drivers/thermal/thermal_helpers.c
                                  │           └── ret = tz->ops->get_temp(tz, temp);
                                  │               └── drivers/thermal/of-thermal.c
                                  │                   └── static int of_thermal_get_temp(struct thermal_zone_device *tz, int *temp)
                                  │                       └── struct __thermal_zone *data = tz->devdata;
                                  │                           └── return data->ops->get_temp(data->sensor_data, temp);
                                  ├── thermal_zone_set_trips(tz);
                                  │   └── drivers/thermal/thermal_helpers.c
                                  │       └── void thermal_zone_set_trips(struct thermal_zone_device *tz)
                                  │           ├── for (i = 0; i < tz->trips; i++)
                                  │           │   ├── tz->ops->get_trip_temp(tz, i, &trip_temp);
                                  │           │   └── tz->ops->get_trip_hyst(tz, i, &hysteresis);
                                  │           └── ret = tz->ops->set_trips(tz, low, high);
                                  └── for (count = 0; count < tz->trips; count++)
                                      └── handle_thermal_trip(tz, count);
                                          ├── tz->ops->get_trip_type(tz, trip, &type);
                                          ├── if (type == THERMAL_TRIP_CRITICAL || type == THERMAL_TRIP_HOT)
                                          │   └── handle_critical_trips(tz, trip, type);
                                          │       ├── tz->ops->get_trip_temp(tz, trip, &trip_temp);
                                          │       ├── trace_thermal_zone_trip(tz, trip, trip_type);
                                          │       └── if (trip_type == THERMAL_TRIP_CRITICAL)
                                          │           ├── dev_emerg(&tz->device, "critical temperature reached (%d C), shutting down\n", tz->temperature / 1000);
                                          │           └── if (!power_off_triggered)
                                          │               ├── thermal_emergency_poweroff();
                                          │               ├── orderly_poweroff(true);
                                          │               └── power_off_triggered = true;
                                          └── monitor_thermal_zone(tz);
                                              └── thermal_zone_device_set_polling(tz, 0);
```

# thermal zone

* 其实这里叫thermal貌似更合适，表示一个thermal设备
* `brcm,bcm2711-thermal`驱动probe，其通过`#thermal-sensor-cells`指定thermal zones中的索引，目前是0
* bcm2711_thermal驱动可以认为是传感器驱动，最终会挂在到`drivers/thermal/thermal_core.c`生成的thermal zone框架设备上，相当于绑定的动作
* 主要是向thermal zone device的devdata注册实际NTC传感器调用函数，例如温度获取函数；

```
* drivers/thermal/broadcom/bcm2711_thermal.c
  └── module_platform_driver(bcm2711_thermal_driver);
      └── static struct platform_driver bcm2711_thermal_driver
          ├── .driver
          │   └── .of_match_table = bcm2711_thermal_id_table,
          │       └──  static const struct of_device_id bcm2711_thermal_id_table[]
          │           └── { .compatible = "brcm,bcm2711-thermal" },
          └── .probe = bcm2711_thermal_probe,
              └── static int bcm2711_thermal_probe(struct platform_device *pdev)
                  ├── thermal = devm_thermal_zone_of_sensor_register(dev, 0, priv, &bcm2711_thermal_of_ops);
                  │   ├── bcm2711_thermal_of_ops
                  │   │   └── static const struct thermal_zone_of_device_ops bcm2711_thermal_of_ops
                  │   │       └── .get_temp   = bcm2711_get_temp,
                  │   │           └── static int bcm2711_get_temp(void *data, int *temp)
                  │   │               ├── int slope = thermal_zone_get_slope(priv->thermal);
                  │   │               ├── int offset = thermal_zone_get_offset(priv->thermal);
                  │   │               ├── ret = regmap_read(priv->regmap, AVS_RO_TEMP_STATUS, &val);
                  │   │               ├── t = slope * val + offset;
                  │   │               └── *temp = t < 0 ? 0 : t;
                  │   └── devm_thermal_zone_of_sensor_register(...);
                  │       └── drivers/thermal/of-thermal.c
                  │           └── struct thermal_zone_device *devm_thermal_zone_of_sensor_register(struct device *dev, int sensor_id, void *data, const struct thermal_zone_of_device_ops *ops)
                  │               ├── ptr = devres_alloc(devm_thermal_zone_of_sensor_release, sizeof(*ptr), GFP_KERNEL);
                  │               └── tzd = thermal_zone_of_sensor_register(dev, sensor_id, data, ops);
                  │                   ├── np = of_find_node_by_name(NULL, "thermal-zones");
                  │                   │   └── 这是隐藏数据
                  │                   ├── sensor_np = of_node_get(dev->of_node);
                  │                   └── for_each_available_child_of_node(np, child)
                  │                       ├── ret = of_parse_phandle_with_args(child, "thermal-sensors", "#thermal-sensor-cells", 0, &sensor_specs);
                  │                       └── if (sensor_specs.np == sensor_np && id == sensor_id)
                  │                           └── tzd = thermal_zone_of_add_sensor(child, sensor_np, data, ops);
                  │                               └── drivers/thermal/of-thermal.c
                  │                                   └── static struct thermal_zone_device *thermal_zone_of_add_sensor(struct device_node *zone, struct device_node *sensor, void *data, const struct thermal_zone_of_device_ops *ops)
                  │                                       ├── tzd = thermal_zone_get_zone_by_name(zone->name);
                  │                                       │   └── drivers/thermal/thermal_core.c
                  │                                       │       └── list_for_each_entry(pos, &thermal_tz_list, node)
                  │                                       │           └── if (!strncasecmp(name, pos->type, THERMAL_NAME_LENGTH))
                  │                                       │               ├── found++;
                  │                                       │               └── ref = pos;
                  │                                       └── for_each_available_child_of_node(np, child)
                  │                                           └── if (sensor_specs.np == sensor_np && id == sensor_id)
                  │                                               └── tzd = thermal_zone_of_add_sensor(child, sensor_np, data, ops);
                  │                                                   ├── tzd = thermal_zone_get_zone_by_name(zone->name);
                  │                                                   ├── tzd->ops->get_temp = of_thermal_get_temp;
                  │                                                   └── tzd->ops->get_trend = of_thermal_get_trend;
                  └── ret = thermal_add_hwmon_sysfs(thermal);
                      ├── hwmon = kzalloc(sizeof(*hwmon), GFP_KERNEL);
                      ├── hwmon->device = hwmon_device_register_with_info(&tz->device, hwmon->type, hwmon, NULL, NULL);
                      ├── temp = kzalloc(sizeof(*temp), GFP_KERNEL);
                      ├── snprintf(temp->temp_input.name, sizeof(temp->temp_input.name), "temp%d_input", hwmon->count);
                      ├── sysfs_attr_init(&temp->temp_input.attr.attr);
                      └── result = device_create_file(hwmon->device, &temp->temp_input.attr);
```
