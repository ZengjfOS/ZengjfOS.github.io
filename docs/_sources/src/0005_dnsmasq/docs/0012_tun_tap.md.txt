# tun tap

理解tun/tap网卡

# 参考文档

* [虚拟设备](https://xujiyou.work/Linux/%E7%BD%91%E7%BB%9C/Linux%E8%99%9A%E6%8B%9F%E7%BD%91%E7%BB%9C%E8%AE%BE%E5%A4%87%E4%B9%8Btun-tap.html)
* [How to open tap device on android using native code C?](https://stackoverflow.com/questions/24745398/how-to-open-tap-device-on-android-using-native-code-c)
* [simpletun.c](https://github.com/gregnietsky/simpletun/blob/master/simpletun.c)

# 示例源代码

* [README.md](refers/linux/spawn/README.md)
  * 用代码实现创建tun设备

# ip tuntap help

```
Usage: ip tuntap { add | del } [ dev PHYS_DEV ]
          [ mode { tun | tap } ] [ user USER ] [ group GROUP ]
          [ one_queue ] [ pi ] [ vnet_hdr ] [ multi_queue ]

Where: USER  := { STRING | NUMBER }
       GROUP := { STRING | NUMBER }
```

# 创建设备

创建 tap/tun 设备：

```
ip tuntap add dev tap0 mod tap # 创建 tap 
ip tuntap add dev tun0 mod tun # 创建 tun
```

删除 tap/tun 设备：

```
ip tuntap del dev tap0 mod tap # 删除 tap 
ip tuntap del dev tun0 mod tun # 删除 tun
```

# 测试

* sudo ip tuntap add dev tap0 mod tap
  * sudo ip tuntap del dev tap0 mod tap
* ifconfig tap0
  ```
  tap0      Link encap:Ethernet  HWaddr 72:9a:b3:35:89:57
            BROADCAST MULTICAST  MTU:1500  Metric:1
            RX packets:0 errors:0 dropped:0 overruns:0 frame:0
            TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
            collisions:0 txqueuelen:1000
            RX bytes:0 TX bytes:0
  ```
* sudo ip link set tap0 up
* sudo ip addr add 10.10.0.33/24 dev tap0
  * 不设置IP会报warning: `warning: interface tap0 does not currently exist`
    ```
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: started, version 2.51 cachesize 150
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: compile time options: IPv6 GNU-getopt no-DBus no-I18N DHCP TFTP
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: warning: interface tap0 does not currently exist
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: using nameserver 114.114.114.114#53 for domain sina.com
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: read /etc/hosts - 5 addresses
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: enter reload_servers()
    Dec  8 01:58:13 raspberrypi dnsmasq[1946]: fname: /run/dnsmasq/resolv.conf
    ```
* sudo src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -i tap0 -q
  * pidof dnsmasq | xargs sudo kill -9
* sudo iptables -t nat -A POSTROUTING -s tap0 -o wlan0 -j MASQUERADE
  * sudo iptables -t nat -L
    ```
    Chain PREROUTING (policy ACCEPT)
    target     prot opt source               destination
    DOCKER     all  --  anywhere             anywhere             ADDRTYPE match dst-type LOCAL
    
    Chain INPUT (policy ACCEPT)
    target     prot opt source               destination
    
    Chain POSTROUTING (policy ACCEPT)
    target     prot opt source               destination
    MASQUERADE  all  --  172.17.0.0/16        anywhere
    MASQUERADE  all  --  localhost            anywhere
    
    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination
    DOCKER     all  --  anywhere            !127.0.0.0/8          ADDRTYPE match dst-type LOCAL
    
    Chain DOCKER (2 references)
    target     prot opt source               destination
    RETURN     all  --  anywhere             anywhere
    ```
* tail -f /var/log/daemon.log
