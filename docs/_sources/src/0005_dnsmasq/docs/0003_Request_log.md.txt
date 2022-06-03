# Request log

log中显示请求、结果信息，方便查看信息

# 示例

* 输出每次查询加参数`-q`
  ```
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: started, version 2.51 cachesize 150
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: compile time options: IPv6 GNU-getopt no-DBus no-I18N DHCP TFTP
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: read /etc/hosts - 5 addresses
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: using nameserver 172.20.10.1#53
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: using nameserver 8.8.8.8#53
  Nov 24 07:26:24 raspberrypi dnsmasq[5523]: start for loop
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: start for loop
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter receive_query()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter extract_request()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: daemon->namebuff: baidu.com
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: query[A] baidu.com from 127.0.0.1
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter answer_request()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter extract_request()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter forward_query()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: enter search_servers()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: exit search_servers()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: forwarded baidu.com to 8.8.8.8
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: forwarded baidu.com to 172.20.10.1
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: exit forward_query()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: exit receive_query()
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: reply baidu.com is 220.181.38.251
  Nov 24 07:26:36 raspberrypi dnsmasq[5523]: reply baidu.com is 220.181.38.148
  ```
* sudo src/dnsmasq --keep-in-foreground --no-poll --dhcp-authoritative  --pid-file -C dnsmasq.conf.example -r /run/dnsmasq/resolv.conf -q
