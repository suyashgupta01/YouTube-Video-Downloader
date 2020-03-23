from pytube import YouTube, exceptions

try:
    yt = YouTube('youtube.com/aldsfjasdkf')
    # create YouTube object; 2nd arg? --> passed the reference of the function...
except exceptions.RegexMatchError:
    print('No video exits at given link!')