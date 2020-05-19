import os
import subprocess
from sys import platform

import aria2p

import resource_path
from ui_log import Frame


class CoreAria2:
    def __init__(self, log: Frame, port: int = 2333, secret: str = '123456', ):
        self.__log = log
        self.__port = port
        self.__secret = secret
        self.__aria2: aria2p.API = None
        self.__options: aria2p.Options = None
        self.__subprocess: subprocess.Popen = None
        print('CoreAria2.__init__', os.getpid())

    def start(self):
        self.__log.log('正在启动Aria2c，端口:{} 密钥:{}'.format(self.__port, self.__secret))
        parameters = ' --daemon  --enable-rpc --rpc-listen-port={} --rpc-secret={}' \
                     ' --rpc-allow-origin-all=true --rpc-listen-all=true' \
            .format(self.__port, self.__secret)
        if platform == 'win32':
            command = os.path.join('binary', 'win', 'aria2c.exe')
            command = resource_path.path(command) + parameters
            # si = subprocess.STARTUPINFO()
            # si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # self.__subprocess = subprocess.Popen(command, env=None, shell=True, startupinfo=si,
            #                                      stdin=subprocess.PIPE,
            #                                      stdout=subprocess.PIPE,
            #                                      stderr=subprocess.PIPE, )
        else:
            command = os.path.join('binary', 'darwin', 'aria2c')
            command = resource_path.path(command) + parameters

        self.__subprocess = subprocess.Popen(command, env=None, shell=True,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, )
        print('Aria2启动命令', command)

    def connect(self, dir: str, max_concurrent: int = 5, all_proxy: str = ''):
        self.__aria2 = aria2p.API(
            aria2p.Client(
                port=self.__port,
                secret=self.__secret,
                timeout=5,
            )
        )
        self.__options = aria2p.Options(api=self.__aria2,
                                        struct={
                                            'dir': dir,
                                            'max-concurrent-downloads': max_concurrent,
                                            'all-proxy': all_proxy
                                        })
        self.__aria2.set_global_options(self.__options)
        self.__log.log('成功启动Aria2c，版本：{}'.format(self.__aria2.client.get_version()['version']))
        # print('保存的目录', self.__aria2.client.get_global_option()['dir'])

    def stop(self):
        self.__log.log('正在停止Aria2c')
        self.__disconnect()
        if self.__subprocess is not None:
            self.__subprocess.terminate()
            self.__subprocess.kill()
            self.__subprocess = None
        self.__log.log('成功停止Aria2c')

    def __disconnect(self):
        if self.__aria2 is None:
            return
        self.__aria2.stop_listening()
        self.__aria2 = None
        self.__options = None

    def add_uris(self, uri):
        if self.__aria2 is None:
            return
        print('add uris', uri)
        self.__aria2.add_uris(uri)

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
