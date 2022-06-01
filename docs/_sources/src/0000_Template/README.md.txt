# README

这个是一个plan的文档模板目录示例架构

# docs

NO.|文件名称|摘要
:--:|:--|:--
0002| [green_image](docs/0002_green_image.md) | 分析绿色图片原理
0001| [red_image](docs/0001_red_image.md) | 分析红色图片原理

# 目录及文件规则

这部分内容不需要在正式文档中出现

## 示例目录层次

```
.
├── README.md
└── docs
    ├── 0001_red_image.md
    ├── 0002_green_image.md
    ├── images
    │   ├── 0001_red_image.png
    │   └── 0002_green_image.png
    └── refers
        ├── 0001_red_image.tar.bz2
        └── 0002_green_image.tar.bz2

3 directories, 7 files
```

## 目录说明

* 由于gitlab中文目录、文件会存在索引问题，所以只能用英文名；
* 所有的总结文档放在docs目录，示例：
  * docs/0001_red_image.md
  * docs/0002_green_image.md
* 所有的引用图片放在docs/images目录，示例：
  * docs/0001_red_image.md 引用 0001_red_image.png
  * docs/0002_green_image.md 引用 0002_green_image.png
* 所有的引用文档资料放在docs/refers目录，示例：
  * docs/0001_red_image.md 引用 0001_red_image.tar.bz2
  * docs/0002_green_image.md 引用 0002_green_image.tar.bz2

## 文档名命规范说明

* 由于gitlab中文目录、文件会存在索引问题，所以只能用英文名；
* 文档名命格式：[文档索引]_[内容名称].[后缀]
  * 文档索引: 采用四位表示: xxxx，例如：0231;
  * 内容名称: 不能有空格，仅能用英文名字;
  * 后缀: 正常的文件后缀就行;
* 文档索引必须唯一，文档索引依次增加，便于查找及排序；
* 同一文档内的图片索引必须相同，便于查找及排序；
* 同一文档内的文档资料索引必须相同，便于查找及排序；

# git相关说明

* git显示中文
  * git config --global core.quotepath false
* git commit
  * commit内容按照一定规范进行编写，写清楚为什么提交、提交了什么
  * 相对来可以放宽写，主要是文档内容
* git config --global core.editor "vim"
