import requests

def latestPost():
    url = 'http://yesayasoftware.test/api/posts'
    json_data = requests.get(url).json()

    return json_data[0]
