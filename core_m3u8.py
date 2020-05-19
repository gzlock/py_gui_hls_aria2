import threading
import time
from typing import Callable, List
from urllib import parse

import aria2p
import m3u8
import requests

from ui_log import Frame

aria2_client_p: aria2p.API

is_stop: bool = False


class NotM3u8Exception(Exception):
    pass


class CoreM3u8:
    def __init__(self, url: str, log: Frame, m3u8_proxy: str, callback: Callable[[List], None]):
        self.__url = url
        self.__m3u8_proxy = m3u8_proxy
        self.__log = log
        self.__is_running: bool = False
        self.__callback = callback
        self.urls: List[str] = []

    def start(self):
        self.__is_running = True
        threading.Thread(target=self.__loop).start()

    def stop(self):
        self.__is_running = False

    def __loop(self):
        downloaded_url: set = set()
        while self.__is_running:
            try:
                new = self.load_m3u8_content()
                unique = list(new - downloaded_url)
                downloaded_url |= new
                # print('新url', unique)
                if len(unique) > 0:
                    self.__callback(unique)
            except Exception as e:
                self.__log.error('m3u8错误\n{}'.format(e))
            finally:
                time.sleep(2)

    def load_m3u8_content(self) -> set:
        print('load_m3u8_content', self.__url)
        res = requests.get(url=self.__url, proxies={'http': self.__m3u8_proxy, 'https': self.__m3u8_proxy},
                           timeout=5)
        if res.status_code != 200:
            raise Exception('m3u8 response status code {}'.format(res.status_code))
        if '#EXTM3U' not in res.text:
            raise NotM3u8Exception('不是标准的HLS m3u8文档')
        content = m3u8.loads(res.text, uri=self.__url)
        '''可变分辨率，取最大分辨率的m3u8链接'''
        if content.is_variant:
            self.__url = max(content.playlists, key=lambda item: item.stream_info.bandwidth).absolute_uri
            return set()
        urls: set = set()
        for segment in content.segments:
            uri = segment.uri
            if segment.uri.find('http') != 0:
                uri = parse.urljoin(self.__url, uri)
            urls.add(uri)
        return urls
