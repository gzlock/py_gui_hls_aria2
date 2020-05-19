import multiprocessing
import threading
import time
import tkinter
from typing import Set

from core_aria2 import CoreAria2
from core_m3u8 import CoreM3u8
from ui_log import Frame


class Core:
    def __init__(self,
                 m3u8_src: tkinter.Variable,
                 m3u8_proxy: tkinter.Variable,
                 aria2_dir: tkinter.Variable,
                 aria2_max_concurrent: tkinter.Variable,
                 aria2_proxy: tkinter.Variable,
                 log: Frame):
        self.__m3u8_src = m3u8_src
        self.__m3u8_proxy = m3u8_proxy
        self.__aria2_dir = aria2_dir
        self.__aria2_max_concurrent = aria2_max_concurrent
        self.__aria2_proxy = aria2_proxy
        self.__is_running = False
        self.__m3u8: CoreM3u8 = None
        self.__aria2: CoreAria2 = CoreAria2()
        self.__log = log
        self.__hls_segments: Set[str] = set()
        self.__daemon_process = multiprocessing.Process
        aria2_max_concurrent.trace('w', lambda *args: self.__watch_aria2_input())

    def __watch_aria2_input(self):
        print('任务数量改变了：', self.__aria2_max_concurrent.get())
        self.__aria2.set_concurrent(self.__aria2_max_concurrent.get())

    def is_running(self):
        return self.__is_running

    def test_m3u8(self):
        self.__m3u8 = CoreM3u8(url=self.__m3u8_src.get(), proxy=self.__m3u8_proxy.get())
        self.__hls_segments.update(self.__m3u8.load_m3u8_content())

    def start(self):
        self.__aria2.start(log=self.__log)
        threading.Thread(target=self.__start).start()

    def __start(self):
        # time.sleep(2)
        self.__aria2.connect(dir=self.__aria2_dir.get(),
                             max_concurrent=self.__aria2_max_concurrent.get(),
                             all_proxy=self.__aria2_proxy.get())
        for url in self.__hls_segments:
            self.__aria2.add_uris([url])
        self.__is_running = True
        while self.__is_running:
            try:
                new = self.__m3u8.load_m3u8_content().difference(self.__hls_segments)
                if len(new) > 0:
                    self.__hls_segments.update(new)
                    for url in new:
                        self.__aria2.add_uris([url])
                        self.__log.log('新视频碎片：\n' + url)
                time.sleep(2)
            except Exception as e:
                self.__log.error('m3u8错误\n {}'.format(e))
        print('线程结束')

    def stop(self):
        if self.__is_running:
            self.__aria2.stop()
        self.__is_running = False

    def has_downloading(self) -> bool:
        return False if self.__aria2 is None else self.__aria2.has_downloading()
