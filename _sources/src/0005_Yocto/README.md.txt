# README

分析Yocto编译原理，能做的事情和Buildroot类似，不过更重要的是芯片大厂都参与维护，知名度更高

* [The Yocto Project Development Manual](https://www.yoctoproject.org/docs/1.5.1/dev-manual/dev-manual.html#dev-manual-intro)
* [L4.1.15_2.0.0_LINUX_DOCS](https://www.nxp.com/webapp/Download?colCode=L4.1.15_2.0.0-LINUX-DOCS&Parent_nodeId=1337695836026701499367&Parent_pageType=product&Parent_nodeId=1337695836026701499367&Parent_pageType=product)

# Install libs

* `sudo apt-get install gawk wget git-core diffstat unzip texinfo gcc-multilib build-essential chrpath socat libsdl1.2-dev`
* `sudo apt-get install libsdl1.2-dev xterm sed cvs subversion coreutils texi2html docbook-utils python-pysqlite2 help2man make gcc g++ desktop-file-utils libgl1-mesa-dev libglu1-mesa-dev mercurial autoconf automake groff curl lzop asciidoc`
* i.MX layers host packages for a Ubuntu 12.04 host setup only are:  
  `sudo apt-get install uboot-mkimage`
* i.MX layers host packages for a Ubuntu 14.04 host setup only are:  
  `sudo apt-get install u-boot-tools`
* Repo: https://github.com/ZoroZeng/manifest

# How to select additional packages

* [YOCTO Customizing Images Doc](https://www.yoctoproject.org/docs/1.5.1/dev-manual/dev-manual.html#usingpoky-extend-customimage)
* Search YOCTO Recipes: https://layers.openembedded.org/layerindex/branch/master/recipes/
* 《i.MX Yocto Project User's Guide.pdf》 -- A.4 How to select additional packages

# docs

NO.  |文件名称|摘要
:---:|:--|:--
0017 | [ATF_SCFW_M4](docs/0017_ATF_SCFW_M4.md) | ATF SCFW M4编译原理
0016 | [rootfs_add_gcc_g++](docs/0016_rootfs_add_gcc_g++.md) | 尝试在rootfs中加入gcc、g++
0015 | [copy_file_to_rootfs](docs/0015_copy_file_to_rootfs.md) | 自动添加文件到rootfs
0014 | [run_do_function](docs/0014_run_do_function.md) | Yocto run do函数
0013 | [u-boot_generate](docs/0013_u-boot_generate.md) | u-boot生成原理
0012 | [boot-img_generate](docs/0012_boot-img_generate.md) | boot.img合成原理
0011 | [bitbake_variable_override](docs/0011_bitbake_variable_override.md) | bitback变量覆盖
0010 | [bitbake_Hello-World](docs/0010_bitbake_Hello-World.md) | 添加Hello World bb
0009 | [YOCTO_SD_Image_Generate](docs/0009_YOCTO_SD_Image_Generate.md) | 分析Yocto SD卡镜像合成
0008 | [Yocto_Toolchain](docs/0008_Yocto_Toolchain.md) | 编译Yocto编译工具链
0007 | [MFGTool_initramfs_Boot_Root_Filesystem](docs/0007_MFGTool_initramfs_Boot_Root_Filesystem.md) | 分析MFGTool的initramfs
0006 | [MFGTool_U-Boot_In_Yocto_Receipe](docs/0006_MFGTool_U-Boot_In_Yocto_Receipe.md) | 分析MFGTool的U-Boot在Yocto中的编译
0005 | [Repo_Default_Config](docs/0005_Repo_Default_Config.md) | Yocto Repo
0004 | [Add_New_layer_And_Recipe](docs/0004_Add_New_layer_And_Recipe.md) | Yocto添加新的Layer和Recipe
0003 | [Operation_bb_File](docs/0003_Operation_bb_File.md) | 生成bb可视化文件
0002 | [Read_Manual](docs/0002_Read_Manual.md) | Yocto参考手册
0001 | [fsl-setup-release_setup-environment](docs/0001_fsl-setup-release_setup-environment.md) | Freescal i.MX6 Yocto编译
