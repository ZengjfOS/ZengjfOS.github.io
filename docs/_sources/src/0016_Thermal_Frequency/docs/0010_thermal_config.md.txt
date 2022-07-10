# thermal config

温控配置

# 配置

* device/mediatek/mt6761/thermal.conf
  * vendor/etc/.tp/thermal.conf
  * 配置文件不是明文，有加密，需要使用mtk工具解密
    * [0010_thermal.txt](refers/0010_thermal.txt)
      ```
      /proc/driver/thermal/tzcharger
      1 120000 0 mtktscharger-sysrst 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 0 0 no-cooler 2000
      ```
      * Polling interval: 2000
        * kernel-4.19/drivers/misc/mediatek/thermal/common/thermal_zones/mtk_ts_charger.c
          * `static unsigned int interval; /* seconds, 0 : no auto polling */`

# 解密thermal.config

* Thermal_Config_Tool_exe_v1.1942.1/thermal_config_tool_V1.20.0_dev/decrypt
  * 采用的是excel的方式处理，需要独立处理加密、解密
  * 将thermal配置文件重命名为.mtc文件: thermal.mtc
  * decrypt_all_config.bat
    * thermal.txt
      * 其中的明文还是挺好理解的
    * 修改完成后，可直接使用.txt文件让修改策略生效。如果需要加密，按如下步骤进行：
    * PC CMD界面下运行，生成thermal而配置文件
      * encrypt.exe thermal.txt thermal.conf
* Thermal_Config_tool_exe_v2.2.2125.1/Thermal_config_tool_v2.2_64-bit.exe
  * 可以直接导入thermal.conf
    * 界面上的数据一列一种thermal zone配置
