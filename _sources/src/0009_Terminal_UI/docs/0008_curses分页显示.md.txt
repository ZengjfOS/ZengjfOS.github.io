# curses分页显示

分析musicbox中是如何处理分页显示的，看别人是怎么处理大于一页内容(翻页)

# build_menu分析

* https://github.com/darknessomi/musicbox/blob/master/NEMbox/ui.py#L373
  * `def build_menu(self, datatype, title, datalist, offset, index, step, start):`
* datalist是所有的数据，也就是说一般数据量很多，还是保存在内存中的；
* 通过step，也就是一页显示的内容范围来做翻页处理；
* offset表示当前页起始索引；
* index表示高亮的索引，也就是当前播放的歌曲，也就是当前的选择；

```python
# start is the called timestamp of this function
#
# 1. step: 是屏幕能够显示的最大一页
# 2. offset: 是当前起始数据
# 3. index: 高亮显示的那一行（那首歌），聚焦的那首歌
# 4. start: 终端可显示范围小于实际需要显示的字符串的长度，所以需要滚动显示，start用来处理这个滚动显示
def build_menu(self, datatype, title, datalist, offset, index, step, start):
    # keep playing info in line 1
    curses.noecho()
    curses.curs_set(0)
    self.screen.move(7, 1)
    self.screen.clrtobot()
    self.addstr(7, self.startcol, title, curses.color_pair(1))

    # ...省略

    elif datatype == "songs" or datatype == "djprograms" or datatype == "fmsongs":
        # 很好的处理了最后一页内容不够一页问题
        iter_range = min(len(datalist), offset + step)
        for i in range(offset, iter_range):
            # 数据类型判断
            if isinstance(datalist[i], str):
                raise ValueError(datalist)
            # this item is focus
            if i == index:
                # 一行的开始填充空格
                self.addstr(i - offset + 9, 0, " " * self.startcol)
                # ->表示聚焦在哪一行(高亮)
                lead = "-> " + str(i) + ". "
                self.addstr(
                    i - offset + 9,
                    self.indented_startcol,
                    lead,
                    curses.color_pair(2),
                )
                # 歌曲信息
                name = "{}{}{}  < {} >".format(
                    datalist[i]["song_name"],
                    self.space,
                    datalist[i]["artist"],
                    datalist[i]["album_name"],
                )

                # the length decides whether to scroll
                # 显示数据小于可显示范围，直接显示
                if truelen(name) < self.content_width:
                    self.addstr(
                        i - offset + 9,
                        self.indented_startcol + len(lead),
                        name,
                        curses.color_pair(2),
                    )
                # 显示数据大于可显示范围，通过start来截取字符串
                else:
                    name = scrollstring(name + "  ", start)
                    self.addstr(
                        i - offset + 9,
                        self.indented_startcol + len(lead),
                        truelen_cut(
                            str(name), self.content_width - len(str(i)) - 2
                        ),
                        curses.color_pair(2),
                    )
            # 非聚焦行，只需要正常处理就好了
            else:
                self.addstr(i - offset + 9, 0, " " * self.startcol)
                self.addstr(
                    i - offset + 9,
                    self.startcol,
                    truelen_cut(
                        "{}. {}{}{}  < {} >".format(
                            i,
                            datalist[i]["song_name"],
                            self.space,
                            datalist[i]["artist"],
                            datalist[i]["album_name"],
                        ),
                        self.content_width,
                    ),
                )

        self.addstr(iter_range - offset + 9, 0, " " * self.x)

    # ...省略

    self.screen.refresh()
```
