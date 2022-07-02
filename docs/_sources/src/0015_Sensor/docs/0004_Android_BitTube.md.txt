# Android BitTube

BitTube本质是socketpair，Binder实现了sendmsg传递fd的功能

# 参考文档

* [输入系统：进程间双向通信(socketpair+binder)](https://www.cnblogs.com/blogs-of-lxl/p/10542654.html)
* [7.6.3 跨进程传递文件描述符的探讨](https://www.kancloud.cn/alex_wsc/android-deep2/413529)
* [【Android】Binder传送文件描述符分析](https://blog.csdn.net/aaajj/article/details/73381384)
* [android sensor 框架分析---sensor数据流分析](https://blog.csdn.net/u012439416/article/details/74614078?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522158814043219725222462036%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=158814043219725222462036&biz_id=0&utm_source=)

# 简要说明

* Android系统中进程间通信方式主要为Binder，而Binder通信方式中，Client端可以主动发起请求与Server端通信，但Server端无法向Client端主动发起请求，基于socketpair + binder可以实现任意进程间的双向通信（通过binder将fd句柄传到另一个非亲缘关系的进程）
* binder支持传递文件描述符
  ```CPP
  // kernel-4.9/drivers/android/binder.c
  
  static void binder_transaction(struct binder_proc *proc,
                     struct binder_thread *thread,
                     struct binder_transaction_data *tr, int reply,
                     binder_size_t extra_buffers_size)
  {
          // ...省略
          case BINDER_TYPE_FD: {
              struct binder_fd_object *fp = to_binder_fd_object(hdr);
              int target_fd = binder_translate_fd(fp->fd, t, thread,
                                  in_reply_to);
  
              if (target_fd < 0) {
                  return_error = BR_FAILED_REPLY;
                  return_error_param = target_fd;
                  return_error_line = __LINE__;
                  goto err_translate_failed;
              }
              fp->pad_binder = 0;
              fp->fd = target_fd;
  #ifdef BINDER_WATCHDOG
              e->fd = target_fd;
  #endif
              binder_alloc_copy_to_buffer(&target_proc->alloc,
                              t->buffer, object_offset,
                              fp, sizeof(*fp));
          } break;
          // ...省略
  }
  ```
* [Android BitTube进程间数据传递](https://blog.csdn.net/new_abc/article/details/8971961)
* [输入系统：进程间双向通信(socketpair+binder)](https://www.cnblogs.com/blogs-of-lxl/p/10542654.html)
