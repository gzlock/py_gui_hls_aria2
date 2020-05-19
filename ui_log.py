import tkinter
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from typing import List, Tuple


class Frame:
    def __init__(self, root):
        self.layout = layout = ttk.LabelFrame(root, text='日志')
        layout.config(padding=5)

        self.__logs: List[Tuple[str, int]] = []
        self.__current_line = 0

        # 日志文本框
        frame = ttk.Frame(layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        self.__log_view = ScrolledText(frame,
                                       state=tkinter.DISABLED,
                                       wrap=tkinter.WORD,
                                       )
        self.__log_view.pack(fill=tkinter.BOTH)
        self.__log_view.bind("<1>", lambda event: self.__log_view.focus_set())
        self.__log_view.tag_config('log', foreground='black')
        self.__log_view.tag_config('error', foreground='red')

        # 功能按钮
        frame = ttk.Frame(layout, height=10)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Button(frame, text='清空日志', command=self.clear).pack(side=tkinter.LEFT)
        self.__is_scroll_to_bottom = tkinter.IntVar(value=1)
        ttk.Checkbutton(frame, text='自动滚动到底部', variable=self.__is_scroll_to_bottom).pack(side=tkinter.LEFT)

    def pack(self):
        self.layout.pack(fill=tkinter.BOTH, pady=5)

    def log(self, msg: str):
        # print('log', msg)
        self.__logs.append((msg, 0))
        self.__display_log()

    def error(self, msg: str):
        # print('error', msg)
        self.__logs.append((msg, 1))
        self.__display_log()

    def clear(self):
        self.__logs.clear()
        self.__current_line = 0
        self.__log_view.config(state=tkinter.NORMAL)
        self.__log_view.delete(1.0, tkinter.END)
        self.__log_view.config(state=tkinter.DISABLED)

    def __display_log(self):
        lines = self.__logs[self.__current_line:]
        if lines:
            self.__current_line += len(lines)
            self.__log_view.config(state=tkinter.NORMAL)
            for line in lines:
                self.__log_view.insert(tkinter.END, line[0] + '\n', 'log' if line[1] == 0 else 'error')
            self.__log_view.config(state=tkinter.DISABLED)

        if self.__is_scroll_to_bottom.get() == 1:
            self.__log_view.see('end')
