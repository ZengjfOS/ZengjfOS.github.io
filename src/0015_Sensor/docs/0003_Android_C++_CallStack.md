# Android C++ CallStack

Android C++ backtrace

# 头文件

* #include <utils/CallStack.h>

# 使用

* android::CallStack stack;
* stack.update( );
* stack.log("XXX");

# lib

* 使用的时候添加依赖库：libutilscallstack
* system/core/libutils/Android.bp
  ```js
  cc_library {
      name: "libutilscallstack",
      defaults: ["libutils_defaults"],
  
      srcs: [
          "CallStack.cpp",
      ],
  
      arch: {
          mips: {
              cflags: ["-DALIGN_DOUBLE"],
          },
      },
  
      shared_libs: [
           "libutils",
           "libbacktrace",
      ],
  
      target: {
          linux: {
              srcs: [
                  "ProcessCallStack.cpp",
              ],
          },
          darwin: {
              enabled: false,
          },
          windows: {
              enabled: false,
          },
      },
  }
  ```
