# hosts

dnsmasq会加载Android hosts文件

# log

输出log如下

```
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: started, version 2.51 cachesize 150
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: compile time options: IPv6 GNU-getopt no-DBus no-I18N DHCP TFTP
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: using nameserver 114.114.114.114#53 for domain sina.com
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: read /etc/hosts - 5 addresses
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: enter reload_servers()
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: fname: /run/dnsmasq/resolv.conf
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: exit reload_servers()
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: using nameserver 8.8.8.8#53
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: using nameserver 114.114.114.114#53 for domain sina.com
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: start check daemon->sfds
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: end check daemon->sfds
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: start check daemon->randomsocks
Dec  8 21:06:09 raspberrypi dnsmasq[1298]: end check daemon->randomsocks
```

* 关键log
  * `Dec  8 21:06:09 raspberrypi dnsmasq[1298]: read /etc/hosts - 5 addresses`
* /etc/hosts
  ```
  cat /etc/hosts
  127.0.0.1       localhost
  ::1             localhost ip6-localhost ip6-loopback
  ff02::1         ip6-allnodes
  ff02::2         ip6-allrouters
  
  127.0.1.1               raspberrypi
  ```
