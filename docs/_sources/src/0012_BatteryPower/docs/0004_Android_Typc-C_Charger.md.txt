# Android Type-C Charger

Android Type-C 充电

# 参考文档

* [锂电池充电的原理](https://blog.csdn.net/zhenwenxian/article/details/7471892)
* [MTK平台充电模块梳理](https://blog.csdn.net/yuewen2008/article/details/80899568)
* [MTK Battery系统](https://blog.csdn.net/u012719256/article/details/78865196)
* [0003_USB_PD_Protocol.md](0003_USB_PD_Protocol.md)
* https://github.com/MediaTek-Labs/common-kernel-4.19
* [Android Healthd电池服务分析](https://www.cnblogs.com/linhaostudy/p/12002068.html)
* Smartphone/HW/Common Design Notes/PMU/Charger
  * Charging_study_for_Customer_SW_V0.1_20191118.pdf
    * **重点阅读**

# 简述

MTK方案的电池充电过程分为预充、恒流充电（CC模式）、恒压充电（CV模式）三种模式，从充电状态图看出来，刚开始充电的时候，代码先判断是插USB充电还是插ac充电，电池在进入充电阶段分为快速充电、CC（恒流充电）、CV（恒压充电）。

Charger所处的位置，在通往电池Battery的那条通路上，会有一个毫欧级别的电阻，两端接着Gauge，以此来判定电池电流状态

# dts

* kernel-4.19/arch/arm64/boot/dts/mediatek/mt6765.dts
  ```dts
  charger: charger {
      compatible = "mediatek,charger";
      gauge = <&mtk_gauge>;
      charger = <&mt6370_chg>;
      bootmode = <&chosen>;
      pmic = <&main_pmic>;

      algorithm_name = "Basic";
      charger_configuration= <0>;

      // ...省略
  };
  ```
* kernel-4.19/arch/arm64/boot/dts/mediatek/mt6370.dtsi
  ```dts
  mt6370_chg: charger {
      compatible = "mediatek,mt6370_pmu_charger";
      interrupt-names = "chg_mivr", "chg_aiclmeasi",
          "attachi", "ovpctrl_uvp_d_evt", "chg_wdtmri",
          "chg_vbusov", "chg_tmri", "chg_treg", "dcdti";
      charger_name = "primary_chg";
      load_switch_name = "primary_load_switch";
      // ...省略
      charger = <&mt6370_chg>;
      bc12_sel = <0>;
      otg_vbus: usb-otg-vbus {
          regulator-compatible = "usb-otg-vbus";
          regulator-name = "usb-otg-vbus";
          regulator-min-microvolt = <4350000>;
          regulator-max-microvolt = <5800000>;
          regulator-min-microamp = <500000>;
          regulator-max-microamp = <3000000>;
      };
  };
  ```
* kernel-4.19/arch/arm64/boot/dts/mediatek/mt6357.dtsi
  ```dts
  mtk_gauge: mtk_gauge {
      compatible = "mediatek,mt6357-gauge";
      charger = <&mt6370_chg>;
      bootmode = <&chosen>;
      // ...省略
  };
  ```
* kernel-4.9/arch/arm64/boot/dts/mediatek/bat_setting/mt6765_battery_prop.dtsi
  ```dts
  bat_gm30: battery{
      compatible = "mediatek,bat_gm30";
      // ...省略
  #include "mt6765_battery_table.dtsi"
  };
  ```

# driver

* Android Q
  * kernel-4.9/drivers/power/supply/mediatek/charger
    * 充电
  * kernel-4.9/drivers/power/supply/mediatek/battery
    * 电池
* Android R
  * kernel-4.19/drivers/power/supply/mtk_charger.c
  * kernel-4.19/drivers/power/supply/mtk_battery.c
  * kernel-4.19/drivers/power/supply/mt6357-gauge.c
  * kernel-4.19/drivers/misc/mediatek/pmic/mt6370/mt6370_pmu_charger.c

# 充电电流

* Android R
  ```
  * drivers/power/supply/mtk_charger.c
    * static int mtk_charger_probe(struct platform_device *pdev)
      * mtk_charger_parse_dt(info, &pdev->dev);
        * mtk_basic_charger_init(info);
          * drivers/power/supply/mtk_basic_charger.c
            * int mtk_basic_charger_init(struct mtk_charger *info)
              * static int do_algorithm(struct mtk_charger *info)
                * static bool select_charging_current_limit(struct mtk_charger *info, struct chg_limit_setting *setting)
  ```

# 电池容量

* vendor/mediatek/proprietary/packages/overlay/vendor/FrameworkResOverlay/power/res/xml/power_profile.xml
  ```xml
  <!-- This is the battery capacity in mAh (measured at nominal voltage) -->
  <item name="battery.capacity">3000</item>
  ```

# 电池充放电

* 3CBatteryManager.apk
* 在设置选项中，电池可以将记录的数据保存出来
  * [History]
  * [左上角三条杠] -> [Settings] -> [Battery] -> [Export battery history]
* 修改监听参数
  * [左上角三条杠] -> [Settings] -> [Battery] -> [Monitoring]

# usb plug in log

```
<6>[ 2776.747612]  (6)[235:irq/30-mt6370_p]mt6370_pmu_irq_handler
<6>[ 2776.749495]  (6)[61:pd_dbg_info]///PD dbg info 34d
<4>[ 2776.749536]  (6)[61:pd_dbg_info]< 2776.749>TCPC-TCPC:ps_change=2
<6>[ 2776.755642]  (5)[235:irq/30-mt6370_p]mt6370_pmu 5-0034: mt6370_pmu_irq_handler: handler irq_domain = (8, 4)
<5>[ 2776.785404] -(4)[238:type_c_port0]alarmtimer_enqueue, 1620820906063218464
<6>[ 2776.785430]  (6)[61:pd_dbg_info]///PD dbg info 63d
<4>[ 2776.785466]  (6)[61:pd_dbg_info]< 2776.785>TCPC-TCPC:Wakeup
<4>[ 2776.785466] < 2776.785>TCPC-TCPC:wakeup_timer
<6>[ 2776.786957]  (4)[238:type_c_port0]pd_tcp_notifier_call attach wait sink
<6>[ 2776.811292]  (6)[61:pd_dbg_info]///PD dbg info 113d
<4>[ 2776.811359]  (6)[61:pd_dbg_info]< 2776.786>TCPC-TYPEC:[CC_Alert] 5/5
<4>[ 2776.811359] < 2776.787>TCPC-TYPEC:** AttachWait.SNK
<4>[ 2776.811359] < 2776.788>TCPC-TCPC:ps_change=2
<5>[ 2776.886613] -(4)[916:readSpeechMessa][MUSB]musb_stage0_irq 1208: musb_stage0_irq:1208 MUSB_INTR_RESET (b_peripheral)
<5>[ 2776.886689] -(4)[916:readSpeechMessa]QMU_WARN,<musb_disable_q_all 333>, disable_q_all
<5>[ 2776.886731] -(4)[916:readSpeechMessa]QMU_WARN,<mtk_qmu_disable 847>, disable RQ(1)
<5>[ 2776.886841] -(4)[916:readSpeechMessa]QMU_WARN,<mtk_qmu_disable 847>, disable RQ(2)
<5>[ 2776.886897] -(4)[916:readSpeechMessa]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(1)
<5>[ 2776.887004] -(4)[916:readSpeechMessa]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(2)
<5>[ 2776.887056] -(4)[916:readSpeechMessa]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(3)
<5>[ 2776.887113] -(4)[916:readSpeechMessa]BATTERY_SetUSBState Success! Set 1
<6>[ 2776.887147] -(4)[916:readSpeechMessa]android_disconnect
<4>[ 2776.887352] -(4)[916:readSpeechMessa]nuke: 3 callbacks suppressed
<5>[ 2776.887375] -(4)[916:readSpeechMessa][MUSB]nuke 302: call musb_g_giveback on function nuke ep is ep1out
<5>[ 2776.887375] , skip_cnt<3>
<5>[ 2776.887454] -(4)[916:readSpeechMessa][MUSB]nuke 302: call musb_g_giveback on function nuke ep is ep1out
<5>[ 2776.887454] , skip_cnt<0>
<5>[ 2776.887511] -(4)[916:readSpeechMessa][MUSB]nuke 302: call musb_g_giveback on function nuke ep is ep1out
<5>[ 2776.887511] , skip_cnt<0>
<5>[ 2776.887567] -(4)[916:readSpeechMessa][MUSB]nuke 302: call musb_g_giveback on function nuke ep is ep1out
<5>[ 2776.887567] , skip_cnt<0>
<5>[ 2776.887623] -(4)[916:readSpeechMessa][MUSB]nuke 302: call musb_g_giveback on function nuke ep is ep1out
<5>[ 2776.887623] , skip_cnt<0>
<6>[ 2776.887864] -(4)[916:readSpeechMessa]configfs-gadget gadget: acm ttyGS0 deactivated
<6>[ 2776.889496]  (4)[15102:kworker/4:1]android_work: sent uevent USB_STATE=DISCONNECTED
<6>[ 2776.907492]  (7)[236:tcpc_timer_type]pd_tcp_notifier_call sink vbus 5000mv 150ma type(1)
<6>[ 2776.907541]  (6)[61:pd_dbg_info]///PD dbg info 76d
<4>[ 2776.907568]  (6)[61:pd_dbg_info]< 2776.907>TCPC-TYPEC:[CC_Change] 5/5
<4>[ 2776.907568] < 2776.907>TCPC-TYPEC:** Custom.SRC
<6>[ 2776.907912]  (4)[236:tcpc_timer_type]charger_manager_enable_power_path: enable power path = 1
<6>[ 2776.907980]  (4)[236:tcpc_timer_type]mt6370_pmu_charger mt6370_pmu_charger: mt6370_enable_power_path: en = 1
<6>[ 2776.908031]  (4)[236:tcpc_timer_type]mt6370_pmu_charger mt6370_pmu_charger: __mt6370_set_mivr: mivr = 4500000 (0x06)
<6>[ 2776.908425]  (4)[236:tcpc_timer_type]mt6370_pmu_charger mt6370_pmu_charger: mt6370_enable_irq: (chg_mivr) en = 1
<7>[ 2776.908692] -(4)[236:tcpc_timer_type]mt6370_pmu 5-0034: mt6370_pmu_irq_enable: hwirq = 6, chg_mivr
<6>[ 2776.909139]  (5)[235:irq/30-mt6370_p]mt6370_pmu_irq_handler
<5>[ 2776.909160]  (4)[236:tcpc_timer_type]PD charger event:14 0
<6>[ 2776.909191]  (4)[236:tcpc_timer_type]pd_tcp_notifier_call USB Plug in, pol = 0
<5>[ 2776.909309]  (4)[236:tcpc_timer_type][MUSB]otg_tcp_notifier_call 343: TCP_NOTIFY_TYPEC_STATE, old_state=0, new_state=6
<6>[ 2776.909461]  (6)[252:chgdet_thread]charger type: charger IN
<6>[ 2776.923966]  (5)[235:irq/30-mt6370_p]mt6370_pmu 5-0034: mt6370_pmu_irq_handler: handler irq_domain = (0, 6)
<6>[ 2776.924295]  (5)[235:irq/30-mt6370_p]mt6370_pmu_charger mt6370_pmu_charger: mt6370_enable_irq: (chg_mivr) en = 0
<5>[ 2776.924355]  (7)[99:pmic_thread][PMIC] [PMIC_INT] Reg[0x91a]=0x40
<7>[ 2776.924575] -(5)[235:irq/30-mt6370_p]mt6370_pmu 5-0034: mt6370_pmu_irq_disable: hwirq = 6, chg_mivr
<6>[ 2776.935315]  (6)[61:pd_dbg_info]///PD dbg info 85d
<4>[ 2776.935384]  (6)[61:pd_dbg_info]< 2776.909>TCPC-TYPEC:Attached-> CUSTOM_SRC
<4>[ 2776.935384] < 2776.909>TCPC-TCPC:usb_port_attached
<6>[ 2776.973774]  (7)[15638:kworker/7:1]android_work: sent uevent USB_STATE=CONNECTED
<6>[ 2776.996760] -(4)[961:OomAdjuster]configfs-gadget gadget: high-speed config #1: b
<5>[ 2776.996943] -(4)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2776.997005] -(4)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 512, epnum 1,hwepnum 1
<5>[ 2776.997048] -(4)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 631>, enable RQ(1)
<5>[ 2776.997103] -(4)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep1out for bulk OUT, maxpacket 512
<5>[ 2776.997154] -(4)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2776.997202] -(4)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 1024, epnum 1,hwepnum 1
<5>[ 2776.997242] -(4)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(1)
<5>[ 2776.997297] -(4)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep1in for bulk IN, maxpacket 512
<5>[ 2776.997353] -(4)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=INT
<5>[ 2776.997400] -(4)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 1536, epnum 3,hwepnum 3
<5>[ 2776.997438] -(4)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(3)
<5>[ 2776.997491] -(4)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep3in for int IN, maxpacket 10
<5>[ 2776.997540] -(4)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2776.997588] -(4)[961:OomAdjuster][MUSB]check_musb_dbuffer_avail 1299: <check_musb_dbuffer_avail, 1299>, got bulk ep:82 in function :acm
<5>[ 2776.997627] -(4)[961:OomAdjuster][MUSB]is_saving_mode 993: 1
<5>[ 2776.997664] -(4)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=Function FS Gadget
<5>[ 2776.997701] -(4)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=acm
<5>[ 2776.997742] -(4)[961:OomAdjuster][MUSB]is_db_ok 1188: acm IN desc-addr=82, addr=82
<5>[ 2776.997783] -(4)[961:OomAdjuster][MUSB]is_db_ok 1202: [acm] EP2-IN as double buffer
<5>[ 2776.997822] -(4)[961:OomAdjuster][MUSB]fifo_setup 1373: Saving mode, but EP2 supports DBBUF
<5>[ 2776.997867] -(4)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 22 after 512, fifo address is 2048, epnum 2,hwepnum 2
<5>[ 2776.997907] -(4)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(2)
<5>[ 2776.997959] -(4)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep2in for bulk IN, maxpacket 512
<5>[ 2776.998000] -(4)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2776.998046] -(4)[961:OomAdjuster][MUSB]check_musb_dbuffer_avail 1299: <check_musb_dbuffer_avail, 1299>, got bulk ep:2 in function :acm
<5>[ 2776.998083] -(4)[961:OomAdjuster][MUSB]is_saving_mode 993: 1
<5>[ 2776.998119] -(4)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=Function FS Gadget
<5>[ 2776.998155] -(4)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=acm
<5>[ 2776.998195] -(4)[961:OomAdjuster][MUSB]is_db_ok 1188: acm OUT desc-addr=2, addr=2
<5>[ 2776.998235] -(4)[961:OomAdjuster][MUSB]is_db_ok 1198: [acm] EP2-OUT as signle buffer
<5>[ 2776.998281] -(4)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 3072, epnum 2,hwepnum 2
<5>[ 2776.998319] -(4)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 631>, enable RQ(2)
<5>[ 2776.998370] -(4)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep2out for bulk OUT, maxpacket 512
<5>[ 2776.998459] -(4)[961:OomAdjuster]BATTERY_SetUSBState Success! Set 2
<6>[ 2777.002888]  (4)[15102:kworker/4:1]android_work: sent uevent USB_STATE=CONFIGURED
<5>[ 2777.006365] -(4)[957:android.bg][MUSB]service_zero_data_request 339: no more req, clr RXPKTRDY to avoid err RX FIFO/DMA read!! csr:0x2000
<6>[ 2777.007422]  (1)[9248:kworker/1:1]usb_state<CONFIGURED>
<7>[ 2777.059817]  (5)[3739:hif_thread]FPSGO_COMPfpsgo_ctrl2comp_dequeue_start xgf_ret:3
<6>[ 2777.060090]  (5)[3739:hif_thread][wlan][3739]halSetDriverOwn:(INIT INFO) DRIVER OWN Done[7547 us]
<7>[ 2777.060237]  (5)[612:adbd]FPSGO_COMPfpsgo_ctrl2comp_dequeue_end xgf_ret:3
<6>[ 2777.063353]  (5)[612:adbd]unregister_gadget
<6>[ 2777.063797]  (7)[3738:main_thread][wlan][3738]nicUpdateLinkQuality:(RLM INFO) Rssi=-36, NewRssi=-36
<5>[ 2777.063848]  (5)[612:adbd][MUSB]musb_gadget_pullup 2382: is_on=0, softconnect=1 ++
<5>[ 2777.063882] -(5)[612:adbd][MUSB]musb_gadget_pullup 2395: is_on=0, softconnect=1 ++
<5>[ 2777.063895] -(5)[612:adbd][MUSB]musb_pullup 2325: MUSB: gadget pull up 0 start, musb->power:1
<5>[ 2777.063906] -(5)[612:adbd][MUSB]musb_pullup 2334: MUSB: gadget pull up 0 end
<6>[ 2777.063944]  (5)[612:adbd]android_disconnect
<6>[ 2777.064021] -(5)[612:adbd]configfs-gadget gadget: acm ttyGS0 deactivated
<6>[ 2777.064051]  (5)[612:adbd]configfs_composite_unbind
<6>[ 2777.064061]  (5)[612:adbd]purge_configs_funcs
<5>[ 2777.064109]  (5)[612:adbd][MUSB]musb_gadget_stop 2700: musb_gadget_stop
<5>[ 2777.064128] -(5)[612:adbd][MUSB]mt_usb_try_idle 288: (null) inactive, for idle timer for 4 ms
<6>[ 2777.064817]  (7)[636:usb ffs open]read descriptors
<5>[ 2777.064861]  (7)[636:usb ffs open]skip os descriptor, os_descs_count:1, len:35 all to 0
<6>[ 2777.064877]  (7)[636:usb ffs open]read strings
<6>[ 2777.065158]  (5)[15974:kworker/5:1]android_work: sent uevent USB_STATE=DISCONNECTED
<6>[ 2777.065929]  (7)[15638:kworker/7:1][connlog] irq counter=995 module=0x0001
<7>[ 2777.068712]  (3)[114:kworker/u16:1][FSTB]fstb_get_queue_fps  13308 0
<7>[ 2777.068775]  (3)[114:kworker/u16:1]FPSGO_COMPfpsgo_ctrl2comp_enqueue_start xgf_ret:3
<7>[ 2777.068851]  (3)[114:kworker/u16:1]FPSGO_COMPfpsgo_ctrl2comp_enqueue_end xgf_ret:5
<5>[ 2777.068967]  (3)[114:kworker/u16:1][Power/PPM] (0xa0)(8683)(0)(0-7)(15)(14)(4)(4) (15)(8)(4)(4) 
<6>[ 2777.070844]  (7)[661:wificond][wlan][661]mtk_cfg80211_get_station:(REQ INFO) link speed=650, rssi=-36, BSSID:[c4:9f:4c:b3:3b:52], TxFail=0, TxTimeOut=0, TxOK=26578, RxOK=44049
<5>[ 2777.074272] -(5)[1004:kworker/u16:19][MUSB]do_idle_work 241: otg_state (null) to (null), is_active<0>
<5>[ 2777.076974]  (7)[374:init][MUSB]mt_usb_store_saving_mode 984: old=1 new=1
<6>[ 2777.083423]  (5)[374:init]gadget_dev_desc_UDC_store write musb-hdrc
<6>[ 2777.083466]  (5)[374:init]usb_gadget_probe_driver musb-hdrc musb-hdrc
<6>[ 2777.083478]  (5)[374:init]configfs_composite_bind
<6>[ 2777.083538]  (5)[374:init]configfs-gadget gadget: adding 'Function FS Gadget'/000000001d6099fa to config 'b'/000000002777d2e2
<6>[ 2777.083660]  (5)[374:init]configfs-gadget gadget: adding 'acm'/000000006cf508a2 to config 'b'/000000002777d2e2
<5>[ 2777.083687]  (5)[374:init][XLOG_INFO][USB_ACM]acm_bind: ttyGS0: dual speed IN/ep2in OUT/ep2out NOTIFY/ep3in
<5>[ 2777.083701]  (5)[374:init][MUSB]musb_gadget_start 2599: musb_gadget_start
<5>[ 2777.083814]  (5)[374:init][MUSB]musb_gadget_pullup 2382: is_on=1, softconnect=0 ++
<5>[ 2777.083827] -(5)[374:init][MUSB]musb_gadget_pullup 2395: is_on=1, softconnect=0 ++
<5>[ 2777.083839] -(5)[374:init][MUSB]musb_pullup 2325: MUSB: gadget pull up 1 start, musb->power:1
<5>[ 2777.083850] -(5)[374:init][MUSB]musb_pullup 2334: MUSB: gadget pull up 1 end
<5>[ 2777.086159]  (3)[246:kworker/3:2][Power/PPM] (0xa0)(14332)(0)(0-7)(15)(0)(4)(4) (15)(0)(4)(4) 
<6>[ 2777.160080]  (6)[3739:hif_thread][wlan][3739]halSetFWOwn:(INIT INFO) FW OWN:1
<5>[ 2777.175371]  (6)[252:chgdet_thread][MUSB]Charger_Detect_Init 798: Charger_Detect_Init
<5>[ 2777.351998]  (5)[252:chgdet_thread][MUSB]Charger_Detect_Release 818: Charger_Detect_Release
<6>[ 2777.352051]  (5)[252:chgdet_thread]charger type: 1, Standard USB Host
<6>[ 2777.352076]  (5)[252:chgdet_thread]charger type: chrdet_inform_psy_changed: online = 1, type = 1
<6>[ 2777.352101]  (5)[252:chgdet_thread]mt_charger_set_property
<6>[ 2777.352120]  (5)[252:chgdet_thread]mt_charger_set_property
<6>[ 2777.352162]  (5)[252:chgdet_thread]dump_charger_name: charger type: 1, Standard USB Host
<5>[ 2777.352192]  (5)[252:chgdet_thread][MUSB]mt_usb_connect 679: [MUSB] USB connect
<5>[ 2777.352220]  (5)[252:chgdet_thread][MUSB]issue_connection_work 673: issue work, ops<2>
<5>[ 2777.352409]  (7)[1004:kworker/u16:19][MUSB]do_connection_work 578: is_host<0>, power<1>, ops<2>
<5>[ 2777.352456]  (7)[1004:kworker/u16:19][MUSB]usb_cable_connected 545: connected=1 vbus_exist=1 type=1
<5>[ 2777.352493]  (7)[1004:kworker/u16:19][MUSB]cmode_effect_on 565: cable_mode=1, effect=0
<5>[ 2777.352520] -(7)[1004:kworker/u16:19][MUSB]do_connection_work 639: do nothing, usb_on:1, power:1
<5>[ 2777.352557]  (7)[1004:kworker/u16:19]mtk_charger_int_handler
<5>[ 2777.352591]  (7)[1004:kworker/u16:19]battery_callback:1
<5>[ 2777.353302]  (7)[1004:kworker/u16:19][fg_sw_bat_cycle_accu]car[o:0 n:-16],diff_car:-16,ncar[o:1412 n:1428 hw:0] thr 31061
<6>[ 2777.355515]  (7)[1004:kworker/u16:19]mt635x-auxadc mt-pmic:mt635x-auxadc: name:ISENSE, channel=0, adc_out=0x656d, adc_result=4278
<5>[ 2777.355805]  (7)[1004:kworker/u16:19][CH3_DBG] bat_cur = -875
<12>[ 2777.356009]  (6)[528:health@2.0-serv]healthd: battery l=100 v=4261 t=29.7 h=2 st=2 c=-74 fc=3013000 cc=0 chg=u
<5>[ 2777.356770] -(6)[528:health@2.0-serv]alarmtimer_enqueue, 2837353675164
<6>[ 2777.356815]  (5)[1004:kworker/u16:19]mt635x-auxadc mt-pmic:mt635x-auxadc: name:BAT_TEMP, channel=3, adc_out=0x54f, adc_result=597
<5>[ 2777.358163]  (5)[1004:kworker/u16:19]wake_up_charger
<6>[ 2777.360336]  (4)[61:pd_dbg_info]///PD dbg info 126d
<4>[ 2777.360388]  (4)[61:pd_dbg_info]< 2777.358>TCPC-TCPC:bat_update_work_func battery update soc = 100
<4>[ 2777.360388] < 2777.358>TCPC-TCPC:bat_update_work_func Battery Charging
<12>[ 2777.361338]  (6)[528:health@2.0-serv]healthd: battery l=100 v=4278 t=29.7 h=2 st=2 c=-97 fc=3013000 cc=0 chg=u
<6>[ 2777.361612]  (5)[306:charger_thread]mt635x-auxadc mt-pmic:mt635x-auxadc: name:ISENSE, channel=0, adc_out=0x6560, adc_result=4276
<6>[ 2777.363318]  (5)[306:charger_thread]mt635x-auxadc mt-pmic:mt635x-auxadc: name:VCDT, channel=2, adc_out=0x4c6, adc_result=537
<5>[ 2777.363682]  (5)[306:charger_thread][CH3_DBG] bat_cur = -1186
<6>[ 2777.364219]  (5)[306:charger_thread]mt635x-auxadc mt-pmic:mt635x-auxadc: name:BAT_TEMP, channel=3, adc_out=0x54e, adc_result=596
<12>[ 2777.365464]  (6)[528:health@2.0-serv]healthd: battery l=100 v=4278 t=29.7 h=2 st=2 c=-118 fc=3013000 cc=0 chg=u
<5>[ 2777.388508]  (5)[306:charger_thread]Vbat=4276,Ibat=-1056,I=0,VChr=5080,T=29,Soc=100:100,CT:1:0 hv:1 pd:0:0
<5>[ 2777.388561]  (5)[306:charger_thread]mtk_is_charger_on plug in, type:1
<5>[ 2777.389192]  (4)[559:fuelgauged][CH3_DBG] bat_cur = -1948
<5>[ 2777.390664]  (6)[559:fuelgauged]MTK_FG: [FGADC_info] tmp:29 29 31 rdnafg:0 vc:1 disable_fg:0:0 fg_v:3:9997:43830:-471:31061:154:9846:9846 low_temp:0 0 0
<5>[ 2777.390846]  (6)[559:fuelgauged]MTK_FG: [FGADC_intr_end][FG_INTR_CHARGER_IN]soc:9998 fg_c_soc:9998 fg_v_soc:9846 ui_soc:10000 vc_diff:152 vc_mode 1 VBAT 42730 T:[29 V 29 C 29 avg:29] D0_C 10000 D0_V 9997 CAR[c:-9 v:-471] Q:[31061 31061 31061 31061] aging 10000 bat_cycle 0 Trk[0(-186):0:0] UI[1:1] Chr[0:10000:9477] pseudo1 0  DC_ratio 100 dodinit[3][0],ag[0 0 0 1 0 0]I:-780
<5>[ 2777.394607]  (7)[559:fuelgauged][CH3_DBG] bat_cur = -1548
<6>[ 2777.397259]  (4)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_plug_in
<6>[ 2777.397337]  (4)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_enable_wdt: en = 1
<5>[ 2777.401381] -(7)[559:fuelgauged]mtk_rtc_hal_common: hal_rtc_get_spare_register: cmd[0], get rg[0x5aa, 0xff , 8] = 0xe4
<5>[ 2777.401461] -(7)[559:fuelgauged]mtk_rtc_hal_common: hal_rtc_set_spare_register: cmd[0], set rg[0x5aa, 0xff , 8] = 0xe4
<5>[ 2777.401728]  (7)[559:fuelgauged][fg_res] FG_DAEMON_CMD_SET_CON0_SOC = 10048
<5>[ 2777.403910]  (7)[559:fuelgauged][MUSB]usb20_check_vbus_on 137: vbus_on<0>
<7>[ 2777.404151] -(4)[534:vibrator@1.0-se][vibrator]cancel hrtimer, cust:25ms, value:640, shutdown:0
<5>[ 2777.404569]  (5)[306:charger_thread]mtk_charger_start_timer: alarm timer start:0, 2787 401468010
<5>[ 2777.404621] -(5)[306:charger_thread]alarmtimer_enqueue, 2787401468010
<5>[ 2777.404940]  (5)[306:charger_thread][CH3_DBG] bat_cur = 2561
<12>[ 2777.405504]  (6)[528:health@2.0-serv]healthd: battery l=100 v=4262 t=29.4 h=2 st=2 c=256 fc=3013000 cc=0 chg=u
<5>[ 2777.405922]  (7)[559:fuelgauged]get_shutdown_cond ret:0 0 0 0 vbat:4349
<6>[ 2777.406724]  (6)[61:pd_dbg_info]///PD dbg info 126d
<4>[ 2777.406773]  (6)[61:pd_dbg_info]< 2777.400>TCPC-TCPC:bat_update_work_func battery update soc = 100
<4>[ 2777.406773] < 2777.401>TCPC-TCPC:bat_update_work_func Battery Charging
<5>[ 2777.407885]  (5)[306:charger_thread][CH3_DBG] bat_cur = 2472
<6>[ 2777.411324]  (5)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: __mt6370_set_mivr: mivr = 4500000 (0x06)
<5>[ 2777.415648]  (5)[306:charger_thread]check_dynamic_mivr vbat = 4350 
<6>[ 2777.439293]  (5)[15974:kworker/5:1]mt6370_pmu_charger mt6370_pmu_charger: mt6370_enable_irq: (chg_mivr) en = 1
<7>[ 2777.440676] -(5)[15974:kworker/5:1]mt6370_pmu 5-0034: mt6370_pmu_irq_enable: hwirq = 6, chg_mivr
<7>[ 2777.442206] -(7)[534:vibrator@1.0-se][vibrator]cancel hrtimer, cust:25ms, value:640, shutdown:0
<7>[ 2777.443037]  (7)[12308:kworker/u16:3]FPSGO_COMPfpsgo_ctrl2comp_enqueue_start xgf_ret:3
<7>[ 2777.444850]  (7)[12308:kworker/u16:3]FPSGO_COMPfpsgo_ctrl2comp_enqueue_end xgf_ret:5
<5>[ 2777.454226] -(6)[1004:kworker/u16:19][MUSB]musb_stage0_irq 1208: musb_stage0_irq:1208 MUSB_INTR_RESET (b_idle)
<5>[ 2777.454271] -(6)[1004:kworker/u16:19]QMU_WARN,<musb_disable_q_all 333>, disable_q_all
<5>[ 2777.454288] -(6)[1004:kworker/u16:19]QMU_WARN,<mtk_qmu_disable 847>, disable RQ(1)
<5>[ 2777.454329] -(6)[1004:kworker/u16:19]QMU_WARN,<mtk_qmu_disable 847>, disable RQ(2)
<5>[ 2777.454354] -(6)[1004:kworker/u16:19]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(1)
<5>[ 2777.454395] -(6)[1004:kworker/u16:19]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(2)
<5>[ 2777.454417] -(6)[1004:kworker/u16:19]QMU_WARN,<mtk_qmu_disable 847>, disable TQ(3)
<5>[ 2777.454444] -(6)[1004:kworker/u16:19]BATTERY_SetUSBState Success! Set 1
<6>[ 2777.454458] -(6)[1004:kworker/u16:19]android_disconnect
<6>[ 2777.454776]  (6)[14509:kworker/6:1]android_work: did not send uevent (0 0           (null))
<5>[ 2777.456575]  (7)[1004:kworker/u16:19][Power/PPM] (0xa0)(8684)(0)(0-7)(15)(14)(4)(4) (15)(8)(4)(4) 
<5>[ 2777.473505]  (7)[15638:kworker/7:1][Power/PPM] (0xa0)(9020)(0)(0-7)(15)(0)(4)(4) (15)(0)(4)(4) 
<5>[ 2777.477504]  (5)[114:kworker/u16:1][Power/PPM] (0xa0)(9126)(0)(0-7)(15)(13)(4)(4) (15)(8)(4)(4) 
<6>[ 2777.477718]  (4)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_get_tchg: tchg = 30
<5>[ 2777.479187]  (4)[306:charger_thread]tmp:29 (jeita:0 sm:0 cv:0 en:0) (sm:1) en:1 c:0 s:0 ov:0 1 1
<5>[ 2777.479214]  (4)[306:charger_thread]mtk_switch_charging_run [1 0], timer=0
<5>[ 2777.479654]  (4)[306:charger_thread][CH3_DBG] bat_cur = 1291
<5>[ 2777.486827]  (7)[12308:kworker/u16:3][Power/PPM] (0xa0)(9319)(0)(0-7)(15)(14)(4)(4) (15)(8)(4)(4) 
<5>[ 2777.504437]  (7)[15638:kworker/7:1][Power/PPM] (0xa0)(14526)(0)(0-7)(15)(0)(4)(4) (15)(0)(4)(4) 
<6>[ 2777.528390]  (4)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_get_ibus: ibus = 450mA
<5>[ 2777.528439]  (4)[306:charger_thread]pe40_ready:0 hv:1 thermal:-1,-1 tmp:29,39,16 pps:0 en:0 ibus:0 80
<5>[ 2777.528602]  (6)[306:charger_thread] charger_dev_run_aicl input_current_limit_by_aicl = -1
<5>[ 2777.528641]  (6)[306:charger_thread]force:0 thermal:-1,-1 pe4:-1,-1,0 setting:500 500 type:1 usb_unlimited:0 usbif:0 usbsm:1 aicl:-1 atm:0 ichg1_min:300
<6>[ 2777.529669]  (4)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: __mt6370_set_cv: bat voreg = 4350000 (0x2D)
<6>[ 2777.541709]  (4)[15102:kworker/4:1]android_work: sent uevent USB_STATE=CONNECTED
<6>[ 2777.562269] -(5)[961:OomAdjuster]configfs-gadget gadget: high-speed config #1: b
<5>[ 2777.562362] -(5)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2777.562382] -(5)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 512, epnum 1,hwepnum 1
<5>[ 2777.562395] -(5)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 631>, enable RQ(1)
<5>[ 2777.562414] -(5)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep1out for bulk OUT, maxpacket 512
<5>[ 2777.562433] -(5)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2777.562445] -(5)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 1024, epnum 1,hwepnum 1
<5>[ 2777.562457] -(5)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(1)
<5>[ 2777.562475] -(5)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep1in for bulk IN, maxpacket 512
<5>[ 2777.562535] -(5)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=INT
<5>[ 2777.562550] -(5)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 1536, epnum 3,hwepnum 3
<5>[ 2777.562561] -(5)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(3)
<5>[ 2777.562579] -(5)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep3in for int IN, maxpacket 10
<5>[ 2777.562596] -(5)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2777.562609] -(5)[961:OomAdjuster][MUSB]check_musb_dbuffer_avail 1299: <check_musb_dbuffer_avail, 1299>, got bulk ep:82 in function :acm
<5>[ 2777.562620] -(5)[961:OomAdjuster][MUSB]is_saving_mode 993: 1
<5>[ 2777.562631] -(5)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=Function FS Gadget
<5>[ 2777.562640] -(5)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=acm
<5>[ 2777.562651] -(5)[961:OomAdjuster][MUSB]is_db_ok 1188: acm IN desc-addr=82, addr=82
<5>[ 2777.562663] -(5)[961:OomAdjuster][MUSB]is_db_ok 1202: [acm] EP2-IN as double buffer
<5>[ 2777.562673] -(5)[961:OomAdjuster][MUSB]fifo_setup 1373: Saving mode, but EP2 supports DBBUF
<5>[ 2777.562685] -(5)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 22 after 512, fifo address is 2048, epnum 2,hwepnum 2
<5>[ 2777.562696] -(5)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 709>, enable TQ(2)
<5>[ 2777.562714] -(5)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep2in for bulk IN, maxpacket 512
<5>[ 2777.562726] -(5)[961:OomAdjuster][MUSB]fifo_setup 1347: musb type=BULK
<5>[ 2777.562738] -(5)[961:OomAdjuster][MUSB]check_musb_dbuffer_avail 1299: <check_musb_dbuffer_avail, 1299>, got bulk ep:2 in function :acm
<5>[ 2777.562748] -(5)[961:OomAdjuster][MUSB]is_saving_mode 993: 1
<5>[ 2777.562758] -(5)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=Function FS Gadget
<5>[ 2777.562767] -(5)[961:OomAdjuster][MUSB]is_db_ok 1144: Ifc name=acm
<5>[ 2777.562778] -(5)[961:OomAdjuster][MUSB]is_db_ok 1188: acm OUT desc-addr=2, addr=2
<5>[ 2777.562789] -(5)[961:OomAdjuster][MUSB]is_db_ok 1198: [acm] EP2-OUT as signle buffer
<5>[ 2777.562801] -(5)[961:OomAdjuster][MUSB]fifo_setup 1393: fifo size is 6 after 512, fifo address is 3072, epnum 2,hwepnum 2
<5>[ 2777.562812] -(5)[961:OomAdjuster]QMU_WARN,<mtk_qmu_enable 631>, enable RQ(2)
<5>[ 2777.562828] -(5)[961:OomAdjuster][MUSB]musb_gadget_enable 1596: musb-hdrc periph: enabled ep2out for bulk OUT, maxpacket 512
<5>[ 2777.562878] -(5)[961:OomAdjuster]BATTERY_SetUSBState Success! Set 2
<6>[ 2777.564575]  (5)[15974:kworker/5:1]android_work: sent uevent USB_STATE=CONFIGURED
<5>[ 2777.569632] -(6)[950:android.ui][MUSB]service_zero_data_request 339: no more req, clr RXPKTRDY to avoid err RX FIFO/DMA read!! csr:0x2000
<5>[ 2777.613202]  (7)[1004:kworker/u16:19][Power/PPM] (0xa0)(10954)(0)(0-7)(15)(12)(4)(4) (15)(6)(4)(4) 
<5>[ 2777.633825]  (7)[15638:kworker/7:1][Power/PPM] (0xa0)(13556)(0)(0-7)(15)(0)(4)(4) (15)(0)(4)(4) 
<7>[ 2777.677784]  
<7>[ 2777.679054]  
<6>[ 2777.765166]  (7)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_dump_register: ICHG = 500mA, AICR = 500mA, MIVR = 4500mV, IEOC = 150mA, CV = 4350mV
<6>[ 2777.765208]  (7)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_dump_register: VSYS = 4345mV, VBAT = 4325mV, IBAT = 80mA, IBUS = 450mA, VBUS = 4900mV
<6>[ 2777.765224]  (7)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_dump_register: CHG_EN = 1, CHG_STATUS = progress, CHG_STAT = 0xA0
<6>[ 2777.765239]  (7)[306:charger_thread]mt6370_pmu_charger mt6370_pmu_charger: mt6370_dump_register: CHG_CTRL1 = 0x10, CHG_CTRL2 = 0x1B
```
