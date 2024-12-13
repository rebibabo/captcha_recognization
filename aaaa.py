import requests
import json
from bs4 import BeautifulSoup

proxies = {
    "http": "http://101.6.68.101:7893",
}
def translate1(sentence, reverse=False):
    # 默认繁体转简体
    if reverse:
        source = "s"
        target = "t"
    else:
        source = "t"
        target = "s"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.lddgo.net",
        "priority": "u=1, i",
        "referer": "https://www.lddgo.net/",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    url = "https://openapi.lddgo.net/base/gtool/api/v1/Transfer"
    data = {
        "data": sentence,
        "from": source,
        "to": target
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(url, data=data, headers=headers, proxies=proxies)
    print(response.text)

    return response.json()["data"]

def translate2(sentence, reverse=False):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.converts.cn",
        "Referer": "https://www.converts.cn/Simplified.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "Get_Token": "8241a7c7-00ae-4101-abf7-8aae8b62ee0a",
        "__vtins__3Fb2glfpkh9D6XsP": "%7B%22sid%22%3A%20%2232b5d9f9-7c5c-546b-b9c1-ad980893b18a%22%2C%20%22vd%22%3A%201%2C%20%22stt%22%3A%200%2C%20%22dr%22%3A%200%2C%20%22expires%22%3A%201734054318861%2C%20%22ct%22%3A%201734052518861%7D",
        "__51uvsct__3Fb2glfpkh9D6XsP": "1",
        "__51vcke__3Fb2glfpkh9D6XsP": "2db7f9e8-9e7a-5f5c-aa23-e2774bf05ca8",
        "__51vuft__3Fb2glfpkh9D6XsP": "1734052518865"
    }
    url = "https://www.converts.cn/ToConvert"
    data = {
        "Text": sentence,
        "TargetConvertsEnum": str(int(reverse))
    }
    response = requests.post(url, headers=headers, cookies=cookies, data=data)

    return response.json()["data"]

translate_mode = 0
def lookup(character):
    # global translate_mode
    # if translate_mode == 0:
    #     translated_character = translate1(character, reverse=True)
    # if not translated_character:
    #     translated_character = translate2(character, reverse=True)
    #     translate_mode = 1
    
    translated_character = translate2(character, reverse=True)
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Referer": "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/left.php",
        "Sec-Fetch-Dest": "frame",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    url = "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/search.php"
    params = {
        "q": translated_character.encode("Big5") # 编码为大五码
    }
    response = requests.get(url, headers=headers, params=params).text

    soup = BeautifulSoup(response, "html.parser")
    table = soup.select('form table')[0]

    for tr in table.select('tr')[1:]:
        word = tr.select('td div')[-1].get_text()
        if word:
            consonant = tr.select('td font[color="red"]')[0].get_text()
            vowel = tr.select('td font[color="green"]')[0].get_text()
            intonation = tr.select('td font[color="blue"]')[0].get_text()
            print(f"word: {word}")
            print(f"consonant: {consonant}")
            print(f"vowel: {vowel}")
            print(f"intonation: {intonation}")
            
print(lookup("当"))