# Whitelist Blacklist

设置server白名单，设置address黑名单

# 参考文档

* [Using dnsmasq to block DNS requests](https://alblue.bandlem.com/2020/05/using-dnsmasq.html)
* [To Protect and Surf (dnsmasq and Whitelists)](https://www.teknynja.com/2009/06/to-protect-and-surf-dnsmasq-and.html)
* [Dnsmasq Whitelist](http://www.intellamech.com/RaspberryPi-projects/dnsmasq_whitelist.html)

# set config

```diff
diff --git a/dnsmasq-2.51/dnsmasq.conf.example b/dnsmasq-2.51/dnsmasq.conf.example
index ac9ef7a..e158fbf 100644
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
+address=/doubleclick.net/127.0.0.2

 # --address (and --server) work with IPv6 addresses too.
 #address=/www.thekelleys.org.uk/fe80::20d:60ff:fe36:f83
```

# server

* 启动log
  ```
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: started, version 2.51 cachesize 150
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: compile time options: IPv6 GNU-getopt no-DBus no-I18N DHCP TFTP
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: using nameserver 114.114.114.114#53 for domain sina.com
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: read /etc/hosts - 5 addresses
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: using nameserver 8.8.8.8#53
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: using nameserver 114.114.114.114#53 for domain sina.com
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: start check daemon->sfds
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: end check daemon->sfds
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
  Nov 25 01:37:39 raspberrypi dnsmasq[2111]: start for loop
  ```
  * Nov 25 01:37:39 raspberrypi dnsmasq[2111]: using nameserver 114.114.114.114#53 for domain sina.com
  * using nameserver 114.114.114.114#53 for domain sina.com
* ./dns
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
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: start check daemon->sfds
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: end check daemon->sfds
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: start for loop
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter receive_query()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter extract_request()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: daemon->namebuff: sina.com
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: query[A] sina.com from 127.0.0.1
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter answer_request()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter extract_request()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter forward_query()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: enter search_servers()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: exit search_servers()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: daemon->namebuff: sina.com
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: forwarded sina.com to 114.114.114.114
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: exit forward_query()
  Nov 25 01:46:50 raspberrypi dnsmasq[2111]: exit receive_query()
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: start check daemon->sfds
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: end check daemon->sfds
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: reply sina.com is 66.102.251.24
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
  Nov 25 01:46:51 raspberrypi dnsmasq[2111]: start for loop
  ```
  * Nov 25 01:46:50 raspberrypi dnsmasq[2111]: forwarded sina.com to 114.114.114.114

# address

* ./dns
  ```
  Enter Hostname to Lookup : doubleclick.net
  Enter DNS Server : 127.0.0.1
  Resolving doubleclick.net
  Sending Packet...Done
  Receiving answer...Done
  The response contains :
   1 Questions.
   1 Answers.
   0 Authoritative Servers.
   0 Additional records.
  
  
  Answer Records : 1
  Name : doubleclick.net has IPv4 address : 127.0.0.2
  
  Authoritive Records : 0
  
  Additional Records : 0
  ```
* log
  ```
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: start check daemon->sfds
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: end check daemon->sfds
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: start for loop
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter receive_query()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter extract_request()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: daemon->namebuff: doubleclick.net
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: query[A] doubleclick.net from 127.0.0.1
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter answer_request()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter extract_request()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter forward_query()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: enter search_servers()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: config doubleclick.net is 127.0.0.2
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: exit search_servers()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: exit forward_query()
  Nov 25 01:43:41 raspberrypi dnsmasq[2111]: exit receive_query()
  ```

# 总结

The main reason I did this was to block hosts. In dnsmasq, the syntax for blocking a host as flowing, which roughly translated means For domains ending in example.com, send the result to NXDOMAIN. 

```
address=/example.com/
```

Direct all other domains to 127.0.0.1

```
address=/#/127.0.0.1
```

Add other name servers here, with domain specs if they are for non-public domains.

```
server=/google.com/8.8.8.8
```

* address：预置域名及其IP
* server：指定DNS去解析域名
