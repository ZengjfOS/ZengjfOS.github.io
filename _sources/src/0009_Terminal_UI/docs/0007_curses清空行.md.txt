# curses清空行

curses自带清空行

# 参考文档

* [clrtoeol(3) - Linux man page](https://linux.die.net/man/3/clrtoeol)
* [self.screen.clrtoeol()](https://github.com/darknessomi/musicbox/blob/master/NEMbox/ui.py#L149)

# 简述

The clrtobot and wclrtobot routines erase from the cursor to the end of screen. That is, they erase all lines below the cursor in the window. Also, the current line to the right of the cursor, inclusive, is erased.

The clrtoeol and wclrtoeol routines erase the current line to the right of the cursor, inclusive, to the end of the current line.
