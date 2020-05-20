import os
import subprocess
import time
import tkinter
from glob import glob
from sys import platform
from tkinter import messagebox

from appdirs import unicode

import resource_path
import utils


def merge_ts_to_mp4(dir: str):
    dir = os.path.abspath(dir)
    files = ["file '" + f + "'\n" for f in glob(os.path.join(dir, "*.ts"), recursive=True)]
    if len(files) == 0:
        messagebox.showerror(title='错误', message='没有视频碎片')
        return
    list.sort(files)
    file_list = os.path.join(dir, 'list.txt')
    with open(file_list, 'w+') as file:
        file.writelines(files)

    if platform == 'win32':
        command = resource_path.path(os.path.join('binary', 'win', 'ffmpeg.exe'))
    else:
        command = resource_path.path(os.path.join('binary', 'darwin', 'ffmpeg'))
    target = time.strftime("%Y-%m-%d_%H_%M_%S", time.localtime()) + '.mp4'
    target = os.path.join(dir, target)
    command = '%s -f concat -safe 0 -i %s -c copy %s -y' \
              % (command, file_list, target)

    print(command)
    process = subprocess.Popen(command, shell=True)
    win = tkinter.Toplevel()
    tkinter.Label(win, text='正在合并视频文件中，请稍候', font=('times', 20, 'bold')).pack(padx=10, pady=10)
    win.resizable(0, 0)
    win.after(100, utils.move_to_screen_center, win)

    def check():
        return_code = process.poll()
        if return_code is None:
            win.after(1000, check)
            return

        win.grab_release()
        win.destroy()
        if return_code == 0:
            if messagebox.askyesno('合并文件成功', '是否打开文件夹？'):
                if platform == 'win32':
                    os.startfile(target)
                    # subprocess.Popen('explorer /select,"{}"'.format(final_mp4_path))
                else:
                    subprocess.Popen(['open', '-R', target])
        else:
            messagebox.showinfo('合并视频文件错误', process.stdout.read())

    win.after(100, check)

    def on_closing():
        if messagebox.askokcancel('警告', '正在合并视频，关闭这个窗口将会中断合并视频'):
            process.kill()
            win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_closing)

    win.grab_set()
