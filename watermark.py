#!/usr/bin/python
# -*- coding=utf-8 -*-

import glob
import json
import multiprocessing
import os
import random
import subprocess
import sys

import log
import resource_path


class VideoTask:
    def __init__(self, dir: str,
                 ffmpeg: str,
                 file: str,
                 watermark,
                 codec_name: str,
                 profile: str,
                 level: str,
                 font: str):
        self.dir = dir
        self.ffmpeg = ffmpeg
        self.font = font
        self.file = file
        self.watermark = watermark
        self.codec_name = codec_name
        self.profile = profile
        self.level = level

    def __str__(self):
        return 'ffmpeg: {ffmpeg}\nfont: {font}\nfile: {file}\nwatermark: {watermark}' \
            .format(ffmpeg=self.ffmpeg, font=self.font, file=self.file, watermark=self.watermark)


def watermark(dir: str, watermark: str, pool: multiprocessing.Pool, count: int):
    # open('./log.txt', 'a').write('水印 文件夹 %s\n' % dir)
    ts_files = glob.glob(os.path.join(dir, "*.ts"), recursive=True)
    # open('./log.txt', 'a').write('碎片文件数量 %d\n' % len(ts_files))
    count = count if count < len(ts_files) else len(ts_files)
    sorted(ts_files)
    random.shuffle(ts_files)

    add_watermark_files = ts_files[:count]
    # print('要加水印的片段', add_watermark_files)
    log.log('要加水印的片段 %s' % add_watermark_files)
    stream = get_video_stream(ts_files[0])
    codec_name = stream['codec_name']
    profile = stream['profile']
    level = stream['level']
    if sys.platform == 'win32':
        ffmpeg = os.path.join('binary', 'win', 'ffmpeg.exe')
        font = 'C\\:/Windows/Fonts/msyh.ttc'
    else:
        ffmpeg = os.path.join('binary', 'darwin', 'ffmpeg')
        font = '/System/Library/Fonts/PingFang.ttc'
    ffmpeg = resource_path.path(ffmpeg)
    # open('./log.txt', 'a').write('水印文件数量 %d\n' % len(add_watermark_files))
    for file in add_watermark_files:
        # open('./log.txt', 'a').write('水印文件 %s \n' % file)
        task = VideoTask(dir=dir,
                         ffmpeg=ffmpeg, font=font, file=file,
                         watermark=watermark,
                         codec_name=codec_name,
                         level=level,
                         profile=profile
                         )
        # print(task)
        pool.apply_async(func=process, args=(task,))
    pool.close()
    pool.join()


def get_video_stream(file: str):
    parameter = ' -v quiet -select_streams v:0 -print_format json -show_streams %s' % file
    if sys.platform == 'win32':
        command = os.path.join('binary', 'win', 'ffprobe.exe')
    else:
        command = os.path.join('binary', 'darwin', 'ffprobe')

    command = resource_path.path(command) + parameter
    # open('./log.txt', 'a').write('ffprobe 命令 %s\n' % command)
    p = subprocess.Popen(command,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    # open('./log.txt', 'a').write('ffprobe输出out %s\n' % out)
    # open('./log.txt', 'a').write('ffprobe输出err %s\n' % err)
    streams = json.loads(out)['streams']
    return streams[0]


def rename(file: str) -> str:
    path = list(os.path.split(file))
    path[1] = '%s_' % path[1]
    return os.path.join(*path)


def process(task: VideoTask):
    # open('./log.txt', 'a').write('水印 process\n')
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
    command = '{ffmpeg} -i {input} ' \
              '-vf "drawtext=fontfile=\'{font}\': text=\'{watermark}\' ' \
              ':x={x}: y={y}: fontsize=20: fontcolor=white@0.8: box=1: boxcolor=random@0.5: boxborderw=5" ' \
              '-c:a copy -c:v {codec_name} -profile:v {profile} -level {level} ' \
              '{output} -y'.format(ffmpeg=task.ffmpeg,
                                   font=task.font,
                                   input=old_file,
                                   watermark=task.watermark, x=x, y=y,
                                   codec_name=task.codec_name, profile=task.profile, level=task.level,
                                   output=new_file)
    print('添加水印命令', command)
    # open('./log.txt', 'a').write('添加水印命令: %s \n' % command)
    process = subprocess.Popen(command,
                               shell=True,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    out, err = process.communicate()
    print('输出out %s' % out)
    print('输出err %s' % err.decode('utf-8'))
    # open('./log.txt', 'a').write('输出out: %s \n' % out)
    # open('./log.txt', 'a').write('输出err: %s \n' % err.decode('utf-8'))
    # print('加水印后', get_video_stream(file))


def undo(dir: str):
    # open('./log.txt', 'a').write('水印 undo %s \n' % dir)
    files = glob.glob(os.path.join(dir, '*.ts_'), recursive=True)
    # open('./log.txt', 'a').write('水印 undo 数量%d \n' % len(files))
    for file in files:
        os.replace(file, file[:-1])


if __name__ == '__main__':
    undo('/Volumes/HDD/玩很大')
