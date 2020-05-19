import os
import subprocess
import threading
import time
import tkinter.ttk
from sys import platform
from tkinter.scrolledtext import ScrolledText

import aria2p
import psutil


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


class W:
    def __init__(self):
        self.t: threading.Thread = None
        self.is_running = False
        root = tkinter.Tk()
        frame = tkinter.ttk.Frame(root, padding=20)
        frame.pack()
        tkinter.ttk.Button(frame, text='开始', command=self.start).pack()
        tkinter.ttk.Button(frame, text='停止', command=self.stop).pack(pady=20)
        self.__log = ScrolledText(frame)
        self.__log.pack()
        root.mainloop()

    def start(self):
        self.t = threading.Thread(target=self.aria2)
        self.t.start()

    def log(self, msg: str):
        self.__log.insert(tkinter.END, msg[0] + '\n')

    def stop(self):
        self.is_running = False

    def aria2(self):
        self.is_running = True
        parameter = ' -s4 -x16 --enable-rpc --rpc-listen-port=2333 --rpc-secret=123456' \
                    ' --rpc-allow-origin-all=true --rpc-listen-all=true'
        if platform == 'win32':
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            command = os.path.join('binary', 'win', 'aria2c.exe')
            command = command + parameter
            print('启动命令', command)
            # return subprocess.Popen(command, env=utils.popen_env(), shell=True, startupinfo=si)
        else:
            command = os.path.join('binary', 'darwin', 'aria2c')
        process = subprocess.Popen(command + parameter, shell=True)
        api = aria2p.API(aria2p.Client(port=2333, secret='123456', timeout=2))

        options = api.get_global_options()
        options.max_concurrent_downloads = 20
        options.all_proxy = 'http://127.0.0.1:8888'
        while self.is_running:
            self.log('api version' + api.client.get_version()['version'])
            options = api.get_global_options()
            self.log('api max-concurrent-downloads {}'.format(options.max_concurrent_downloads))
            self.log('api all-proxy {}'.format(options.all_proxy))
            time.sleep(2)
        print('结束任务')
        kill(process.pid)
        try:
            print('杀掉Aria2后查询version', api.client.get_version()['version'])
        except Exception as e:
            print('杀掉Aria2后查询version失败', e)


if __name__ == '__main__':
    W()
