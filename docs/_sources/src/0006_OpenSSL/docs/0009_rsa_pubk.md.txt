# rsa pubk

私钥提取公钥

# cmd

./openssl/app rsa -in rootca.key -pubout -out rsa_public_key.pem

# bt

```
#0  EVP_PKEY_get1_RSA (pkey=pkey@entry=0x20a3c0) at p_lib.c:287
#1  0x000258ac in rsa_main (argc=<optimized out>, argv=0xbefff5a0) at rsa.c:296
#2  0x00012610 in do_cmd (prog=prog@entry=0x20b250, argc=argc@entry=6, argv=argv@entry=0xbefff588) at openssl.c:490
#3  0x00012234 in main (Argc=6, Argv=0xbefff588) at openssl.c:382
```
