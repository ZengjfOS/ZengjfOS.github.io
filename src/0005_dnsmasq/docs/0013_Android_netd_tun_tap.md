# Android netd tun tap

netd创建tun tap网卡

# 参考文档

* [spawn.cpp](refers/android/dnsMonitor/spawn.cpp)

# netd SELinux

将参考的[spawn.cpp](refers/android/dnsMonitor/spawn.cpp)修改在netd中处理，netd SELinux策略禁止了访问tun节点生成tun网卡，由于是spawn出来的，发现修改netd SELinux策略无效

```
12-08 09:02:51.376000   766   766 W ip      : type=1400 audit(0.0:49): avc: denied { ioctl } for path="/dev/tun" dev="tmpfs" ino=18538 ioctlcmd=0x54cb scontext=u:r:netd:s0 tcontext=u:object_r:tun_device:s0 tclass=chr_file permissive=0
```

不过直接通过C代码[tap.c](refers/linux/spawn/tap.c)处理是可以的
