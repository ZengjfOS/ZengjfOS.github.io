# boot id

启动id

# 参考文档

* [On IDs](http://0pointer.de/blog/projects/ids.html)

# 说明

/proc/sys/kernel/random/boot_id

A random ID that is regenerated on each boot. As such it can be used to identify the local machine's current boot. It's universally available on any recent Linux kernel. It's a good and safe choice if you need to identify a specific boot on a specific booted kernel.

# steps

cat /proc/sys/kernel/random/boot_id
