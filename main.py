import tkinter
from multiprocessing import freeze_support
from sys import platform
from tkinter import messagebox
from tkinter.ttk import Frame

import my_cache
import resource_path
import ui_aria2
import ui_buttons
import ui_log
import ui_m3u8
from core import Core
from ui_menu import Menu


def start_aria2c():
    pass


class Window:
    def __init__(self):
        self.__is_start = False
        self.__root = root = tkinter.Tk()
        root.title('HLS录制程序')
        Menu(root)
        print('app目录', resource_path.path('./'))
        # 设置windows窗口图标
        if platform == 'win32':
            icon = resource_path.path('icon.ico')
            # print('icon', icon)
            root.iconbitmap(icon)

        root.minsize(450, 450)
        frame = Frame(root)
        frame.config(padding=5)
        frame.pack(fill=tkinter.BOTH, expand=True)
        self.__ui_m3u8 = m3u8 = ui_m3u8.Frame(root=frame, cache=my_cache)
        self.__ui_aria2 = aria2 = ui_aria2.Frame(root=frame, cache=my_cache)
        self.__ui_log = log = ui_log.Frame(root=frame)
        self.__ui_buttons = ui_buttons.Frame(root=frame,
                                             on_click_start=self.start,
                                             on_click_stop=self.stop,
                                             on_click_merge_video=self.merge_video)
        log.pack()

        self.__core: Core = Core(
            log=log,
            m3u8_src=m3u8.m3u8_src,
            m3u8_proxy=m3u8.m3u8_proxy,
            aria2_dir=aria2.dir,
            aria2_max_concurrent=aria2.max_concurrent,
            aria2_proxy=aria2.aria2_proxy,
        )

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        root.mainloop()

    def on_closing(self):
        if self.__core.is_running():
            if messagebox.askokcancel('警告', '正在录制，确认退出？'):
                self.__core.stop()
                self.__root.destroy()
        else:
            self.__root.destroy()

    def start(self):
        if len(self.__ui_aria2.dir.get()) == 0:
            messagebox.showerror(title='错误', message='请选择存放文件夹')
            return

        self.__ui_m3u8.disable()
        self.__ui_aria2.disable()
        self.__ui_buttons.disable()

        try:
            self.__core.start()
        except Exception as e:
            self.__ui_m3u8.disable(False)
            self.__ui_aria2.disable(False)
            self.__ui_buttons.disable(False)
            messagebox.showerror(title='M3u8源读取错误', message=e)
            return

        self.__ui_aria2.turn_on()

    def stop(self):
        self.__core.stop()
        self.__ui_aria2.turn_off()
        self.__ui_m3u8.disable(False)
        self.__ui_aria2.disable(False)
        self.__ui_buttons.disable(False)

    def merge_video(self):
        print('merge video')


if __name__ == '__main__':
    freeze_support()
    Window()
