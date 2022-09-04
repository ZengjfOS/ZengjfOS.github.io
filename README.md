# README

使用Sphinx，配合myst_parser插件，将Markdown文档生成GitHub Pages

# 发行PyPi处理流程

* pip3 install twine
* https://pypi.org/
  * 注册帐号
* python3 setup.py sdist bdist_wheel
* twine upload dist/*
  ```
  Uploading distributions to https://upload.pypi.org/legacy/
  Enter your username: zengjf
  Enter your password:
  Uploading VisualLog-0.0.0-py3-none-any.whl
  100% ---------------------------------------- 8.4/8.4 kB • 00:00 • ?
  Uploading VisualLog-0.0.0.tar.gz
  100% ---------------------------------------- 6.6/6.6 kB • 00:00 • ?
  
  View at:
  https://pypi.org/project/VisualLog/0.0.0/
  ```
