import tkinter
from multiprocessing import freeze_support
from sys import platform
from tkinter import messagebox
from tkinter.ttk import Frame
from typing import List

import my_cache
import resource_path
import ui_aria2
import ui_buttons
import ui_log
import ui_m3u8
from core_aria2 import CoreAria2
from core_m3u8 import CoreM3u8
from ui_menu import Menu


class Window:
    def __init__(self):
        self.__is_start = False
        self.__core_m3u8: CoreM3u8 = None
        self.__core_aria2: CoreAria2 = None
        self.__root = root = tkinter.Tk()
        root.title('HLS录制程序')
        Menu(root)
        print('app目录', resource_path.path('./'))
        # 设置windows窗口图标
        if platform == 'win32':
            icon = resource_path.path('icon.ico')
            print('icon', icon)
            root.iconbitmap(icon)

        root.minsize(450, 450)
        frame = Frame(root)
        frame.config(padding=5)
        frame.pack(fill=tkinter.BOTH, expand=True)
        self.__m3u8 = m3u8 = ui_m3u8.Frame(root=frame, cache=my_cache)
        self.__aria2 = aria2 = ui_aria2.Frame(root=frame, cache=my_cache)
        self.__log = log = ui_log.Frame(root=frame)
        self.__buttons = ui_buttons.Frame(root=frame,
                                          on_click_start=self.start,
                                          on_click_stop=self.stop,
                                          on_click_merge_video=self.merge_video)
        log.pack()

        def watch_max_concurrent(*args):
            print('动态改变 任务数量', aria2.max_concurrent.get())
            if self.__core_aria2:
                self.__core_aria2.set_concurrent(aria2.max_concurrent.get())

        aria2.max_concurrent.trace('w', watch_max_concurrent)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        root.mainloop()

    def on_closing(self):
        if self.__is_start:
            if messagebox.askokcancel('警告', '转播程序正在工作，确认退出？'):
                self.__root.destroy()
        else:
            self.__root.destroy()

    def start(self):
        self.__root.after_idle(self.__start)

    def __start(self):
        if len(self.__aria2.dir.get()) == 0:
            messagebox.showerror(title='错误', message='请选择存放文件夹')
            return
        self.__m3u8.disable()
        self.__aria2.disable()
        self.__buttons.disable()

        self.__core_m3u8 = CoreM3u8(url=self.__m3u8.m3u8_src.get(),
                                    m3u8_proxy=self.__m3u8.m3u8_proxy.get(),
                                    log=self.__log,
                                    callback=self.download_segments,
                                    )
        try:
            self.__core_m3u8.load_m3u8_content()
        except Exception as e:
            self.__m3u8.disable(False)
            self.__aria2.disable(False)
            self.__buttons.disable(False)
            messagebox.showerror(title='M3u8源读取错误', message=e)
            return

        self.__is_start = True
        # 启动aria2
        self.__core_aria2 = CoreAria2(log=self.__log)
        self.__core_aria2.start(self.__aria2.dir.get())

        # 开始循环读取m3u8
        self.__core_m3u8.start()

        self.__aria2.turn_on()

    def stop(self):
        self.__is_start = False
        self.__core_aria2.stop()
        self.__core_aria2 = None
        self.__core_m3u8.stop()
        self.__core_m3u8 = None
        self.__aria2.turn_off()
        self.__m3u8.disable(False)
        self.__aria2.disable(False)
        self.__buttons.disable(False)

    def download_segments(self, urls: List[str]):
        if self.__core_aria2 is None:
            return
        for url in urls:
            self.__log.log('新碎片\n' + url)
        self.__core_aria2.add_uris(urls)

    def merge_video(self):
        print('merge video')


if __name__ == '__main__':
    freeze_support()
    Window()
