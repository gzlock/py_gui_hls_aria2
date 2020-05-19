import multiprocessing
import os
import subprocess
import threading
import time
import tkinter
from sys import platform
from typing import Set

import resource_path
from core_aria2 import CoreAria2
from core_m3u8 import CoreM3u8
from ui_log import Frame


def daemon_process_entry():
    # print('守护进程', os.getpid())
    # self.__log.log('正在启动Aria2c，端口:{} 密钥:{}'.format(2333, '123456'))
    parameters = ' --daemon --enable-rpc --rpc-listen-port={} --rpc-secret={}' \
                 ' --rpc-allow-origin-all=true --rpc-listen-all=true' \
                 ' --stop-with-process={}' \
        .format(2333, '123456', str(os.getpid()))
    if platform == 'win32':
        command = os.path.join('binary', 'win', 'aria2c.exe')
        command = resource_path.path(command) + parameters
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.Popen(command, env=None, shell=True, startupinfo=si, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, )
    else:
        command = os.path.join('binary', 'darwin', 'aria2c')
        command = resource_path.path(command) + parameters
        subprocess.Popen(command, env=None, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, )
    # print('Aria2启动命令', command)
    count = 0
    while True:
        # print('守护进程工作中', count)
        count += 1
        time.sleep(5)


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
        self.__aria2: CoreAria2 = CoreAria2(log=log)
        self.__log = log
        self.__hls_segments: Set[str] = set()
        self.__daemon_process = multiprocessing.Process
        aria2_max_concurrent.trace('w', lambda *args: self.__watch_aria2_input())

    def __watch_aria2_input(self):
        print('任务数量改变了：', self.__aria2_max_concurrent.get())
        self.__aria2.set_concurrent(self.__aria2_max_concurrent.get())

    def is_running(self):
        return self.__is_running

    def start(self):
        self.__m3u8 = CoreM3u8(url=self.__m3u8_src.get(), proxy=self.__m3u8_proxy.get())
        self.__hls_segments.update(self.__m3u8.load_m3u8_content())
        self.__daemon_process = multiprocessing.Process(target=daemon_process_entry)
        self.__daemon_process.start()
        threading.Thread(target=self.__start).start()

    def __start(self):
        # self.__aria2.start()
        time.sleep(2)
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
        print('线程结束', threading.get_ident())

    def stop(self):
        if self.__is_running:
            self.__aria2.stop()
            self.__daemon_process.kill()
        self.__is_running = False
