import json
from weibo import weibo_query

#加载参数
with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

if __name__ == '__main__':
    headers = data["weibo_header"]
    cookies = data["weibo_cookies"]
    page = data["page"]
    query = data["query"]
    Weibo_query = weibo_query(query,page,headers,cookies)
    df = Weibo_query.get_weibo_info()
    df.to_csv(f'{query}.csv', encoding='utf_8_sig', index=False)











