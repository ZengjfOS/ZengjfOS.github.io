# parse Whitelist config

分析配置文件server、address解析、应用原理

# MAXDNAME

* https://github.com/openbsd/src/blob/master/include/arpa/nameser.h#L100
  * `#define MAXDNAME	1025		/* maximum presentation domain name */`

# fgets

fgets() reads in at most one less than size characters from stream and stores them into the buffer pointed to by s. Reading stops after an EOF or a newline. If a newline is read, it is stored into the buffer. A terminating null byte ('\0') is stored after the last character in the buffer.

简单来说，一次读一行，可以如下测试看效果

```diff
diff --git a/dnsmasq-2.51/src/option.c b/dnsmasq-2.51/src/option.c
index abea37e..a3f3f80 100644
--- a/dnsmasq-2.51/src/option.c
+++ b/dnsmasq-2.51/src/option.c
@@ -2579,6 +2579,8 @@ static void one_file(char *file, int nest, int hard_opt)
       unsigned int lastquote;
       char *errmess;

+      my_syslog(LOG_DEBUG, "config file: %s", buff);
+
       /* Memory allocation failure longjmps here if mem_recover == 1 */
       if (hard_opt)
        {
```

# 测试config

* cat dnsmasq.conf.example
  ```
  server=/sina.com/114.114.114.114
  address=/#/127.0.0.1
  ```

# parse Whitelist config

* 在域名字段会检测#符号作为通配符；
  * address=/#/127.0.0.1#53
* IP字段#后面是port
  * address=/double-click.net/127.0.0.1#53
* @可以当作直接IP转发，相当于IP直通匹配
  * server=10.1.2.3@192.168.1.1#55
* 在数据处理部分，server和address是同一个地方处理，最终也是保存在同一个链表，采用的尾插链表
  * serv->next = daemon->servers;
  * daemon->servers = newlist;

```
* src/dnsmasq.c
  └── int main (int argc, char **argv)
      └── read_opts(argc, argv, compile_opts);
          ├── else if (option == 'C')
          │   └── conffile = opt_string_alloc(arg);
          └── if (conffile)
              └── one_file(conffile, nest, 0);
                  ├── fgets(buff, MAXDNAME, f)
                  ├── else if ((p=strchr(buff, '=')))
                  │   ├── for (start = buff; *start && isspace((int)*start); start++);
                  │   └── for (option = 0, i = 0; opts[i].name; i++)
                  │       └── if (strcmp(opts[i].name, start) == 0)
                  │           ├── option = opts[i].val;
                  │           │   └── 从配置名，如server、address找到对应的opts列表序号，然后从序号中获取其对应的简写option，一个配置名对应一个简写option
                  │           └── break
                  └── errmess = one_opt(option, arg, _("error"), nest + 1);
                      └── switch (option)
                          ├── case 'S':
                          └── case 'A':
                              └── if (arg && *arg == '/')
                                  └── while ((end = split_chr(arg, '/')))
                                      ├── if (strcmp(arg, "#") == 0)
                                      │   └── domain = "";
                                      │       └── 通配符#，用于设置所有的域名过滤
                                      ├── else if (strlen (arg) != 0 && !(domain = canonicalise_opt(arg)))
                                      ├── if ((newlist->addr.in.sin_addr.s_addr = inet_addr(arg)) != (in_addr_t) -1)
                                      │   └── newlist->addr.in.sin_port = htons(serv_port);
                                      │       └── 设置forward IP之后，设置forward port
                                      ├── serv->next = daemon->servers;
                                      └── daemon->servers = newlist;
```

# 测试daemon servers

* ./dns
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
* log
  ```
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: start check daemon->sfds
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: end check daemon->sfds
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: start check daemon->randomsocks
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: end check daemon->randomsocks
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: start for loop
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter receive_query()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter extract_request()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: daemon->namebuff: baidu.com
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: query[A] baidu.com from 127.0.0.1
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter answer_request()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter extract_request()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter forward_query()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter search_servers()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: config baidu.com is 127.0.0.1
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: exit search_servers()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: exit forward_query()
  Nov 25 06:04:35 raspberrypi dnsmasq[3730]: exit receive_query()
  ```
  * 关键信息，forward里面查询servers
    ```
    Nov 25 06:04:35 raspberrypi dnsmasq[3730]: enter search_servers()
    Nov 25 06:04:35 raspberrypi dnsmasq[3730]: config baidu.com is 127.0.0.1
    Nov 25 06:04:35 raspberrypi dnsmasq[3730]: exit search_servers()
    ```

# address Whitelist

* 在正常的forward之前，会查询daemon->servers
* 查询的使用的是域名尾匹配，就是只要域名的后面部分相同就算是相同的，便于处理子域名，这里比较重要的是设置了
  * `*type = SERV_HAS_DOMAIN;`
* 当查询到预置域名且是address时，会直接返回预置IP；

```
* src/dnsmasq.c
  └── int main (int argc, char **argv)
      └── check_dns_listeners(&rset, now);
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
                              ├── flags = search_servers(now, &addrp, gotname, daemon->namebuff, &type, &domain);
                              │   └── for (serv = daemon->servers; serv; serv=serv->next)
                              │       ├── else if (serv->flags & SERV_HAS_DOMAIN)
                              │       │   └── if (namelen >= domainlen && hostname_isequal(matchstart, serv->domain) && ...)
                              │       │       ├── *type = SERV_HAS_DOMAIN;
                              │       │       └── 匹配上了
                              │       └── log_query(logflags | flags | F_CONFIG | F_FORWARD, qdomain, *addrpp, NULL);
                              │           └── Nov 25 06:04:35 raspberrypi dnsmasq[3730]: config baidu.com is 127.0.0.1
                              │               └── 如果在config中配置了，就用config中配置的
                              └── if (udpfd != -1)
                                  ├── plen = setup_reply(header, plen, addrp, flags, daemon->local_ttl);
                                  └── send_from(udpfd, daemon->options & OPT_NOWILD, (char *)header, plen, udpaddr, dst_addr, dst_iface);
```

# server Whitelist

* 在正常的forward之前，会查询daemon->servers
* 查询的使用的是域名尾匹配，就是只要域名的后面部分相同就算是相同的，便于处理子域名，这里比较重要的是设置了
  * `*type = SERV_HAS_DOMAIN;`
* 当查询到预置域名且是server时，走的是正常的forward流程，但是
  * `forward->forwardall = 0;`
* 在后面迭代daemon->servers的时候
  * 只要找到了server发送完请求就会break，不会往下继续迭代
  * 默认的/run/dnsmasq/resolv.conf中的nameserver是在链表最底部，所以不会被迭代
  * 正常的域名解析会迭代所有的

```
* src/dnsmasq.c
  * int main (int argc, char **argv)
    * check_dns_listeners(&rset, now);
      * for (listener = daemon->listeners; listener; listener = listener->next)
        * if (listener->fd != -1 && FD_ISSET(listener->fd, set))
          * receive_query(listener, now);
            * n = recvmsg(listen->fd, &msg, 0)
            * if (extract_request(header, (size_t)n, daemon->namebuff, &type))
              * log_query(F_QUERY | F_IPV4 | F_FORWARD, daemon->namebuff, (struct all_addr *)&source_addr.in.sin_addr, types);
                * Nov 24 06:52:10 raspberrypi dnsmasq[5107]: query[A] baidu.com from 127.0.0.1
            * m = answer_request (header, ((char *) header) + PACKETSZ, (size_t)n, dst_addr_4, netmask, now);
            * else if (forward_query(listen->fd, &source_addr, &dst_addr, if_index, header, (size_t)n, now, NULL))
              * static int forward_query(int udpfd, union mysockaddr *udpaddr, ...)
                * flags = search_servers(now, &addrp, gotname, daemon->namebuff, &type, &domain);
                  * for (serv = daemon->servers; serv; serv=serv->next)
                    * else if (serv->flags & SERV_HAS_DOMAIN)
                      * if (namelen >= domainlen && hostname_isequal(matchstart, serv->domain) && ...)
                        * *type = SERV_HAS_DOMAIN;
                          * 这个type会决定是只迭代一次daemon->servers，还是所有
                    * log_query(logflags | flags | F_CONFIG | F_FORWARD, qdomain, *addrpp, NULL);
                      * Nov 25 06:04:35 raspberrypi dnsmasq[3730]: config baidu.com is 127.0.0.1
                        * 如果在config中配置了，就用config中配置的
                * if (forward)
                  * forward->forwardall = 0;
                    * if (type != 0  || (daemon->options & OPT_ORDER))
                      * 这里很关键的，没有设置forward->forwardall = 1
                * sendto(fd, (char *)header, plen, 0, &start->addr.sa, sa_len(&start->addr))
                * log_query(F_SERVER | F_IPV4 | F_FORWARD, daemon->namebuff, (struct all_addr *)&start->addr.in.sin_addr, NULL);
                  * Nov 24 07:26:36 raspberrypi dnsmasq[5523]: forwarded baidu.com to 8.8.8.8
```
