# Whitelist Only

访问白名单

# 参考文档

* [0008_Whitelist_Blacklist.md](0008_Whitelist_Blacklist.md)
* [Dnsmasq Whitelist](http://www.intellamech.com/RaspberryPi-projects/dnsmasq_whitelist.html)

# set config

```diff
diff --git a/dnsmasq-2.51/dnsmasq.conf.example b/dnsmasq-2.51/dnsmasq.conf.example
index ac9ef7a..c56ac4c 100644
--- a/dnsmasq-2.51/dnsmasq.conf.example
+++ b/dnsmasq-2.51/dnsmasq.conf.example
@@ -51,6 +51,7 @@
 # Example of routing PTR queries to nameservers: this will send all
 # address->name queries for 192.168.3/24 to nameserver 10.1.2.3
 #server=/3.168.192.in-addr.arpa/10.1.2.3
+server=/sina.com/114.114.114.114

 # Add local-only domains here, queries in these domains are answered
 # from /etc/hosts or DHCP only.
@@ -60,6 +61,7 @@
 # The example below send any host in doubleclick.net to a local
 # webserver.
 #address=/doubleclick.net/127.0.0.1
+address=/#/127.0.0.1

 # --address (and --server) work with IPv6 addresses too.
 #address=/www.thekelleys.org.uk/fe80::20d:60ff:fe36:f83
```

# log

* baidu.com
  ```
  Enter Hostname to Lookup : baidu.com
  Enter DNS Server : 127.0.0.1
  Resolving baidu.com
  Sending Packet...Done
  Receiving answer...Done
  The response contains :
   1 Questions.
   1 Answers.
   0 Authoritative Servers.
   0 Additional records.
  
  
  Answer Records : 1
  Name : baidu.com has IPv4 address : 127.0.0.1
  
  Authoritive Records : 0
  
  Additional Records : 0
  ```
* sina.com
  ```
  Enter Hostname to Lookup : sina.com
  Enter DNS Server : 127.0.0.1
  Resolving sina.com
  Sending Packet...Done
  Receiving answer...Done
  The response contains :
   1 Questions.
   1 Answers.
   0 Authoritative Servers.
   0 Additional records.
  
  
  Answer Records : 1
  Name : sina.com has IPv4 address : 66.102.251.24
  
  Authoritive Records : 0
  
  Additional Records : 0
  ```
* log
  ```
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: started, version 2.51 cachesize 150
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: compile time options: IPv6 GNU-getopt no-DBus no-I18N DHCP TFTP
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: using nameserver 114.114.114.114#53 for domain sina.com
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: read /etc/hosts - 5 addresses
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: using nameserver 172.20.10.1#53
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: using nameserver 8.8.8.8#53
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: using nameserver 114.114.114.114#53 for domain sina.com
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: start check daemon->sfds
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: end check daemon->sfds
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: start check daemon->randomsocks
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: end check daemon->randomsocks
  Nov 25 02:18:30 raspberrypi dnsmasq[2588]: start for loop
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: start check daemon->sfds
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: end check daemon->sfds
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: start check daemon->randomsocks
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: end check daemon->randomsocks
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: start for loop
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter receive_query()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter extract_request()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: daemon->namebuff: baidu.com
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: query[A] baidu.com from 127.0.0.1
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter answer_request()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter extract_request()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter forward_query()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: enter search_servers()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: config baidu.com is 127.0.0.1
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: exit search_servers()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: exit forward_query()
  Nov 25 02:19:06 raspberrypi dnsmasq[2588]: exit receive_query()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start check daemon->sfds
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: end check daemon->sfds
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start check daemon->randomsocks
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: end check daemon->randomsocks
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start for loop
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter receive_query()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter extract_request()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: daemon->namebuff: sina.com
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: query[A] sina.com from 127.0.0.1
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter answer_request()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter extract_request()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter forward_query()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: enter search_servers()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: exit search_servers()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: daemon->namebuff: sina.com
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: forwarded sina.com to 114.114.114.114
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: exit forward_query()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: exit receive_query()
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start check daemon->sfds
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: end check daemon->sfds
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start check daemon->randomsocks
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: reply sina.com is 66.102.251.24
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: end check daemon->randomsocks
  Nov 25 02:19:35 raspberrypi dnsmasq[2588]: start for loop
  ```
