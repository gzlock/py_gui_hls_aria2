import multiprocessing
import os
import subprocess
import threading
import time
from sys import platform

import aria2p

import utils


def startup_aria2() -> subprocess.Popen:
    parameter = ' --enable-rpc --rpc-listen-port=2333 --rpc-secret=123456 --rpc-allow-origin-all=true --rpc-listen-all=true'
    if platform == 'win32':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        command = 'binary/win/aria2c.exe'
        command = os.path.join('.', 'binary', 'win', 'aria2c.exe')
        command = command + parameter
        print('启动命令', command)
        return subprocess.Popen(command, env=utils.popen_env(), shell=True, startupinfo=si)
    else:
        return subprocess.Popen('./binary/darwin/aria2c' + parameter,
                                env=utils.popen_env(),
                                shell=True)


def connect_aria2():
    for i in range(10):
        time.sleep(2)
        aria2 = aria2p.Client(port=2333, secret='123456', timeout=2)
        print('aria2 version', aria2.get_version()['version'])


def new_thread():
    print('thread pid', os.getpid())
    a = 0
    while True:
        a += 1
        print(a)
        time.sleep(1)


if __name__ == '__main__':
    print('main pid', os.getpid())
    t = multiprocessing.Process(target=new_thread)
    t.start()
    time.sleep(5)
    t.kill()

if __name__ == '__main__1':
    p = startup_aria2()
    print('pid', p.pid)
    thread = threading.Thread(target=connect_aria2)
    thread.start()
    thread.join()
