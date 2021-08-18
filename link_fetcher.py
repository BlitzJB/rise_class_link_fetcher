import requests
from bs4 import BeautifulSoup


def return_youtube_link_from_embed_id(embed_id):
  headers = {
    'authority': 'www.youtube-nocookie.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-gpc': '1',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': 'https://server1.onlineecas.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
  }

  params = (
    ('autoplay', '0'),
    ('controls', '0'),
    ('disablekb', '1'),
    ('playsinline', '1'),
    ('cc_load_policy', '0'),
    ('cc_lang_pref', 'auto'),
    ('widget_referrer', 'https^%^3A^%^2F^%^2Fserver1.onlineecas.com^%^2Fcbt2037^%^2FeLearnVideos.aspx^%^3FRESTYPE^%^3DVIDEOS^%^23'),
    ('rel', '0'),
    ('showinfo', '0'),
    ('iv_load_policy', '3'),
    ('modestbranding', '1'),
    ('customControls', 'true'),
    ('noCookie', 'true'),
    ('enablejsapi', '1'),
    ('origin', 'https^%^3A^%^2F^%^2Fserver1.onlineecas.com'),
    ('widgetid', '1'),
  )

  response = requests.get(f'https://www.youtube-nocookie.com/embed/{embed_id}', headers=headers, params=params)

  soup = BeautifulSoup(response.text, 'html.parser')
  link_container = soup.find('div', class_ = 'submessage')
  link = link_container.a['href']
  
  return link


def return_rec_ids():
  headers = {
    'authority': 'server1.onlineecas.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'content-type': 'application/json; charset=UTF-8',
    'sec-gpc': '1',
    'origin': 'https://server1.onlineecas.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://server1.onlineecas.com/CBT2037/eLearnVideos.aspx?RESTYPE=VIDEOS',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'CData=; ClientID=203700; SoftID=1; HMD=0; _zm_lang=en-US; zm_previewVal=7; ASP.NET_SessionId=gt4e2w45vb13e3jodtbui0r5; UserLogin=B849AD93FFC3AAAB0AFFF08E8C4611BC111A2B3E9D7F960A7C5ECC942B7A2F17EF2B8502EEC7399C23EC6164ED24CA2A307F5FAD7AB368E363BBB8041BD2B5ADF44A2A7696FE1742CAE613660B6972D85E490177357A6EC5A52648239D47D5239BBAEFEC; LOGID=12391',
  }

  data = '{"RTYPE":"VIDEOS","VSUB":"3","VST":"1","VCAT":""}'

  response = requests.post('https://server1.onlineecas.com/CBT2037/WebService1.asmx/getResourcesList', headers=headers, data=data)

  raw = response.json()['d']
  raw.replace(r'\u003c', '<').replace(r'\u003e', '>')
  soup = BeautifulSoup(raw, 'html.parser')
  out = [
          (
            li.find('span').text.split(':')[1], 
            li.find('h6').text
          ) 
          for li in soup.find_all('li') 
        ]
  return out


def return_embed_id_from_rec_id(rec_id: str) -> str:
  headers = {
    'authority': 'server1.onlineecas.com',
    'cache-control': 'no-cache',
    'x-requested-with': 'XMLHttpRequest',
    'x-microsoftajax': 'Delta=true',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'accept': '*/*',
    'sec-gpc': '1',
    'origin': 'https://server1.onlineecas.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://server1.onlineecas.com/CBT2037/eLearnVideos.aspx?RESTYPE=VIDEOS',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': 'CData=; ClientID=203700; SoftID=1; HMD=0; _zm_lang=en-US; zm_previewVal=7; ASP.NET_SessionId=gt4e2w45vb13e3jodtbui0r5; UserLogin=B849AD93FFC3AAAB0AFFF08E8C4611BC111A2B3E9D7F960A7C5ECC942B7A2F17EF2B8502EEC7399C23EC6164ED24CA2A307F5FAD7AB368E363BBB8041BD2B5ADF44A2A7696FE1742CAE613660B6972D85E490177357A6EC5A52648239D47D5239BBAEFEC; LOGID=12391',
  }

  params = (
    ('RESTYPE', 'VIDEOS'),
  )

  data = {
    '__EVENTTARGET': 'lnkShowVideo',
    '__EVENTARGUMENT': rec_id.strip(),
  }

  response = requests.post('https://server1.onlineecas.com/CBT2037/eLearnVideos.aspx', headers=headers, params=params, data=data)

  return response.text.split('loadPlayer')[1].split(';')[0][1:-1].split(',')[0][1:-1]

if __name__ == '__main__':
  for id, name in return_rec_ids():
    embed_id = return_embed_id_from_rec_id(id)
    link = return_youtube_link_from_embed_id(embed_id)
    print(name, f'[{id}]', link)