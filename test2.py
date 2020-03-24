from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ&t=7s')

# stream = yt.streams.get_by_resolution('360p')

ss = yt.streams.all()

for i in ss:
    if i.resolution == '480p':
        print('pp')
