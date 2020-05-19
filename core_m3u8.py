from urllib import parse

import m3u8
import requests


class CoreM3u8:
    def __init__(self, url: str, m3u8_proxy: str):
        self.__url = url
        self.__proxy = m3u8_proxy

    def load_m3u8_content(self, timeout: int = 5) -> set:
        print('load_m3u8_content', self.__url)
        res = requests.get(url=self.__url, proxies={'http': self.__proxy, 'https': self.__proxy},
                           timeout=timeout)
        if res.status_code != 200:
            raise Exception('m3u8源响应状态不等于200，当前为：{}'.format(res.status_code))
        if '#EXTM3U' not in res.text:
            raise Exception('m3u8源不是标准的HLS m3u8文档')
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
