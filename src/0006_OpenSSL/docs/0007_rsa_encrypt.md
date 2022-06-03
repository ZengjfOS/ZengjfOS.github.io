# rsa encrypt

ras加密

# hash

sha256sum rootca.key | cut -d " " -f 1 > hash.txt

# command

./openssl/apps/openssl rsautl -sign -in hash.txt -out hash.sig -inkey rootca.key

# cgdb

```
(gdb) handle SIGILL pass nostop
(gdb) set args rsautl -sign -in hash.txt -out hash.sig -inkey rootca.key
```

# error

```
ig -inkey rootca.key
open error
load_sig_file error /tmp/hashraw753763409_SIG.bin
RSA operation error
```

# bt

```
#0  load_sig_file (_sz=<synthetic pointer>, data=..., fn=0xbeffeba0 "") at rsa_eay.c:444
#1  calcSignatureRaw (textpadded=textpadded@entry=0x20ffb0 "", signature=..., signature@entry=0x20b060 "\230$\255\373H\356 ")
at rsa_eay.c:444
#2  0x000c3200 in RSA_eay_private_encrypt (flen=<optimized out>, from=<optimized out>, to=0x20b060 "\230$\255\373H\356 ", rsa=0x20c1e0, padding=1) at rsa_eay.c:602
#3  0x000265a0 in rsautl_main (argc=<optimized out>, argv=<optimized out>) at rsautl.c:285
#4  0x00012610 in do_cmd (prog=prog@entry=0x20b310, argc=argc@entry=8, argv=argv@entry=0xbefff3d8) at openssl.c:490
#5  0x00012234 in main (Argc=8, Argv=0xbefff3d8) at openssl.c:382
```

# 私钥加密

crypto/rsa/rsa_eay.c

```CPP
/* signing */
static int RSA_eay_private_encrypt(int flen, const unsigned char *from,
                                   unsigned char *to, RSA *rsa, int padding)
{
    BIGNUM *f, *ret, *res;
    int i, j, k, num = 0, r = -1;
    unsigned char *buf = NULL;
    BN_CTX *ctx = NULL;
    int local_blinding = 0;
    /*
     * Used only if the blinding structure is shared. A non-NULL unblind
     * instructs rsa_blinding_convert() and rsa_blinding_invert() to store
     * the unblinding factor outside the blinding structure.
     */
    BIGNUM *unblind = NULL;
    BN_BLINDING *blinding = NULL;

    // 创建上下文，如果创建上下文失败，就进行错误处理
    if ((ctx = BN_CTX_new()) == NULL)
        goto err;
    BN_CTX_start(ctx);
    f = BN_CTX_get(ctx);
    ret = BN_CTX_get(ctx);
    num = BN_num_bytes(rsa->n);
    buf = OPENSSL_malloc(num);
    if (!f || !ret || !buf) {
        RSAerr(RSA_F_RSA_EAY_PRIVATE_ENCRYPT, ERR_R_MALLOC_FAILURE);
        goto err;
    }

    // 数据填充模式，from是数据输入，buf是填充后的结果，处理错误返回
    switch (padding) {
    case RSA_PKCS1_PADDING:
        i = RSA_padding_add_PKCS1_type_1(buf, num, from, flen);
        break;
    case RSA_X931_PADDING:
        i = RSA_padding_add_X931(buf, num, from, flen);
        break;
    case RSA_NO_PADDING:
        i = RSA_padding_add_none(buf, num, from, flen);
        break;
    case RSA_SSLV23_PADDING:
    default:
        RSAerr(RSA_F_RSA_EAY_PRIVATE_ENCRYPT, RSA_R_UNKNOWN_PADDING_TYPE);
        goto err;
    }
    if (i <= 0)
        goto err;

    // 将填充后的buf中的num位的正整数转化为大数(big number)，结果在f中
    if (BN_bin2bn(buf, num, f) == NULL)
        goto err;

    // 比较大数f和传入的ras的n
    if (BN_ucmp(f, rsa->n) >= 0) {
        /* usually the padding functions would catch this */
        RSAerr(RSA_F_RSA_EAY_PRIVATE_ENCRYPT,
               RSA_R_DATA_TOO_LARGE_FOR_MODULUS);
        goto err;
    }

    // 获取是否使用盲签
    if (!(rsa->flags & RSA_FLAG_NO_BLINDING)) {
        blinding = rsa_get_blinding(rsa, &local_blinding, ctx);
        if (blinding == NULL) {
            RSAerr(RSA_F_RSA_EAY_PRIVATE_ENCRYPT, ERR_R_INTERNAL_ERROR);
            goto err;
        }
    }

    // 对大数f盲签处理
    if (blinding != NULL) {
        if (!local_blinding && ((unblind = BN_CTX_get(ctx)) == NULL)) {
            RSAerr(RSA_F_RSA_EAY_PRIVATE_ENCRYPT, ERR_R_MALLOC_FAILURE);
            goto err;
        }
        if (!rsa_blinding_convert(blinding, f, unblind, ctx))
            goto err;
    }

    // 数据加密，最终数据在ret中
    if ((rsa->flags & RSA_FLAG_EXT_PKEY) ||
        ((rsa->p != NULL) &&
         (rsa->q != NULL) &&
         (rsa->dmp1 != NULL) && (rsa->dmq1 != NULL) && (rsa->iqmp != NULL))) {
        if (!rsa->meth->rsa_mod_exp(ret, f, rsa, ctx))
            goto err;
    } else {
        BIGNUM local_d;
        BIGNUM *d = NULL;

        if (!(rsa->flags & RSA_FLAG_NO_CONSTTIME)) {
            BN_init(&local_d);
            d = &local_d;
            BN_with_flags(d, rsa->d, BN_FLG_CONSTTIME);
        } else
            d = rsa->d;

        if (rsa->flags & RSA_FLAG_CACHE_PUBLIC)
            if (!BN_MONT_CTX_set_locked
                (&rsa->_method_mod_n, CRYPTO_LOCK_RSA, rsa->n, ctx))
                goto err;

        if (!rsa->meth->bn_mod_exp(ret, f, d, rsa->n, ctx,
                                   rsa->_method_mod_n))
            goto err;
    }

    // 对大数f盲签处理
    if (blinding)
        if (!rsa_blinding_invert(blinding, ret, unblind, ctx))
            goto err;

    // 最终加密后的数据保存在res中
    if (padding == RSA_X931_PADDING) {
        BN_sub(f, rsa->n, ret);
        if (BN_cmp(ret, f) > 0)
            res = f;
        else
            res = ret;
    } else
        res = ret;

    /*
     * put in leading 0 bytes if the number is less than the length of the
     * modulus
     *
     * 将大数res转成二进制
     */
    j = BN_num_bytes(res);
    i = BN_bn2bin(res, &(to[num - j]));
    for (k = 0; k < (num - i); k++)
        to[k] = 0;

    r = num;

    // TODO
    // 加密数据替换主要发生在这里

 err:
    if (ctx != NULL) {
        BN_CTX_end(ctx);
        BN_CTX_free(ctx);
    }
    if (buf != NULL) {
        OPENSSL_cleanse(buf, num);
        OPENSSL_free(buf);
    }
    return (r);
}
```
