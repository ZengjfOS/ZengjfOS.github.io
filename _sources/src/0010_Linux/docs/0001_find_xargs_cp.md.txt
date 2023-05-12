# find xargs cp

find之后通过xargs进行拷贝

# shell

```sh
find * -iname "*440*" | xargs -I {} cp {} ../../ZengjfOS.github.io/src/PowerConsumption/docs
```
