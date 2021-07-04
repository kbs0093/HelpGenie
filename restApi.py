import requests


def uploadVideo(filename):

    url = 'http://49.247.212.224:8000/upload/'
    video = open(('./' + filename), 'rb')

    upload = { 'document' : video}

    res = requests.post(url, files = upload)

    print(res)
    return res

uploadVideo('handSignal.avi')
