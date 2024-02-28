import requests
from bs4 import BeautifulSoup
import pandas as pd

class weibo_query:
    def __init__(self,query,page,headers,cookies):
        '''
        :param query: 话题请求
        :param page: 请求几页,用来控制数据条数（一页十条）
        :param my_headers: 传入的headers
        :param my_cookies: 传入的cookies
        '''
        self.query = query
        self.headers = headers
        self.cookies = cookies
        self.page = page

    def weibo_response(self):
        '''
        :return: 返回请求结果
        '''
        params = {
            'q': self.query,
            'nodup': 1,
            'page':self.page
        }
        response = requests.get('https://s.weibo.com/weibo', params=params, headers=self.headers,cookies=self.cookies)
        return response

    def extract_data(self,text):
        '''
        对传入的网页信息通过BeautifulSoup进行解析和处理，提取出一个页面的信息
        :return:返回处理后的dataframe
        '''
        soup = BeautifulSoup(text, 'lxml')
        divs = soup.select('div[action-type="feed_list_item"]')
        lst = []
        for div in divs:
            time = div.select('div.card-feed > div.content > div.from > a:first-of-type')
            if time:
                time = time[0].string.strip()
            else:
                time = None
            p = div.select('div.card-feed > div.content > p:last-of-type')
            if p:
                p = p[0].strings
                content = '\n'.join([para.replace('\u200b', '').strip() for para in list(p)]).strip()
            else:
                content = None
            lst.append((content, time))
        df = pd.DataFrame(lst, columns=['content', 'time'])
        return df

    def get_weibo_info(self):
        '''
        得到最后的多个页面信息
        :return: 多个页面的信息，类型为Dataframe
        '''
        df_list = []
        for i in range(1, self.page + 1):
            response = self.weibo_response()
            if response.status_code == 200:
                df = self.extract_data(response.text)
                df_list.append(df)
                print(f'第{i}页解析成功！', flush=True)
        df = pd.concat(df_list)
        return df