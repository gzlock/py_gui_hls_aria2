import os
import subprocess
import threading
import time
import tkinter
from sys import platform

import aria2p
import psutil

import resource_path
from ui_log import Frame


class CoreAria2c:
    def __init__(self, logger: Frame, active: tkinter.IntVar):
        self.__popen: subprocess.Popen = None
        self.__is_running = False
        self.__loop_is_running = False
        self.__logger = logger
        self.__api: aria2p.API = None
        self.__port: int = None
        self.__active = active

    @property
    def activity(self):
        return self.__active

    @property
    def api(self) -> aria2p.API:
        return self.__api

    @property
    def is_running(self) -> bool:
        return self.__is_running

    @property
    def port(self) -> int:
        return self.__port

    def start(self, dir: str, proxy: str):
        self.__is_running = True
        self.__loop_is_running = True
        self.__start_aria2c(dir, proxy)
        threading.Thread(target=self.__loop).start()

    def stop(self):
        self.__loop_is_running = False
        time.sleep(1)

    @staticmethod
    def __get_open_port() -> int:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    def __start_aria2c(self, dir: str, proxy: str):
        self.__port = port = CoreAria2c.__get_open_port()
        parameter = ' --enable-rpc --rpc-listen-port=%d --rpc-secret=123456' \
                    ' --split=2' \
                    ' --max-connection-per-server=16' \
                    ' --max-concurrent-downloads=10' \
                    ' --lowest-speed-limit=10k' \
                    ' --auto-file-renaming=false --allow-overwrite=true' \
                    ' --rpc-allow-origin-all=true --rpc-listen-all=true' \
                    ' --dir=%s' % (port, dir)
        if proxy and len(proxy) > 0:
            parameter += ' --all-proxy=%s' % proxy
        if platform == 'win32':
            command = os.path.join('binary', 'win', 'aria2c.exe')
        else:
            command = os.path.join('binary', 'darwin', 'aria2c')
        command = resource_path.path(command)
        print('启动命令 %s' % command + parameter)
        self.__popen = subprocess.Popen(command + parameter, shell=True, )
        self.__api = aria2p.API(aria2p.Client(port=port, secret='123456', timeout=2))
        if platform != 'win32':
            time.sleep(2)
        self.__logger.log('Aria2c版本：%s' % self.__api.client.get_version()['version'])
        self.__logger.log('Aria2c端口：%d\nAria2c密钥：%s' % (port, '123456'))

    def __loop(self):
        options = self.__api.get_global_options()
        print('保存目录', options.dir)
        while self.__loop_is_running:
            '''获取因为下载速度低于10K被暂停的任务
            用代码手动恢复下载'''
            self.__api.resume_all()
            self.__active.set(len(self.__api.client.tell_active()))
            time.sleep(0.5)
        self.kill()
        self.__active.set(0)
        self.__is_running = False

    def kill(self):
        process = psutil.Process(self.__popen.pid)
        for proc in process.children(recursive=True):
            proc.kill()
        process.kill()
