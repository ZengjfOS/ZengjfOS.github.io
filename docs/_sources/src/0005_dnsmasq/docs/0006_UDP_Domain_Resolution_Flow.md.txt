# UDP Domain Resolution Flow

UDP域名解析流程

# 域名解析调用关系

```
* src/dnsmasq.c
  └── int main (int argc, char **argv)
      └── check_dns_listeners(&rset, now);
          ├── if (daemon->port != 0 && !daemon->osport)
          │   └── for (i = 0; i < RANDOM_SOCKS; i++)
          │       └── if (daemon->randomsocks[i].refcount != 0 && FD_ISSET(daemon->randomsocks[i].fd, set))
          │           └── reply_query(daemon->randomsocks[i].fd, daemon->randomsocks[i].family, now);
          │               └── nn = process_reply(header, now, server, (size_t)n)
          │                   └── extract_addresses(header, n, daemon->namebuff, now)
          │                       └── cache_insert(NULL, &addr, now, ttl, name_encoding | F_REVERSE | F_NEG | flags);
          │                           └── log_query(flags | F_UPSTREAM, name, addr, NULL);
          │                               └── Nov 24 06:52:11 raspberrypi dnsmasq[5107]: reply baidu.com is 220.181.38.251
          └── for (listener = daemon->listeners; listener; listener = listener->next)
              └── if (listener->fd != -1 && FD_ISSET(listener->fd, set))
                  └── receive_query(listener, now);
                      ├── n = recvmsg(listen->fd, &msg, 0)
                      ├── if (extract_request(header, (size_t)n, daemon->namebuff, &type))
                      │   └── log_query(F_QUERY | F_IPV4 | F_FORWARD, daemon->namebuff, (struct all_addr *)&source_addr.in.sin_addr, types);
                      │       └── Nov 24 06:52:10 raspberrypi dnsmasq[5107]: query[A] baidu.com from 127.0.0.1
                      ├── m = answer_request (header, ((char *) header) + PACKETSZ, (size_t)n, dst_addr_4, netmask, now);
                      └── else if (forward_query(listen->fd, &source_addr, &dst_addr, if_index, header, (size_t)n, now, NULL))
                          └── static int forward_query(int udpfd, union mysockaddr *udpaddr, ...)
                              ├── sendto(fd, (char *)header, plen, 0, &start->addr.sa, sa_len(&start->addr))
                              └── log_query(F_SERVER | F_IPV4 | F_FORWARD, daemon->namebuff, (struct all_addr *)&start->addr.in.sin_addr, NULL);
                                  └── Nov 24 07:26:36 raspberrypi dnsmasq[5523]: forwarded baidu.com to 8.8.8.8
```

# baidu.com log

```
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start check daemon->sfds
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: end check daemon->sfds
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start for loop
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter receive_query()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter extract_request()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: daemon->namebuff: baidu.com
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: query[A] baidu.com from 127.0.0.1
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter answer_request()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter extract_request()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter forward_query()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: enter search_servers()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: exit search_servers()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: daemon->namebuff: baidu.com
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: forwarded baidu.com to 8.8.8.8
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: exit forward_query()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: exit receive_query()
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start check daemon->sfds
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: end check daemon->sfds
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start check daemon->randomsocks
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: reply baidu.com is 220.181.38.148
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: reply baidu.com is 220.181.38.251
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: end check daemon->randomsocks
Nov 25 01:50:02 raspberrypi dnsmasq[2111]: start for loop
```
