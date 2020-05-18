import m3u8

if __name__ == '__main__':
    '''vidol m3u8入口链接'''
    # a = m3u8.load(
    #    'https://manifest.prod.boltdns.net/manifest/v1/hls/v4/aes128/4338955585001/88e1ccb7-26af-4d5c-b640-d5054d4f717b/10s/master.m3u8?fastly_token=NWVjMzRmNjRfOWIzNGU2MzgxMzc0MTQ2Mjg3YmVkYjdkZmYxMDRkNmEyMjA2YmU4ZGJiYTY2NTk4ZGMyYmZmZjlhYjUyNmE0NA%3D%3D')
    '''4gtv m3u8入口链接'''
    a = m3u8.load(
        'https://4gtvfreepc-cds.cdn.hinet.net/live/pool/4gtv-4gtv040/4gtv-live-mid/index.m3u8?token=YtEJGbrARJoqpK6Ue6LZ6Q&expires=1589882071&token1=bwb6ix1jMCbKDMn8FIlaQA&expires1=1589882071&_=1589835268678')
    print('a is_variant', a.is_variant)
    print('playlists', max([p.stream_info.bandwidth for p in a.playlists]))
    pl: m3u8.Playlist = max(a.playlists, key=lambda item: item.stream_info.bandwidth)
    print('最高清：', pl.absolute_uri)
