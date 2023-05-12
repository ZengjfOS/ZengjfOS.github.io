# LogParser

解决分析数据重复操作解析log文件，使用正则表达式配合回调函数处理

# 示例

* [0008_LogParser.py](refers/0008_LogParser.py)
* [0008_zcv.txt](refers/0008_zcv.txt)
* 使用示例
  ```python
  def defaultLineCallback(lineInfo):
      lineInfoFixed = []
      for index in range(len(lineInfo)):
          lineInfoFixed.append(float(lineInfo[index].strip()))
      
      return lineInfoFixed

  lineInfos = LogParser.logFileParser(
          "refers/0008_zcv.txt",
          r'(\d+)\s+(\d+)\s+(\d+)',
          callback=defaultLineCallback
      )
  for info in lineInfos:
  print(info)
  ```
  * 回调函数主要用于过滤、修正、中间数据处理等操作
* log
  ```
  [27956.0, 36608.0, 1178.0]
  [28257.0, 36305.0, 1118.0]
  [28558.0, 35848.0, 1115.0]
  [28858.0, 35271.0, 1150.0]
  [29159.0, 34459.0, 1187.0]
  [29459.0, 33091.0, 1536.0]
  [29760.0, 29420.0, 8600.0]
  ```
