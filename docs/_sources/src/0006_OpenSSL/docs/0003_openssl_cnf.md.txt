# openssl.cnf

openssl.cnf依赖

## openssl.conf

/usr/local/ssl/openssl.cnf

```
* apps/openssl.c
  * p=getenv("OPENSSL_CONF");
  * if (p == NULL)
    * p=to_free=make_config_name();
      * apps/apps.c
        * char *make_config_name()
          * const char *t=X509_get_default_cert_area();
            * t: /usr/local/ssl
```

* 环境变量设置的OPENSSL_CONF优先级更高
* export

```sh
export OPENSSL_CONF=[openssl.cnf file path]
```
