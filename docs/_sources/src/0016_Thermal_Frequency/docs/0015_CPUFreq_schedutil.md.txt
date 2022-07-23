# schedutil

scheduler和调频建立起更加紧密的联系，同时提升了性能和功耗表现

# 参考文档

* [CPU调速器schedutil原理分析](https://deepinout.com/android-system-analysis/android-cpu-related/principle-analysis-of-cpu-governor-schedutil.html)

# CPU频率

* 最小频率：850MHz
* 最大频率：2001MHz
* CPU支持调频的策略
  ```
  conservative powersave performance schedutil
  ```
  * 目前采用schedutil
 