# pem 2 der

pem转der

# cmd

* openssl -V x509 -outform der -in rootca_pem.crt -out rootca_pem.der

# steps

* cgdb ./openssl/apps/openssl
  * set args x509 -outform der -in rootca_pem.crt -out rootca_pem.der

```
#0  ASN1_item_i2d_bio (it=0x1c2b1c <X509_it>, out=out@entry=0x20ceb0, x=x@entry=0x20d398) at a_i2d_fp.c:138
#1  0x00111714 in i2d_X509_bio (bp=bp@entry=0x20ceb0, x509=x509@entry=0x20d398) at x_all.c:157
#2  0x0002c358 in x509_main (argc=<optimized out>, argv=<optimized out>) at x509.c:1054
#3  0x00012610 in do_cmd (prog=prog@entry=0x20b250, argc=argc@entry=7, argv=argv@entry=0xbefff3e8) at openssl.c:490
#4  0x00012234 in main (Argc=7, Argv=0xbefff3e8) at openssl.c:382
```
