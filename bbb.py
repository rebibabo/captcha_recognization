import requests


headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "origin": "https://www.lddgo.net",
    "priority": "u=1, i",
    "referer": "https://www.lddgo.net/",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
}
url = "https://openapi.lddgo.net/base/gauth/api/v1/RequestCaptcha"
response = requests.get(url, headers=headers)

captcha = response.json()["data"]["captchaContent"]
# 将上述的content转为图片并显示
from PIL import Image
import io
import base64

img_data = base64.b64decode(captcha)
img = Image.open(io.BytesIO(img_data))
print(img.size)