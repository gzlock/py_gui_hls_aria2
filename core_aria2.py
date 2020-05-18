import subprocess
import time
from sys import platform
from typing import List

import aria2p

import resource_path
import utils
from ui_log import Frame


class CoreAria2:
    def __init__(self, log: Frame, port: int = 2333, secret: str = '123456'):
        self.__log = log
        self.__port = port
        self.__secret = secret
        self.__process: subprocess.Popen = None
        self.__aria2: aria2p.API = None
        self.__options: aria2p.Options = None

    def start(self, dir: str):
        self.__log.log('正在启动Aria2c，端口:{} 密钥:{}'.format(self.__port, self.__secret))
        parameters = ' --enable-rpc --rpc-listen-port={} --rpc-secret={} --rpc-allow-origin-all=true --rpc-listen-all=true' \
            .format(self.__port, self.__secret)
        if platform == 'win32':
            command = resource_path.path('binary/win/aria2c.exe') + parameters
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.__process = subprocess.Popen(command, shell=True,
                                              stdin=subprocess.PIPE,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              startupinfo=si)
        else:
            command = resource_path.path('binary/darwin/aria2c') + parameters
            self.__process = subprocess.Popen(command, shell=True,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              env=utils.popen_env())
        print('Aria2启动命令', command)
        time.sleep(2)
        self.__connect(dir=dir)

    def stop(self):
        self.__log.log('正在停止Aria2')
        self.__disconnect()
        if self.__process is not None:
            self.__process.kill()
            self.__process = None
        self.__log.log('成功停止Aria2')

    def __connect(self, dir: str, max_concurrent: int = 5, all_proxy: str = ''):
        self.__aria2 = aria2p.API(
            aria2p.Client(host='http://127.0.0.1',
                          port=self.__port,
                          secret=self.__secret,
                          timeout=5, )
        )
        self.__options = aria2p.Options(api=self.__aria2,
                                        struct={
                                            'dir': dir,
                                            'max-concurrent-downloads': max_concurrent,
                                            'all-proxy': all_proxy
                                        })
        self.__aria2.set_global_options(self.__options)
        self.__log.log('成功启动Aria2，版本：{}'.format(self.__aria2.client.get_version()['version']))
        print('保存的目录', dir, self.__aria2.client.get_global_option()['dir'])

    def __disconnect(self):
        if self.__aria2 is None:
            return
        self.__aria2.stop_listening()
        self.__aria2 = None
        self.__options = None

    def add_uris(self, uris: List[str]):
        if self.__aria2 is None:
            return
        self.__aria2.add_uris(uris)

    def set_concurrent(self, value: int):
        if self.__options is None:
            return
        self.__options.max_concurrent_downloads = value

    def set_proxy(self, value: str):
        if self.__options is None:
            return
        self.__options.all_proxy = value

    def set_dir(self, value: str):
        if self.__options is None:
            return
        self.__options.dir = value
