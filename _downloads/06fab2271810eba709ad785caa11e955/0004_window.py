# curses
import curses

# keyboard code
KEY_BOARD_ENTER = 10
KEY_BOARD_ESC = 27
KEY_BOARD_BACKSPACE = 127
KEY_BOARD_UP = 259
KEY_BOARD_DOWN = 258
KEY_BOARD_LEFT = 260
KEY_BOARD_RIGHT = 261

# 初始化一个窗口
mainScreen = curses.initscr()
# 绘制边框
mainScreen.border(0)
# 使用curses通常要关闭屏幕回显，目的是读取字符仅在适当的环境下输出
curses.noecho()
# 应用程序一般是立即响应的，即不需要按回车就立即回应的，这种模式叫cbreak模式，相反的常用的模式是缓冲输入模式
curses.cbreak()
# 终端经常返回特殊键作为一个多字节的转义序列，比如光标键，或者导航键比如Page UP和Home键。
# curses可以针对这些序列做一次处理，比如curses.KEY_LEFT返回一个特殊的值。要完成这些工作，必须开启键盘模式。
mainScreen.keypad(1)

# 获取当前行列信息
maxRows = curses.LINES
maxCols = curses.COLS

# 计数
count = 0

# 在行列(1，1)输出window字符
mainScreen.addstr(1, 1, "window: " + str(count))
# 刷新界面
mainScreen.refresh()

while True:
    # 等待按键事件
    ch = mainScreen.getch()

    if ch == curses.KEY_RESIZE:
        count += 1

        mainScreen.clear()
        maxRows, maxCols = mainScreen.getmaxyx()
        mainScreen.border(0)

        mainScreen.addstr(1, 1, "window: " + str(count))

        mainScreen.refresh()
    # 退出按键
    elif ch == KEY_BOARD_ESC:
        break

# 退出curses环境
curses.endwin()
