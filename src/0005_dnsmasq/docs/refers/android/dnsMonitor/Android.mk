LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE_TAGS := optional
LOCAL_MODULE := dnsMonitor
LOCAL_SRC_FILES := dnsMonitor.c
LOCAL_CFLAGS := -Wall -Werror -Wno-unused-parameter
LOCAL_SHARED_LIBRARIES := libc

include $(BUILD_EXECUTABLE)

include $(CLEAR_VARS)

LOCAL_MODULE_TAGS := optional
LOCAL_MODULE := spawn
LOCAL_SRC_FILES := spawn.cpp
LOCAL_CFLAGS := -Wall -Werror -Wno-unused-parameter
LOCAL_SHARED_LIBRARIES := libc

include $(BUILD_EXECUTABLE)
