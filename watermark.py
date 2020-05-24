import glob
import json
import multiprocessing
import os
import random
import subprocess
import sys

import resource_path


class VideoTask:
    def __init__(self, file: str, watermark, codec_name: str, profile: str, level: str):
        self.file = file
        self.watermark = watermark
        self.codec_name = codec_name
        self.profile = profile
        self.level = level


def watermark(dir: str, watermark: str, pool: multiprocessing.Pool, count: int):
    ts_files = glob.glob(os.path.join(dir, "*.ts"), recursive=True)
    count = count if count < len(ts_files) else len(ts_files)
    sorted(ts_files)
    random.shuffle(ts_files)

    add_watermark_files = ts_files[:count]
    print('要加水印的片段', add_watermark_files)
    stream = get_video_stream(ts_files[0])
    codec_name = stream['codec_name']
    profile = stream['profile']
    level = stream['level']
    for file in add_watermark_files:
        pool.apply_async(func=process, args=(VideoTask(file=file,
                                                       watermark=watermark,
                                                       codec_name=codec_name,
                                                       level=level,
                                                       profile=profile),))
    pool.close()
    pool.join()


def get_video_stream(file: str):
    parameter = ' -v quiet -select_streams v:0 -print_format json -show_streams %s' % file
    if sys.platform == 'win32':
        command = os.path.join('binary', 'win', 'ffprobe.exe')
    else:
        command = os.path.join('binary', 'darwin', 'ffprobe')
    command = resource_path.path(command) + parameter
    print('水印', command)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    streams = json.loads(out)['streams']
    print('streams length: %d' % len(streams))
    streams = list(filter(lambda stream: stream['codec_type'] == 'video', streams))
    if not streams:
        return None
    return streams[0]


def rename(file: str) -> str:
    path = list(os.path.split(file))
    path[1] = '%s_' % path[1]
    return os.path.join(*path)


def process(task: VideoTask):
    old_file = rename(task.file)
    new_file = task.file
    # 先备份文件
    os.rename(new_file, old_file)
    top = random.choice([True, False])
    left = random.choice([True, False])
    x = str(random.randint(10, 100))
    y = str(random.randint(10, 100))
    if not left:
        x = 'W-text_w-%s' % x
    if not top:
        y = 'H-text_h-%s' % y
    # print('加水印前', stream)
    command = 'ffmpeg -i {input} ' \
              '-vf "drawtext=text=\'{watermark}\'' \
              ':x={x}:y={y}:fontsize=20:fontcolor=white:shadowcolor=black:shadowx=2:shadowy=2" ' \
              '-c:a copy -c:v {codec_name} -profile {profile} -level {level} ' \
              '{output} -y'.format(input=old_file,
                                   watermark=task.watermark, x=x, y=y,
                                   codec_name=task.codec_name, profile=task.profile, level=task.level,
                                   output=new_file)
    print('command %s' % command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    # print('输出 %s' % out)
    # print('加水印后', get_video_stream(file))


def undo(dir: str):
    files = glob.glob(os.path.join(dir, '*.ts_'), recursive=True)
    for file in files:
        os.replace(file, file[:-1])


if __name__ == '__main__':
    undo('/Volumes/HDD/玩很大')
