#!/usr/bin/python
# -*- coding=utf-8 -*-

import tkinter
import webbrowser
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
from core_aria2c import CoreAria2c
from core_m3u8 import CoreM3u8
from ffmpeg import merge_ts_to_mp4
from ui_menu import Menu
from window_watermark import WatermarkWindow


class Window:
    def __init__(self):
        self.__root = root = tkinter.Tk()
        root.title('HLS录制程序')
        Menu(root)
        print('app目录', resource_path.path(''))
        # 设置windows窗口图标
        if platform == 'win32':
            icon = resource_path.path('icon.ico')
            print('icon', icon)
            root.iconbitmap(icon)

        root.minsize(450, 450)
        frame = Frame(root)
        frame.config(padding=5)
        frame.pack(fill=tkinter.BOTH, expand=True)
        self.__ui_m3u8 = m3u8 = ui_m3u8.Frame(root=frame, cache=my_cache)
        self.__ui_aria2 = aria2 = ui_aria2.Frame(root=frame, cache=my_cache,
                                                 on_click_start_aria2c=self.start_aria2c,
                                                 on_click_stop_aria2c=self.stop_aria2c,
                                                 on_click_open_aria2c=self.open_aria2c_webui)
        self.__ui_log = log = ui_log.Frame(root=frame)
        self.__ui_buttons = ui_buttons.Frame(root=frame,
                                             on_click_start=self.start,
                                             on_click_stop=self.stop,
                                             on_click_merge_video=self.merge_video,
                                             on_click_watermark=self.watermark)
        log.pack()

        self.__core_m3u8: CoreM3u8 = None
        self.__core_aria2c: CoreAria2c = CoreAria2c(logger=log)

        root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # threading.Thread(target=self.loop_check).start()
        self.loop_check()
        root.mainloop()

    def start_aria2c(self):
        if self.__core_aria2c.is_running:
            return
        self.__ui_log.log('正在启动Aria2c')
        self.__ui_aria2.disable()
        self.__core_aria2c.start(dir=self.__ui_aria2.dir.get(), proxy=self.__ui_aria2.aria2_proxy.get())
        self.__ui_aria2.turn_on()
        self.__ui_aria2.disable()
        self.__ui_log.log('成功启动Aria2c')

    def stop_aria2c(self):
        if self.__core_aria2c.is_running:
            self.__ui_log.log('正在停止Aria2c')
            self.__core_aria2c.stop()
            self.__ui_aria2.disable(False)
            self.__ui_aria2.turn_off()
            self.__ui_log.log('成功停止Aria2c')

    def watermark(self):
        dir = self.__ui_aria2.dir.get()
        if dir:
            WatermarkWindow(dir=dir, root=self.__root)

    def open_aria2c_webui(self):
        if self.__core_aria2c.is_running:
            webbrowser.open(
                'https://ziahamza.github.io/webui-aria2/'
                '?host=127.0.0.1&port={port}&token={token}'.format(port=self.__core_aria2c.port, token=123456))

    def on_closing(self):
        if self.__core_m3u8 and self.__core_m3u8.is_running:
            if not messagebox.askokcancel('警告', '正在录制，确认退出？'):
                return
            self.__core_m3u8.stop()
        self.__core_aria2c.stop()
        self.__root.destroy()

    def start(self):
        if len(self.__ui_m3u8.m3u8_src.get()) == 0:
            messagebox.showerror(title='错误', message='请填写m3u8资源网址')
            return
        if len(self.__ui_aria2.dir.get()) == 0:
            messagebox.showerror(title='错误', message='请选择存放文件夹')
            return

        self.__ui_m3u8.disable()
        self.__ui_buttons.disable()

        if not self.__core_aria2c.is_running:
            self.start_aria2c()

        self.__core_m3u8 = CoreM3u8(
            logger=self.__ui_log,
            m3u8_src=self.__ui_m3u8.m3u8_src.get(),
            m3u8_proxy=self.__ui_m3u8.m3u8_proxy.get(),
            api=self.__core_aria2c.api,
        )

        try:
            self.__core_m3u8.load_m3u8()
        except Exception as e:
            self.__ui_m3u8.disable(False)
            self.__ui_buttons.disable(False)
            messagebox.showerror(title='M3u8源读取错误', message=e)
            raise e
        self.__core_m3u8.start()

        self.__ui_aria2.turn_on()

    def stop(self):
        self.__core_m3u8.stop()
        self.__ui_m3u8.disable(False)
        self.__ui_buttons.disable(False)

        if messagebox.askyesno(message='是否停止Aria2c？'):
            self.stop_aria2c()

    def merge_video(self):
        merge_ts_to_mp4(self.__ui_aria2.dir.get(), test=False)

    def loop_check(self):
        """每秒检查运行状态"""
        if self.__core_m3u8:
            self.__ui_buttons.disable(self.__core_m3u8.is_running)
            self.__ui_m3u8.disable(self.__core_m3u8.is_running)

        self.__root.after(ms=2000, func=self.loop_check)


if __name__ == '__main__':
    freeze_support()
    Window()
