import os

isDev = os.getenv('dev')

if isDev:
    print('开发环境')
else:
    print('产品环境')


def log(msg, clear: bool = False):
    if not isDev:
        return
    mode = 'w' if clear else 'a'
    path = os.path.join(os.path.expanduser('~'), 'Desktop', 'log.txt')
    print('桌面 目录', path)
    open(path, mode).write('{}\n'.format(msg))
