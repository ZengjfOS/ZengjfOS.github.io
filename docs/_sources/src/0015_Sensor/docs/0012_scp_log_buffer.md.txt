# scp log buffer

修改scp log buffer，MTK debuglogger UI抓log要等一段时间，如果log太多会被覆盖，注意裁减log

# last log

* cat /sys/class/misc/scp/scp_A_get_last_log
* adb wait-for-device  && adb root && adb shell "while true; do cat /sys/class/misc/scp/scp_A_get_last_log; sleep 1; done"

# scp

```diff
diff --git a/mediatek/proprietary/tinysys/freertos/source/drivers/common/logger/v01/src/scp_logger.c b/mediatek/proprietary/tinysys/freertos/source/drivers/common/logger/v01/src/scp_logger.c
index 266039a09..4853d2086 100644
--- a/mediatek/proprietary/tinysys/freertos/source/drivers/common/logger/v01/src/scp_logger.c
+++ b/mediatek/proprietary/tinysys/freertos/source/drivers/common/logger/v01/src/scp_logger.c
@@ -56,7 +56,7 @@
 
 #define SHARESEC __attribute__ ((section (".share")))
 #define PLT_LOG_ENABLE      0x504C5402 /*magic*/
-#define BUF_LEN             1024       /*1KB*/
+#define BUF_LEN             (1024 * 20)       /*1KB*/
 #define DRAM_BUF_LEN        0x200000   /*2MB*/
 #define LOGGER_MAX_QUEUE    2          /*maximum timer queue number*/
```

# kernel

```diff
diff --git a/drivers/misc/mediatek/scp/cm4/v01/scp_logger.c b/drivers/misc/mediatek/scp/cm4/v01/scp_logger.c
index a5be682a2..ac506e551 100644
--- a/drivers/misc/mediatek/scp/cm4/v01/scp_logger.c
+++ b/drivers/misc/mediatek/scp/cm4/v01/scp_logger.c
@@ -77,7 +77,7 @@ static DEFINE_SPINLOCK(scp_A_log_buf_spinlock);
 static struct scp_work_struct scp_logger_notify_work[SCP_CORE_TOTAL];
 
 /*scp last log info*/
-#define LAST_LOG_BUF_SIZE  4095
+#define LAST_LOG_BUF_SIZE  8192
 static struct SCP_LOG_INFO last_log_info;
 
 static char *scp_A_last_log;
```
