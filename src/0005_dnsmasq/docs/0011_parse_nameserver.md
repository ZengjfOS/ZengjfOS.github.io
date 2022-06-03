# parse nameserver

resolv.conf中nameserver解析原理

# 解析主要步骤

* 本质就是一行一行读文件，然后解析到IP
* 根据获的IP，生成数据到daemon->servers链表末尾

```
* src/network.c
  └── int reload_servers(char *fname)
      └── while ((line = fgets(daemon->namebuff, MAXDNAME, f)))
          ├── if ((addr.in.sin_addr.s_addr = inet_addr(token)) != (in_addr_t) -1)
          │   └── addr.in.sin_port = htons(NAMESERVER_PORT);
          ├── serv->domain = NULL;
          └── serv->flags = SERV_FROM_RESOLV;
```
