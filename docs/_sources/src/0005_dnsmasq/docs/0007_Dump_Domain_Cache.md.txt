# Dump Domain Cache

查询当前域名缓存

# dump cache

* 查询pid
  ```
  ps aux | grep dnsmasq
  pi        7311  0.2  0.0  12816  6548 pts/4    S+   08:29   0:03 vim dnsmasq.c
  root      7495  0.0  0.0  10584  3228 pts/3    S+   08:47   0:00 sudo src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q
  nobody    7496  0.0  0.0   2408   480 pts/3    S+   08:47   0:00 src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q
  pi        7521  0.0  0.0   7348   496 pts/7    S+   08:49   0:00 grep --color=auto dnsmasq
  ```
* sudo kill -s USR1 74951
  * pidof dnsmasq | xargs sudo kill -s USR1
* tail -f /var/log/daemon.log
  ```
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start check daemon->sfds
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: end check daemon->sfds
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start check daemon->randomsocks
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: end check daemon->randomsocks
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start for loop
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: time 1637744250
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: cache size 150, 0/2 cache insertions re-used unexpired cache entries.
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: queries forwarded 1, queries answered locally 1
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: server 8.8.8.8#53: queries sent 1, retried or failed 0
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: Host                                     Address                        Flags     Expires
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: ip6-loopback                             ::1                            6F I   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: ip6-allrouters                           ff02::2                        6FRI   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: baidu.com                                220.181.38.148                 4F        Wed Nov 24 09:05:13 2021
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: baidu.com                                220.181.38.251                 4F        Wed Nov 24 09:05:13 2021
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: ip6-allnodes                             ff02::1                        6FRI   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: raspberrypi                              127.0.1.1                      4FRI   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: localhost                                ::1                            6FRI   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: localhost                                127.0.0.1                      4FRI   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: ip6-localhost                            ::1                            6F I   H
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start check daemon->sfds
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: end check daemon->sfds
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start check daemon->randomsocks
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: end check daemon->randomsocks
  Nov 24 08:57:30 raspberrypi dnsmasq[7496]: start for loop
  ```
