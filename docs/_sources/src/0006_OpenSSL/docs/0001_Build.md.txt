# Build

编译openssl-1.0.1f

## Download

* https://www.openssl.org/source/old/1.0.1/
  * openssl-1.0.1f.tar.gz
* https://gitee.com/zengjfos/RaspberryPi/tree/openssl-1.0.1f

## build openssl

* ./config
* make
  * 不要用-j进行多核编译
* sudo make install
  * sudo rm /usr/bin/pod2man
* ls /usr/local/ssl
  ```
  bin  certs  include  lib  man  misc  openssl.cnf  private
  ```
* /usr/local/ssl/bin/openssl version
  ```
  OpenSSL 1.0.1f 6 Jan 2014
  ```
* /usr/local/ssl/bin/openssl req -new -x509 -key rootca.key -days 7300 -out oem_rootca.crt -subj /C=CN/ST=SZ/L=GD/OU="AAA"/OU="AAA"/O=AAA/CN="AAA Root Ca" -set_serial 1 -config opensslroot.cfg -sha256 -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:-1 -sigopt digest:sha256
