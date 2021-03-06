import os
import subprocess
import tkinter
from sys import platform
from tkinter import ttk, messagebox, filedialog, Canvas
from typing import Callable

import my_cache
from my_entry import MyEntry
from ui import Frame as baseFrame


class Frame(baseFrame):

    def __init__(self, root,
                 cache: my_cache,
                 on_click_start_aria2c: Callable,
                 on_click_stop_aria2c: Callable,
                 on_click_open_aria2c: Callable):
        super().__init__()

        self.layout = layout = ttk.LabelFrame(root, text='Aria2功能区域')
        layout.config(padding=5)
        layout.pack(fill=tkinter.BOTH, pady=5)

        # 目录选择
        frame = ttk.Frame(layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Label(frame, text='存放目录*', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        self.dir = tkinter.StringVar()
        cache.tkVariable(self.dir, 'local_dir')
        MyEntry(frame, state='readonly', textvariable=self.dir).pack(fill=tkinter.X, side=tkinter.LEFT, expand=True)

        # 打开目录和选择目录 两个按钮
        frame = ttk.Frame(self.layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Button(frame, text='选择目录', command=self.__select_folder).pack(side=tkinter.RIGHT, padx=2)

        button = ttk.Button(frame, text='打开目录', command=self.__open_video_dir)
        button.pack(side=tkinter.RIGHT, padx=2)
        self.without_disable.append(button)

        # 代理输入框
        frame = ttk.Frame(self.layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Label(frame, text='网络代理', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        self.aria2_proxy = tkinter.StringVar()
        cache.tkVariable(self.aria2_proxy, 'aria2_proxy')
        MyEntry(frame, textvariable=self.aria2_proxy).pack(fill=tkinter.BOTH, expand=True)

        # aria2的状态显示
        frame = ttk.Frame(self.layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Label(frame, text='Aria2状态', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        self.__state_canvas = Canvas(frame, width=14, height=14, bd=0, highlightthickness=0, relief=tkinter.FLAT,
                                     borderwidth=0)
        self.__state_canvas.pack(side=tkinter.LEFT)
        self.__change_color(fill='red')

        # # 下载中
        # frame = ttk.Frame(self.layout)
        # frame.pack(fill=tkinter.BOTH, pady=5)
        # ttk.Label(frame, text='正在下载', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
        #     .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        # self.active = tkinter.IntVar(value=0)
        # ttk.Label(frame, textvariable=self.active).pack(side=tkinter.LEFT)
        #
        # # 等待中
        # frame = ttk.Frame(self.layout)
        # frame.pack(fill=tkinter.BOTH, pady=5)
        # ttk.Label(frame, text='等候下载', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
        #     .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        # self.waiting = tkinter.IntVar(value=0)
        # ttk.Label(frame, textvariable=self.waiting).pack(side=tkinter.LEFT)
        #
        # # 已完成
        # frame = ttk.Frame(self.layout)
        # frame.pack(fill=tkinter.BOTH, pady=5)
        # ttk.Label(frame, text='已经完成', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
        #     .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        # self.stopped = tkinter.IntVar(value=0)
        # ttk.Label(frame, textvariable=self.stopped).pack(side=tkinter.LEFT)

        # 启动Aria2c
        frame = ttk.Frame(self.layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Button(frame, text='启动Aria2c', command=on_click_start_aria2c).pack(side=tkinter.LEFT)

        # 杀掉Aria2c
        btn = ttk.Button(frame, text='停止Aria2c', command=on_click_stop_aria2c)
        btn.pack(side=tkinter.LEFT)
        self.without_disable.append(btn)

        # 打开Aria2c webui
        btn = ttk.Button(frame, text='Aria2管理页面', command=on_click_open_aria2c)
        btn.pack(side=tkinter.LEFT)
        self.without_disable.append(btn)

    def turn_on(self):
        self.__change_color('green')

    def turn_off(self):
        self.__change_color('red')

    def save_dir(self):
        return self.dir.get()

    def __change_color(self, fill: str):
        self.__state_canvas.create_rectangle(0, 0, 20, 20, fill=fill)

    def __select_folder(self):
        dir = filedialog.askdirectory(title='选择要存放视频的目录')
        if len(dir) > 0:
            self.dir.set(dir)

    def __open_video_dir(self):
        dir = self.dir.get()
        if len(dir) == 0:
            return messagebox.showerror('错误', '没有选择视频存放的文件夹')
        if not os.path.exists(dir):
            return messagebox.showerror('错误', '不存在的文件夹，无法打开')

        if platform == 'win32':
            os.startfile(dir)
        elif platform == 'darwin':
            subprocess.Popen(['open', dir])
