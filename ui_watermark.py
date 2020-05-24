import glob
import multiprocessing
import os
import threading
import tkinter
from tkinter import ttk, messagebox

import my_cache
import utils
import watermark
from my_entry import MyEntry
from ui import Frame


class WatermarkWindow(Frame):
    def __init__(self, dir: str) -> None:
        super().__init__()
        self.__dir = dir
        self.__is_doing = False
        self.__win = win = tkinter.Toplevel()
        win.grab_set()
        win.title('添加文字水印')
        self.__ui_frame = frame = ttk.Label(win)
        frame.pack(fill=tkinter.BOTH, pady=5)

        # 水印文本
        frame = ttk.Label(frame)
        frame.pack(fill=tkinter.BOTH, pady=5)
        self.__watermark = tkinter.StringVar()
        my_cache.tkVariable(self.__watermark, 'watermark_text')
        ttk.Label(frame, text='输入文本', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        MyEntry(frame, textvariable=self.__watermark).pack(fill=tkinter.X)

        # 碎片文件总量
        frame = ttk.Label(self.__ui_frame)
        frame.pack(fill=tkinter.BOTH, pady=5)
        self.__total = total = len(glob.glob(os.path.join(dir, '*.ts')))
        ttk.Label(frame, text='视频碎片数量', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        ttk.Label(frame, text=str(total) + ' 个文件').pack(side=tkinter.LEFT)

        # 碎片比列
        frame = ttk.Label(self.__ui_frame)
        frame.pack(fill=tkinter.BOTH, pady=5)
        self.__watermark_count = tkinter.IntVar()
        my_cache.tkVariable(self.__watermark_count, 'watermark_count')
        ttk.Label(frame, text='随机给', width=Frame.LABEL_WIDTH, anchor=tkinter.E) \
            .pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        MyEntry(frame, textvariable=self.__watermark_count, width=5) \
            .pack(side=tkinter.LEFT)
        ttk.Label(frame, text='个视频碎片加水印', anchor=tkinter.E).pack(side=tkinter.LEFT, padx=Frame.LABEL_PADDING)
        ttk.Button(self.__ui_frame, text='确认', command=self.doit).pack()
        ttk.Button(self.__ui_frame, text='还原视频碎片', command=self.undo).pack(pady=10)

        # 工作中的提示
        self.__ui_doing = frame = ttk.Frame(win)
        ttk.Label(frame, text='正在添加水印，请稍候', font=('times', 20, 'bold')).pack()

        win.after(100, utils.move_to_screen_center, win)

    def undo(self):
        watermark.undo(self.__dir)

    def doit(self):
        threading.Thread(target=self.__doit).start()

    def __doit(self):
        if not self.__watermark.get():
            messagebox.showerror(message='请输入水印文本')
            return
        try:
            int(self.__watermark_count.get())
        except Exception as e:
            messagebox.showerror(message='不是标准的自然数')
            return

        if self.__watermark_count.get() <= 0:
            messagebox.showerror(message='文件为零不工作')
            return
        if self.__watermark_count.get() > self.__total:
            messagebox.showerror(message='大于文件总量')
            return
        self.__is_doing = True
        self.__win.protocol("WM_DELETE_WINDOW", self.close)
        self.__ui_frame.pack_forget()
        self.__ui_doing.pack()
        self.__pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        watermark.undo(dir=self.__dir)
        watermark.watermark(dir=self.__dir, watermark=self.__watermark.get(), pool=self.__pool,
                            count=self.__watermark_count.get())
        self.__ui_frame.pack()
        self.__ui_doing.pack_forget()
        self.__win.grab_release()
        self.__win.protocol("WM_DELETE_WINDOW", self.nothing)
        self.__is_doing = False

    def close(self):
        if self.__is_doing and messagebox.askokcancel('警告', '正在添加水印中，关闭这个窗口将会中断工作'):
            self.__pool.terminate()
            self.__win.destroy()

    def nothing(self):
        self.__win.destroy()
