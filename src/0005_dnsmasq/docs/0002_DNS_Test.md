# dns Test

模拟DNS请求访问

# 参考文档

* [DNS Query Code in C with linux sockets](https://gist.github.com/fffaraz/9d9170b57791c28ccda9255b48315168)

# 示例

* [dns.c](refers/linux/dnsMonitor/dns.c)
  * make
  * ./dns
    ```
    Enter Hostname to Lookup : baidu.com
    Enter DNS Server : 127.0.0.1
    Resolving baidu.com
    Sending Packet...Done
    Receiving answer...Done
    The response contains :
     1 Questions.
     2 Answers.
     0 Authoritative Servers.
     0 Additional records.
    
    
    Answer Records : 2
    Name : baidu.com has IPv4 address : 220.181.38.251
    Name : baidu.com has IPv4 address : 220.181.38.148
    
    Authoritive Records : 0
    
    Additional Records : 0
    ```
* sudo tcpdump -i wlan0 -n -nn port '53 or 68'
  ```
  tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
  listening on wlan0, link-type EN10MB (Ethernet), capture size 262144 bytes
  ...省略
  01:20:27.659680 IP 172.20.10.7.50887 > 208.67.222.222.53: 1371+ A? baidu.com. (27)
  01:20:27.794022 IP 208.67.222.222.53 > 172.20.10.7.50887: 1371 2/0/0 A 220.181.38.251, A 220.181.38.148 (59)
  ...省略
  ```
