import threading
import time
from typing import Set

import aria2p
import m3u8
import requests

from ui_log import Frame


class CoreM3u8:
    def __init__(self, logger: Frame,
                 m3u8_src: str,
                 m3u8_proxy: str,
                 api: aria2p.API,
                 ):
        self.__is_running = False
        self.__loop_is_running = False
        self.__logger = logger
        self.__m3u8_src = m3u8_src
        self.__m3u8_proxy = m3u8_proxy
        self.__api = api

    @property
    def is_running(self) -> bool:
        return self.__is_running

    def start(self):
        self.__is_running = True
        self.__loop_is_running = True
        threading.Thread(target=self.__loop).start()

    def stop(self):
        self.__loop_is_running = False
        time.sleep(1)

    def load_m3u8(self) -> Set[str]:
        proxies = {}
        if len(self.__m3u8_proxy) > 0:
            proxies['http'] = proxies['https'] = self.__m3u8_proxy
        res = requests.get(self.__m3u8_src, timeout=5, proxies=proxies)
        if res.status_code != 200:
            raise Exception('The m3u8 src status code was not equal to 200.'
                            '\nNow is %d' % res.status_code)
        if '#EXTM3U' not in res.text:
            raise Exception('The m3u8 src is not match the hls standard')
        content = m3u8.loads(res.text, self.__m3u8_src)
        if content.is_variant:
            self.__m3u8_src = max(content.playlists, key=lambda item: item.stream_info.bandwidth).absolute_uri
            return set()
        return set([s.absolute_uri for s in content.segments])

    def __loop(self):
        urls: Set[str] = set()
        while self.__loop_is_running:
            try:
                new_urls = self.load_m3u8().difference(urls)
                if len(new_urls) > 0:
                    urls.update(new_urls)
                    new_urls = list(new_urls)
                    list.sort(new_urls)
                    print('%d个新碎片' % len(new_urls))
                    for url in new_urls:
                        self.__logger.log('新视频碎片\n%s' % url)
                        self.__api.add_uris([url])
            except Exception as e:
                print('loop错误', e)
                self.__logger.error('读取m3u8发生错误\n %s' % str(e))
            time.sleep(2)
        self.__is_running = False
