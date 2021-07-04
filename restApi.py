import requests


def uploadVideo(filename):

    url = 'http://blahblah:8000/upload/'
    video = open(('./' + filename), 'rb')

    upload = {'file': video}

    res = requests.post(url, file_name = upload)

    return res
