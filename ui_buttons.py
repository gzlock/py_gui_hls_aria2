import tkinter
from tkinter import ttk


class Frame:
    def __init__(self, root, on_click_start, on_click_stop, on_click_merge_video):
        self.root = root
        self.layout = layout = ttk.LabelFrame(root, text='控制区')
        layout.config(padding=5)
        layout.pack(fill=tkinter.BOTH, pady=5)

        # 启动按钮
        self.start_btn = start_btn = ttk.Button(layout, text='开始录制', command=on_click_start)
        start_btn.pack(side=tkinter.LEFT)

        # 停止按钮
        self.stop_btn = stop_btn = ttk.Button(layout, text='停止录制', command=on_click_stop, state=tkinter.DISABLED)
        stop_btn.pack(side=tkinter.LEFT, padx=5, pady=5)

        # 合并视频按钮
        ttk.Button(layout, text='合并视频', command=on_click_merge_video).pack(side=tkinter.LEFT, padx=5, pady=5)

    def disable(self, disabled: bool = True):
        if disabled:
            self.start_btn.config(state=tkinter.DISABLED)
            self.stop_btn.config(state=tkinter.NORMAL)
        else:
            self.start_btn.config(state=tkinter.NORMAL)
            self.stop_btn.config(state=tkinter.DISABLED)
