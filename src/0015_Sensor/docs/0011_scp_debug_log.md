# scp debug log

打印更多的scp调试log，注意CFG_OVERLAY_INIT_SUPPORT

**Debuglogger UI中的scp log可能开机等一段时间才有，譬如两分钟**

# android.mk BUILD_TYPE

vendor/mediatek/proprietary/tinysys/freertos/source/Android.mk

```makefile
TINYSYS_SCP_BUILD_CMD := \
    PROJECT=$(TINYSYS_SCP_PROJECT) \
    TARGET_BOARD_PLATFORM=$(TARGET_BOARD_PLATFORM) \
    O=$(abspath $(TINYSYS_SCP_BUILT_INTERMEDIATES)) \
    $(if $(filter showcommands,$(MAKECMDGOALS)),V=1) \
    BUILD_TYPE=$(if $(filter-out user,$(TARGET_BUILD_VARIANT)),debug,release) \
    ROOT_DIR=$$(pwd) \
    -C $(LOCAL_PATH)
```

# cm4 TINYSYS_DEBUG_BUILD

vendor/mediatek/proprietary/tinysys/freertos/source/build/env_cm4.mk

```makefile
ifeq (1,$(V))
  $(info $(TINYSYS_SCP): BUILD_TYPE=$(BUILD_TYPE))
endif

ifeq (debug,$(strip $(BUILD_TYPE)))
  CFLAGS += -DTINYSYS_DEBUG_BUILD
endif
```

# DEBUGLEVEL

vendor/mediatek/proprietary/tinysys/freertos/source/project/CM4_A/mt6765/platform/inc/FreeRTOSConfig.h

```C
#ifdef TINYSYS_DEBUG_BUILD
#define DEBUGLEVEL 3
#else
#define DEBUGLEVEL 1
#endif
```

# PRINTF

```C
/******************************************************************************
******************************************************************************/
#ifndef CFG_LOG_FILTER
/* DEBUG LEVEL definition*/
#define LOG_DEBUG       3
#define LOG_INFO        2
#define LOG_WARN        1
#define LOG_ERROR       0
#define PRINTF(x...)    PRINTF_D(x)

#define PRINTF_D(x...)            \
({                                \
    if (LOG_DEBUG <= DEBUGLEVEL)  \
        printf(x);                \
})

#define PRINTF_I(x...)            \
({                                \
    if (LOG_INFO <= DEBUGLEVEL)   \
        printf(x);                \
})

#define PRINTF_W(x...)            \
({                                \
    if (LOG_WARN <= DEBUGLEVEL)   \
        printf(x);                \
})


#define PRINTF_E(x...)            \
({                                \
    if (LOG_ERROR <= DEBUGLEVEL)  \
        printf(x);                \
})

#define PRINTF_ONCE(x...)                                       \
({                                                              \
    static char __print_once;                                   \
                                                                \
    if (!__print_once) {                                        \
        __print_once = 1;                                       \
        printf(x);                                              \
    }                                                           \
})
```

# last log

cat /sys/class/misc/scp/scp_A_get_last_log
