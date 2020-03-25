from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ&t=7s')

p144 = False
p240 = False
p360 = False
p480 = False
p720 = False
p1080 = False
p1440 = False
p2160 = False

all_streams = yt.streams.all()

for i in all_streams:
    if p144 is not True:  # why this condition? if 1 bar True set ho gya to vapas check krne ki jarurat na pade
        if i.resolution == '144p':
            p144 = True
    if p240 is not True:
        if i.resolution == '240p':
            p240 = True
    if p360 is not True:
        if i.resolution == '360p':
            p360 = True
    if p480 is not True:
        if i.resolution == '480p':
            p480 = True
    if p720 is not True:
        if i.resolution == '720p':
            p720 = True
    if p1080 is not True:
        if i.resolution == '1080p':
            p1080 = True
    if p1440 is not True:
        if i.resolution == '1440p':
            p1440 = True
    if p2160 is not True:
        if i.resolution == '2160p':
            p2160 = True


print(p144, p240, p360, p480, p720, p1080, p1440, p2160)