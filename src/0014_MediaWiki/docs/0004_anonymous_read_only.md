# Anonymous Read Only

匿名用户只能读，无法修改

# 参考文档

* [Mediawiki页面权限设置 禁止游客编辑 禁止注册](https://dev-docs.csdn.net/articles/e8892eb114144269b4d37c6c9490299b/)

# LocalSettings修改

* [0001_LocalSettings.php](refers/0001_LocalSettings.php)
  ```yaml
  $wgGroupPermissions['*']['read'] = true;
  $wgGroupPermissions['*']['edit'] = false;
  ```
