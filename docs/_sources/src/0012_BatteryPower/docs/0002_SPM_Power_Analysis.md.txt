# SPM Power Analysis

System Power Manager功耗分析

# 参考文档

* [0001_Deep_Sleep.md](0001_Deep_Sleep.md)

# 休眠唤醒log

* 如下log中包含：
  * CPU进入休眠的log；
  * CPU被R12_CLDMA_EVENT_B唤醒的log；
    * `<6>[  462.081720] -(0)[3082:Binder:467_2][SPM] suspend wake up by  R12_CLDMA_EVENT_B, timer_out = 7, r13 = 0x604010c, debug_flag = 0x11000 0x0, r12 = 0x4000000, r12_ext = 0x0, raw_sta = 0x0, idle_sta = 0x97f,  req_sta =  0x420000a0, event_reg = 0x30000000, isr = 0x0, raw_ext_sta = 0x4006a095, wake_misc = 0x0, pcm_flag = 0x80080 0x40, req = 0x0, wlk_cntcv_l = 0xb6d0676b, wlk_cntcv_h = 0x2, 26M_off_pct = 0`
* 根据这一段log，可以理解CPU休眠唤醒的基本流程
  ```
  <5>[  461.706933] -(4)[3082:Binder:467_2][MUSB]musb_hub_control 379: port status 00000100,devctl=0x80
  <6>[  461.707555]  (4)[3082:Binder:467_2][mt_udi] UDI suspend
  <5>[  461.709989]  (4)[3082:Binder:467_2]alarmtimer_suspend convert 921861000000 to 2021/02/08 08:16:51 (now = 2021/02/08 08:16:21)
  <5>[  461.713357]  (4)[3082:Binder:467_2]mtk_rtc_common: set al time = 2021/02/08 08:16:52 (1)
  <5>[  461.713548] -(4)[3082:Binder:467_2]mtk_rtc_hal_common: mon = 48130, day = 20488, hour = 16392
  <5>[  461.713907] -(4)[3082:Binder:467_2]mtk_rtc_hal_common: mon = 48130, day = 20488, hour = 16392
  <4>[  461.714811]  (4)[3082:Binder:467_2]<blestech_fp>[bf_suspend:1374]  ++
  <4>[  461.714811] 
  <4>[  461.714857]  (4)[3082:Binder:467_2]<blestech_fp>[bf_suspend:1379]
  <4>[  461.714857] 
  <6>[  461.716069]  (4)[3082:Binder:467_2][ISP][ISP_suspend] cam2 - X. UserCount=0,wakelock:0,devct:4
  <5>[  461.717104]  (4)[3082:Binder:467_2][Thermal/TZ/CPU]tscpu_thermal_suspend
  <5>[  461.717795]  (4)[3082:Binder:467_2][CMDQ]cmdq_suspend ignore
  <5>[  461.717841]  (4)[3082:Binder:467_2][CMDQ]cmdq_core_suspend usage:0 exec thread:0x0
  <5>[  461.718419]  (4)[3082:Binder:467_2]******** battery_suspend!! iavg=0 ***GM3 disable:0 0 0 0 tmp_intr:0***
  <5>[  461.718458]  (4)[3082:Binder:467_2][enable_bat_temp_det] smart reset not support!
  <5>[  461.719402]  (4)[3082:Binder:467_2][Power/PPM] ppm_main_suspend: suspend callback in
  <6>[  461.720037]  (4)[3082:Binder:467_2]PM: suspend of devices complete after 77.927 msecs
  <6>[  461.727342]  (4)[3082:Binder:467_2]PM: late suspend of devices complete after 7.246 msecs
  <6>[  461.734757]  (4)[3082:Binder:467_2]PM: noirq suspend of devices complete after 7.345 msecs
  <6>[  461.734815]  (4)[3082:Binder:467_2]Disabling non-boot CPUs ...
  <5>[  461.761689]  (4)[3082:Binder:467_2]CPU1: shutdown
  <6>[  461.779081]  (4)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  461.779134]  (4)[3082:Binder:467_2]psci: CPU1 killed.
  <5>[  461.805312]  (4)[3082:Binder:467_2]CPU2: shutdown
  <6>[  461.823074]  (4)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  461.823127]  (4)[3082:Binder:467_2]psci: CPU2 killed.
  <5>[  461.849108]  (7)[3082:Binder:467_2]CPU3: shutdown
  <6>[  461.867092]  (7)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  461.867144]  (7)[3082:Binder:467_2]psci: CPU3 killed.
  <5>[  461.903527]  (7)[3082:Binder:467_2]CPU4: shutdown
  <6>[  461.923087]  (7)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  461.923138]  (7)[3082:Binder:467_2]psci: CPU4 killed.
  <5>[  461.966736]  (7)[3082:Binder:467_2]CPU5: shutdown
  <6>[  461.983148]  (6)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  461.983206]  (6)[3082:Binder:467_2]psci: CPU5 killed.
  <5>[  462.018208]  (7)[3082:Binder:467_2]CPU6: shutdown
  <6>[  462.035222]  (7)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  462.035272]  (7)[3082:Binder:467_2]psci: CPU6 killed.
  <5>[  462.062272]  (0)[3082:Binder:467_2]CPU7: shutdown
  <6>[  462.078962]  (0)[3082:Binder:467_2]psci: Retrying again to check for CPU kill
  <6>[  462.078975]  (0)[3082:Binder:467_2]psci: CPU7 killed.
  <5>[  462.081720] -(0)[3082:Binder:467_2][clkchk] unexpected unclosed MTCMOS: pg_conn 
  <6>[  462.081720] -(0)[3082:Binder:467_2]NO spm_get_is_infra_pdn !!!
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM-PMIC] [dlpt_R] pre_SOC=60 SOC=60 skip
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM] sec = 4800, wakesrc = 0xe87ddef (1)(1)
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM] wlk_cntcv_l = 0xb6d005ea, wlk_cntcv_h = 0x2
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM] md_settle = 99, settle = 99
  <6>[  462.081720] -(0)[3082:Binder:467_2]restore UART register start!
  <6>[  462.081720] -(0)[3082:Binder:467_2]restore UART register finish!
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM] suspend wake up by  R12_CLDMA_EVENT_B, timer_out = 7, r13 = 0x604010c, debug_flag = 0x11000 0x0, r12 = 0x4000000, r12_ext = 0x0, raw_sta = 0x0, idle_sta = 0x97f,  req_sta =  0x420000a0, event_reg = 0x30000000, isr = 0x0, raw_ext_sta = 0x4006a095, wake_misc = 0x0, pcm_flag = 0x80080 0x40, req = 0x0, wlk_cntcv_l = 0xb6d0676b, wlk_cntcv_h = 0x2, 26M_off_pct = 0
  <6>[  462.081720] -(0)[3082:Binder:467_2][SPM] dormant = 7, s_ddr = 0, s_vcore = 0, 
  <6>[  462.081720] -(0)[3082:Binder:467_2]ddr = 0, vcore = 0, sleep_count = 82
  <5>[  462.081720] -(0)[3082:Binder:467_2][ccci1/cif] CCIF wakeup channel: 0x0
  <6>[  462.081720] -(0)[3082:Binder:467_2]Resume caused by IRQ 179, SPM
  <6>[  462.081720] -(0)[3082:Binder:467_2]Suspended for 0.002 seconds
  <6>[  462.081739] -(0)[3082:Binder:467_2][ccci1/mcd]Resume cldma pdn register: No need  ...
  <6>[  462.081756] -(0)[3082:Binder:467_2][ccci1/mcd]Resume cldma ao register: No need  ...
  <6>[  462.081878]  (0)[3082:Binder:467_2]Enabling non-boot CPUs ...
  <6>[  462.083162] -(1)[0:swapper/1]Detected VIPT I-cache on CPU1
  <6>[  462.083199] -(1)[0:swapper/1]GICv3: CPU1: found redistributor 1 region 0:0x000000000c120000
  <6>[  462.083248] -(1)[0:swapper/1]CPU1: update cpu_capacity 1024
  <6>[  462.083253] -(1)[0:swapper/1]CPU1: Booted secondary processor [410fd034]
  <6>[  462.084215]  (0)[3082:Binder:467_2]CPU1 is up
  <6>[  462.085533] -(2)[0:swapper/2]Detected VIPT I-cache on CPU2
  <6>[  462.085558] -(2)[0:swapper/2]GICv3: CPU2: found redistributor 2 region 0:0x000000000c140000
  <6>[  462.085585] -(2)[0:swapper/2]CPU2: update cpu_capacity 1024
  <6>[  462.085590] -(2)[0:swapper/2]CPU2: Booted secondary processor [410fd034]
  <6>[  462.086495]  (0)[3082:Binder:467_2]CPU2 is up
  <6>[  462.087699] -(3)[0:swapper/3]Detected VIPT I-cache on CPU3
  <6>[  462.087726] -(3)[0:swapper/3]GICv3: CPU3: found redistributor 3 region 0:0x000000000c160000
  <6>[  462.087756] -(3)[0:swapper/3]CPU3: update cpu_capacity 1024
  <6>[  462.087760] -(3)[0:swapper/3]CPU3: Booted secondary processor [410fd034]
  <6>[  462.088882]  (0)[3082:Binder:467_2]CPU3 is up
  <6>[  462.090853] -(4)[0:swapper/4]Detected VIPT I-cache on CPU4
  <6>[  462.090946] -(4)[0:swapper/4]GICv3: CPU4: found redistributor 100 region 0:0x000000000c180000
  <6>[  462.091047] -(4)[0:swapper/4]CPU4: update cpu_capacity 853
  <6>[  462.091065] -(4)[0:swapper/4]CPU4: Booted secondary processor [410fd034]
  <6>[  462.092387]  (4)[28:cpuhp/4][Power/cpufreq] 7,0,32,0,833,833,833,833
  <6>[  462.096591]  (4)[3082:Binder:467_2]CPU4 is up
  <6>[  462.098975] -(5)[0:swapper/5]Detected VIPT I-cache on CPU5
  <6>[  462.099058] -(5)[0:swapper/5]GICv3: CPU5: found redistributor 101 region 0:0x000000000c1a0000
  <6>[  462.099143] -(5)[0:swapper/5]CPU5: update cpu_capacity 853
  <6>[  462.099162] -(5)[0:swapper/5]CPU5: Booted secondary processor [410fd034]
  <6>[  462.104096]  (4)[3082:Binder:467_2]CPU5 is up
  <6>[  462.106327] -(6)[0:swapper/6]Detected VIPT I-cache on CPU6
  <6>[  462.106412] -(6)[0:swapper/6]GICv3: CPU6: found redistributor 102 region 0:0x000000000c1c0000
  <6>[  462.106502] -(6)[0:swapper/6]CPU6: update cpu_capacity 853
  <6>[  462.106521] -(6)[0:swapper/6]CPU6: Booted secondary processor [410fd034]
  <6>[  462.112080]  (4)[3082:Binder:467_2]CPU6 is up
  <6>[  462.114302] -(7)[0:swapper/7]Detected VIPT I-cache on CPU7
  <6>[  462.114389] -(7)[0:swapper/7]GICv3: CPU7: found redistributor 103 region 0:0x000000000c1e0000
  <6>[  462.114485] -(7)[0:swapper/7]CPU7: update cpu_capacity 853
  <6>[  462.114503] -(7)[0:swapper/7]CPU7: Booted secondary processor [410fd034]
  <6>[  462.125331]  (4)[3082:Binder:467_2]CPU7 is up
  <4>[  462.128344] -(4)[3082:Binder:467_2]usb_6765_dpidle_request: 5 callbacks suppressed
  <5>[  462.128375] -(4)[3082:Binder:467_2][MUSB]usb_6765_dpidle_request 104: USB_DPIDLE_FORBIDDEN, skip_cnt<5>
  <4>[  462.128509] -(4)[3082:Binder:467_2]usb_6765_dpidle_request: 5 callbacks suppressed
  <5>[  462.128529] -(4)[3082:Binder:467_2][MUSB]usb_6765_dpidle_request 97: USB_DPIDLE_ALLOWED, skip_cnt<5>
  <6>[  462.130482]  (4)[3082:Binder:467_2]PM: noirq resume of devices complete after 4.604 msecs
  <6>[  462.131217] -(1)[0:swapper/1][ccci1/cldma]wake up by CLDMA_MD L2(11/0)(f000/18)!
  <6>[  462.136152]  (4)[3082:Binder:467_2]PM: early resume of devices complete after 4.576 msecs
  <5>[  462.136643]  (4)[3082:Binder:467_2][Power/PPM] ppm_main_resume: resume callback in
  <5>[  462.138213]  (4)[3082:Binder:467_2]******** battery_resume!! iavg=0 ***GM3 disable:0 0 0 0***
  <5>[  462.138259]  (4)[3082:Binder:467_2][enable_bat_temp_det] smart reset not support!
  <5>[  462.138619]  (4)[3082:Binder:467_2][CMDQ]cmdq_resume ignore
  <6>[  462.139075]  (7)[5021:kworker/u17:1][ccci1/cldma]CLDMA_AP wakeup source:(0/22)(54)
  <5>[  462.139384]  (4)[3082:Binder:467_2][Thermal/TZ/CPU]tscpu_thermal_resume
  <5>[  462.139703] -(2)[0:swapper/2][Thermal/TZ/CPU]Driver is ready to report valid temperatures
  <6>[  462.141978]  (4)[3082:Binder:467_2]vcodec_resume ok
  <6>[  462.142078]  (4)[3082:Binder:467_2][ISP][ISP_resume] cam2 - X. UserCount=0
  <4>[  462.142711]  (4)[3082:Binder:467_2]<blestech_fp>[bf_resume:1384]  ++
  <4>[  462.142711] 
  <4>[  462.142759]  (4)[3082:Binder:467_2]<blestech_fp>[bf_resume:1389]
  <4>[  462.142759] 
  <6>[  462.143470]  (4)[3082:Binder:467_2][mt_udi] UDI resume
  <5>[  462.143678] -(4)[3082:Binder:467_2][MUSB]musb_hub_control 379: port status 00000100,devctl=0x80
  ```
  * log中没有看到CPU0 shutdown的原因是logcat记录log的程序已经被冻结了，无法进路了，如果要看到，应该要用debug port看
