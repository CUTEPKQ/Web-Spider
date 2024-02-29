import json
from weibo import weibo_query ,weibo_user

#加载参数
with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

if __name__ == '__main__':
    headers = data["weibo_header"]
    cookies = data["weibo_cookies"]
    # page query user_id 可在config.json文件中修改，也可以直接赋值 （！！！ 注意 user_id page 为整数）
    page = 2
    query = data["query"]
    user_id = data["user_id"]
    Weibo_query = weibo_query(query,headers,cookies)
    df = Weibo_query.get_weibo_info(page)
    print(df)

    # Weibo_user = weibo_user(user_id,headers,cookies)
    # df = Weibo_user.get_weibo_user(page)
    #
    # df.to_csv('res.csv', encoding='utf_8_sig', index=False)











