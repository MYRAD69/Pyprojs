import requests
import csv
import concurrent.futures
proxylist = []
with open('proxylist.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        proxylist.append(row[0])
def extract(proxy):
  r = requests.post('https://2021.brmakercamp.cyscc.org.cn/api/review_ticket', proxies={'http': f"http://{proxy}", 'https': f"http://{proxy}"}, data={"video_id": 63, "lang": "en"})
  print(r.json())
  return proxy
with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(extract, proxylist)
