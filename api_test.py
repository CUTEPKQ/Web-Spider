import pandas as pd
import requests
import json

with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# FastAPI 服务器的 URL
url = "http://localhost:9394/api/weibo"
input = {
    "query": data["query"],
    "page": data["page"]
}

json_data = json.dumps(input,ensure_ascii=False)
response = requests.post(url, json=json_data)

# 打印响应内容
info = response.json()
print(info)
# df = pd.DataFrame(info)
# df.to_csv(f'{input["query"]}.csv', encoding='utf_8_sig', index=False)