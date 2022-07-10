# thermal hwmon

the linux hardware monitoring kernel api

# 参考文档

* [Linux Hwmon Documentation](http://blog.foool.net/wp-content/uploads/linuxdocs/hwmon.pdf)
* [Linux thermal子系统和lm_sensors用户态工具](https://blog.csdn.net/scarecrow_byr/article/details/104402354)

# driver

* `brcm,bcm2711-thermal`驱动probe，其通过`#thermal-sensor-cells`指定thermal zones中的索引策略，目前是0
* bcm2711_thermal驱动可以认为是传感器驱动，最终会挂在到`drivers/thermal/thermal_core.c`生成的thermal zone框架设备上，相当于绑定的动作

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
                      ├── hwmon = thermal_hwmon_lookup_by_type(tz);
                      ├── hwmon = kzalloc(sizeof(*hwmon), GFP_KERNEL);
                      ├── hwmon->device = hwmon_device_register_with_info(&tz->device, hwmon->type, hwmon, NULL, NULL);
                      ├── temp = kzalloc(sizeof(*temp), GFP_KERNEL);
                      ├── snprintf(temp->temp_input.name, sizeof(temp->temp_input.name), "temp%d_input", hwmon->count);
                      ├── sysfs_attr_init(&temp->temp_input.attr.attr);
                      └── result = device_create_file(hwmon->device, &temp->temp_input.attr);
```

# sysfs

* cd /sys/class/hwmon
  * ls 
    ```
    hwmon0  hwmon1
    ```
  * cd hwmon0
  * cat name
    ```
    cpu_thermal
    ```
  * cat temp1_input
    ```
    45277
    ```
