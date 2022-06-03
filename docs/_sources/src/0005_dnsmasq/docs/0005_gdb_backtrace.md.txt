# gdb backtrace

通过gdb快速获取函数调用栈，加快代码运作分析

# suport gdb

```diff
diff --git a/dnsmasq-2.51/Makefile b/dnsmasq-2.51/Makefile
index 3d07c24..5ced535 100644
--- a/dnsmasq-2.51/Makefile
+++ b/dnsmasq-2.51/Makefile
@@ -38,7 +38,7 @@ all :   dnsmasq

 dnsmasq :
        @cd $(SRC) && $(MAKE) \
- DNSMASQ_CFLAGS="$(DNSMASQ_CFLAGS)" \
+ DNSMASQ_CFLAGS="$(DNSMASQ_CFLAGS) -g" \
  DNSMASQ_LIBS="$(DNSMASQ_LIBS) $(SUNOS_LIBS)" \
  -f ../bld/Makefile dnsmasq

```

# gdb获取backtrace

* gdb运行程序
  * set args: 设置gdb运行参数
  * break: 设置函数断点
  * r: 运行程序
  * c: 断点之后继续运行程序
  * backtrace: 函数栈
  * quit: 退出

```
pi@raspberrypi:dnsmasq-2.51 $ sudo gdb src/dnsmasq
GNU gdb (Raspbian 8.2.1-2) 8.2.1
Copyright (C) 2018 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "arm-linux-gnueabihf".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from src/dnsmasq...done.
(gdb) set args --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q
(gdb) break cache_insert
Breakpoint 1 at 0x1532c: file cache.c, line 384.
(gdb) r
Starting program: /home/pi/zengjf/dnsMonitor/dnsmasq-2.51/src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q

Breakpoint 1, cache_insert (name=name@entry=0x43150 "baidu.com", addr=addr@entry=0xbefff140, now=1637741386, now@entry=1, ttl=ttl@entry=322, flags=136, flags@entry=0) at cache.c:384
384       int freed_all = flags & F_REVERSE;
(gdb) backtrace
#0  cache_insert (name=name@entry=0x43150 "baidu.com", addr=addr@entry=0xbefff140, now=1637741386, now@entry=1, ttl=ttl@entry=322, flags=136, flags@entry=0) at cache.c:384
#1  0x00016b60 in extract_addresses (header=header@entry=0x43be0, qlen=qlen@entry=59, name=0x43150 "baidu.com", now=1, now@entry=1637741386) at rfc1035.c:815
#2  0x0001eb9c in process_reply (header=header@entry=0x43be0, now=now@entry=1637741386, server=server@entry=0x48518, n=n@entry=59) at forward.c:443
#3  0x0001fe8c in reply_query (fd=<optimized out>, family=<optimized out>, now=now@entry=1637741386) at forward.c:558
#4  0x000222a4 in check_dns_listeners (set=0xbefff304, set@entry=0xbefff2fc, now=now@entry=1637741386) at dnsmasq.c:1045
#5  0x00012694 in main (argc=<optimized out>, argv=<optimized out>) at dnsmasq.c:672
(gdb) c
Continuing.

Breakpoint 1, cache_insert (name=name@entry=0x43150 "baidu.com", addr=addr@entry=0xbefff140, now=1637741386, now@entry=1, ttl=ttl@entry=322, flags=136, flags@entry=0) at cache.c:384
384       int freed_all = flags & F_REVERSE;
(gdb) backtrace
#0  cache_insert (name=name@entry=0x43150 "baidu.com", addr=addr@entry=0xbefff140, now=1637741386,
    now@entry=1, ttl=ttl@entry=322, flags=136, flags@entry=0) at cache.c:384
#1  0x00016b60 in extract_addresses (header=header@entry=0x43be0, qlen=qlen@entry=59,
    name=0x43150 "baidu.com", now=1, now@entry=1637741386) at rfc1035.c:815
#2  0x0001eb9c in process_reply (header=header@entry=0x43be0, now=now@entry=1637741386,
    server=server@entry=0x48518, n=n@entry=59) at forward.c:443
#3  0x0001fe8c in reply_query (fd=<optimized out>, family=<optimized out>,
    now=now@entry=1637741386) at forward.c:558
#4  0x000222a4 in check_dns_listeners (set=0xbefff304, set@entry=0xbefff2fc,
    now=now@entry=1637741386) at dnsmasq.c:1045
#5  0x00012694 in main (argc=<optimized out>, argv=<optimized out>) at dnsmasq.c:672
(gdb) c
Continuing.
(gdb) quit
A debugging session is active.

        Inferior 1 [process 6723] will be killed.

Quit anyway? (y or n) y
```
