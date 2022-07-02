# Android Sensor Power

在PL阶段访问PMIC，配置Sensor电源输出

# PL MT6357 init

```
* vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6765/src/drivers/pmic.c
  * U32 pmic_init (void)
    * print("[PMIC]Preloader Start\n");
    * print("[PMIC]MT6357 CHIP Code = 0x%x\n", get_PMIC_chip_version());
    * mt6357_probe();
* vendor/mediatek/proprietary/bootable/bootloader/preloader/custom/k62v1_64_bsp/dct/dct/codegen.dws
  * dws生成文件如下：
    * out/target/product/k62v1_64_bsp/obj/PRELOADER_OBJ/inc/
      * pmic_drv.h
      * pmic_drv.c
        * void pmu_drv_tool_customization_init(void)
          * pmic_set_register_value(PMIC_RG_LDO_VLDO28_EN_0,1);
```

# 打开VLDO28

```diff
diff --git a/vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6765/src/drivers/pmic.c b/vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6765/src/drivers/pmic.c
index 0acdb975cd3..ab66e3249ad 100644
--- a/vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6765/src/drivers/pmic.c
+++ b/vendor/mediatek/proprietary/bootable/bootloader/preloader/platform/mt6765/src/drivers/pmic.c
@@ -647,6 +647,8 @@ static void pmic_efuse_sw_load(void)
 /*
  * PMIC Init Code
  */
+#define _pmic_set_register_value(flagname, val) \
+    pmic_config_interface(flagname##_ADDR, (val), flagname##_MASK, flagname##_SHIFT)

 U32 pmic_init (void)
 {
@@ -657,6 +659,7 @@ U32 pmic_init (void)

        print("[PMIC]MT6357 CHIP Code = 0x%x\n",
                get_PMIC_chip_version());
+       _pmic_set_register_value(PMIC_RG_LDO_VLDO28_EN_0,1);

        /* Boot debug status */
        pmic_dbg_status(1);
```
