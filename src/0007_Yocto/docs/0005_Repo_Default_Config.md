# Repo Default Config

Yocto Repo

* 创建自己layer仓库；
* 参考下面`fsl-setup-release.sh`添加`layer`到`conf/bblayers.conf`方式，换成自己的`fsl-setup-release.sh`；
* 修改下面的`default.xml`成自己的需求，push到github仓库里；
* `repo init -u <your github repository url> -b <your github repository branch>`；

# default.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest>

  <default sync-j="2"/>

  <remote fetch="git://git.yoctoproject.org" name="yocto"/>
  <remote fetch="git://github.com/Freescale" name="freescale"/>
  <remote fetch="git://git.openembedded.org" name="oe"/>
  <remote fetch="git://github.com/OSSystems" name="OSSystems"/>
  <remote fetch="git://github.com/meta-qt5"  name="QT5"/>
  <remote fetch="git://git.freescale.com/imx" name="fsl-release" />

  <project remote="yocto" revision="f5da2a5913319ad6ac2141438ba1aa17576326ab" name="poky" path="sources/poky"/>
  <project remote="yocto" revision="be78894e4682f111575470fb23e51e6ba523508d" name="meta-fsl-arm" path="sources/meta-fsl-arm"/>

  <project remote="oe" revision="247b1267bbe95719cd4877d2d3cfbaf2a2f4865a" name="meta-openembedded" path="sources/meta-openembedded"/>

  <project remote="freescale" revision="krogoth" name="fsl-community-bsp-base" path="sources/base">
     <copyfile dest="README" src="README"/>
     <copyfile dest="0005_setup-environment" src="0005_setup-environment"/>
  </project>

  <project remote="freescale" revision="3dfb82fc7e703eae9891b3ffda0e9393701f2396" name="meta-fsl-arm-extra" path="sources/meta-fsl-arm-extra"/>
  <project remote="freescale" revision="a165068f8a0d1cf29aabe4b4053f28be1c2aa492" name="meta-fsl-demos" path="sources/meta-fsl-demos"/>

  <project remote="OSSystems" revision="77736988073a5d90fcff9d0005c8477332ede387" name="meta-browser" path="sources/meta-browser" />
  <project remote="QT5" revision="ccae79be69c5268df3b47e4e14cea0591c39a531" name="meta-qt5" path="sources/meta-qt5" />

  <project remote="fsl-release" name="meta-fsl-bsp-release" path="sources/meta-fsl-bsp-release" revision="krogoth_4.1.y" >
     <copyfile src="imx/tools/fsl-setup-release.sh" dest="fsl-setup-release.sh"/>
     <copyfile src="imx/README" dest="README-IMXBSP"/>
  </project>

</manifest>
```

# fsl-setup-release.sh

```Shell
[...省略]
META_FSL_BSP_RELEASE="${CWD}/sources/meta-fsl-bsp-release/imx/meta-bsp"
echo "##Freescale Yocto Project Release layer" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-fsl-bsp-release/imx/meta-bsp \"" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-fsl-bsp-release/imx/meta-sdk \"" >> $BUILD_DIR/conf/bblayers.conf

echo "BBLAYERS += \" \${BSPDIR}/sources/meta-browser \"" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-openembedded/meta-gnome \"" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-openembedded/meta-networking \"" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-openembedded/meta-python \"" >> $BUILD_DIR/conf/bblayers.conf
echo "BBLAYERS += \" \${BSPDIR}/sources/meta-openembedded/meta-filesystems \"" >> $BUILD_DIR/conf/bblayers.conf

echo "BBLAYERS += \" \${BSPDIR}/sources/meta-qt5 \"" >> $BUILD_DIR/conf/bblayers.conf

echo BSPDIR=$BSPDIR
echo BUILD_DIR=$BUILD_DIR
[...省略]
```
