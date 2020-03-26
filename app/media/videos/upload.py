import requests
import os
import json


videos = os.listdir()

URL = 'http://localhost/'

client = requests.session()

client.get(URL)  # sets cookie
if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']
else:
    csrftoken = client.cookies['csrf']

for video in videos:
    if video.endswith("py"):
        continue

    with open(video, "rb") as v:

        res = requests.post("http://localhost/api/video/upload",
                            files={"video": v},
                            data={
                                "csrfmiddlewaretoken": csrftoken,
                            },
                            headers={
                                "Authorization": "Token cc0e15d69090db0d3e7bc1afbd43d3e67a21fb4e"
                            }
                            ).text
        print(res)

    break
