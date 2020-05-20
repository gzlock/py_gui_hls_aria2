import tkinter
from tkinter import ttk

import my_cache
from my_entry import MyEntry
from ui import Frame as baseFrame


class Frame(baseFrame):
    LABEL_WIDTH = 10

    def __init__(self, root, cache: my_cache):
        super().__init__()

        self.layout = layout = ttk.LabelFrame(root, text='HLS m3u8设置')
        layout.config(padding=5)
        layout.pack(fill=tkinter.BOTH, pady=5)

        # 直播源 输入框
        frame = ttk.Frame(layout)
        frame.pack(fill=tkinter.BOTH, pady=2)

        ttk.Label(frame, text='m3u8源*', width=Frame.LABEL_WIDTH, anchor=tkinter.E).pack(side=tkinter.LEFT)
        self.m3u8_src = tkinter.StringVar()
        cache.tkVariable(self.m3u8_src, 'm3u8_src')
        MyEntry(frame, textvariable=self.m3u8_src).pack(fill=tkinter.BOTH, expand=True)

        # 代理输入框
        frame = ttk.Frame(self.layout)
        frame.pack(fill=tkinter.BOTH, pady=5)
        ttk.Label(frame, text='网络代理', width=Frame.LABEL_WIDTH, anchor=tkinter.E).pack(side=tkinter.LEFT)
        self.m3u8_proxy = tkinter.StringVar()
        cache.tkVariable(self.m3u8_proxy, 'm3u8_proxy')
        MyEntry(frame, textvariable=self.m3u8_proxy).pack(fill=tkinter.BOTH, expand=True)
