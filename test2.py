import os
import subprocess
from urllib.parse import urlparse

import m3u8
import requests
from Cryptodome.Cipher import AES


def get_filename_from_url(url: str) -> str:
    return urlparse(url).path.split('/')[-1]


def decrypt(content, key, iv):
    cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    return cipher.decrypt(content)


if __name__ == "__main__":
    _dir = '/Volumes/HDD/玩很大'
    a = m3u8.load(
        'https://manifest.prod.boltdns.net/manifest/v1/hls/v4/aes128/4338955585001/4b93a12b-17e3-4e7e-9217-f4b33bf9944d/10s/master.m3u8?fastly_token=NWVjNzMwODhfMmZjZWE1YjkxYTZkYmY4MmQ3ODM4MjBiYWNiODZkMTkzNWNkYTA1ZjQ5MTZhZTU3Nzg2ZTIxMDA5MjMwNDIzYw%3D%3D')
    # print('碎片数量', len(a.segments))
    # for pl in a.playlists:
    #     print(pl)
    print(a.playlists[-1].media[0])
    # print('iv', a.keys[0].iv)
    # print('碎片数量', len(a.segments))
    # key = requests.get(a.keys[0].absolute_uri).content
    # print('key', key)
    # files = []
    # for segment in a.segments:
    #     url = segment.absolute_uri
    #     file_name = get_filename_from_url(segment.absolute_uri)
    #     content = requests.get(url).content
    #     content = decrypt(content=content, key=key, iv=segment.key.iv.replace('0x', '')[:16].encode())
    #     open(os.path.join(_dir, 'de_' + file_name), 'wb').write(content)
    #
    #     files.append('de_' + file_name)
    #
    # open(_dir + '/list.text', 'w').writelines(['file {} \n'.format(file) for file in files])
    #
    # command = 'ffmpeg -f concat -safe 0 -i %s -c copy %s/1.mp4 -y' % (os.path.join(_dir, 'list.text'), _dir,)
    # print('command', command)
    # subprocess.Popen(command, shell=True)
