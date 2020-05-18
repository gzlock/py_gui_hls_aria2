import os
import subprocess
from sys import platform
from urllib.parse import urlparse


def has_ffmpeg() -> bool:
    if platform == 'win32':
        p = subprocess.Popen('ffmpeg -version', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        msg = out.decode()
        p.terminate()
    else:
        p = subprocess.Popen('ffmpeg -version', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=popen_env())
        out, err = p.communicate()
        msg = out.decode()
        p.terminate()
    return 'ffmpeg version' in msg


def is_url(_url: str) -> bool:
    _url = urlparse(_url)
    if _url.scheme not in ['http', 'https'] or len(_url.netloc) < 5:
        return False
    return True


def move_to_screen_center(target):
    width = target.winfo_screenwidth()
    height = target.winfo_screenheight()
    w = target.winfo_width() + 1
    h = target.winfo_height() + 1
    x = int((width - w) / 2)
    y = int((height - h) / 2)
    target.geometry('{}x{}+{}+{}'.format(w, h, x, y))
    target.update()
    pass


def popen_env() -> dict:
    env = os.environ.copy()
    env['PATH'] = '/usr/local/bin:' + env['PATH']
    return env
