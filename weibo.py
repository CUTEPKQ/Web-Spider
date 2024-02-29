import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

current_date = datetime.now().strftime("%Y-%m-%d")
current_year = datetime.now().year
current_time = datetime.now()
def time_change(time):
    original_time_string = time
    try:
        # 尝试使用 '%Y-%m-%d %H:%M' 格式解析日期
        original_datetime = datetime.strptime(original_time_string.strip(), '%Y-%m-%d %H:%M')
    except ValueError:
        try:
            # 尝试使用 '%m月%d日 %H:%M' 格式解析日期
            original_datetime = datetime.strptime(original_time_string.strip(), '%m月%d日 %H:%M')
            # 如果日期中没有年份，添加当前年份
            original_datetime = original_datetime.replace(year=current_year)
        except ValueError:
            try:
                # 获取相对时间中的数字部分
                time_difference = int(original_time_string.split('分钟前')[0])
                # 计算相对时间
                original_datetime = current_time - timedelta(minutes=time_difference)
            except ValueError:
                try:
                    original_datetime = datetime.strptime(original_time_string.strip(), '%Y年%m月%d日 %H:%M')
                except ValueError:
                    return time
    formatted_time_string = original_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time_string
class weibo_query:
    def __init__(self,query,headers,cookies):
        '''
        :param query: 话题请求
        :param page: 请求几页,用来控制数据条数（一页十条）
        :param my_headers: 传入的headers
        :param my_cookies: 传入的cookies
        '''
        self.query = query
        self.headers = headers
        self.cookies = cookies


    def weibo_response(self,page):
        '''
        :return: 返回请求结果
        '''
        params = {
            'q': self.query,
            'nodup': 1,
            'page':page
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
                time = time.replace("今天",current_date)
                time = time_change(time)
            else:
                time = None
            p = div.select('div.card-feed > div.content > p:last-of-type')
            if p:
                p = p[0].strings
                content = '\n'.join([para.replace('\u200b', '').strip() for para in list(p)]).strip()
            else:
                content = None
            user = div.select('div.info > div > a.name')
            if user:
                user = user[0].get_text(strip=True)
            else:
                user = None
            url = div.select('div.card-feed > div.content > div.from > a')
            if url:
                url = url[0]['href']
                url = 'https:' + url.split('?', 1)[0]
            else:
                url = None
            lst.append((content, time, user, url))
        df = pd.DataFrame(lst, columns=['content', 'time', 'user','url'])
        return df

    def get_weibo_info(self,page):
        '''
        得到最后的多个页面信息
        :return: 多个页面的信息，类型为Dataframe
        '''
        df_list = []
        for i in range(1, page + 1):
            response = self.weibo_response(i)
            if response.status_code == 200:
                df = self.extract_data(response.text)
                df_list.append(df)
                print(f'第{i}页解析成功！', flush=True)
        df = pd.concat(df_list)
        df = df.reset_index(drop=True)
        return df

class weibo_user:
    def __init__(self,user_id,headers,cookies):
        self.userid = user_id
        self.headers = headers
        self.cookies = cookies

    def weibo_response(self,page):
        '''
        :return: 返回请求结果
        '''
        params = {
            'nodup': 1,
            'page': page
        }
        userid = str(self.userid)
        response = requests.get(f'https://weibo.cn/{userid}',
                                headers=self.headers,
                                cookies=self.cookies,
                                params=params)
        return response

    def extract_data(self,text):
        soup = BeautifulSoup(text, 'lxml')
        divs = soup.select('div[class="c"]')
        list = []
        for div in divs:
            # 获取评论内容
            span_element = div.select('div.c div span.ctt')
            if span_element:
                extracted_text = span_element[0].get_text(strip=True)
            else:
                extracted_text = None
            # 获取评论时间
            time_element = div.select('div.c div span.ct')
            if time_element:
                time = time_element[0].get_text(strip=True).split("来自", 1)[0]
                time = time.replace("今天", current_date)
                time = time_change(time)
            else:
                time = None
            list.append((extracted_text, time))
        df = pd.DataFrame(list, columns=['content', 'time'])
        return df.iloc[:-1]

    def get_weibo_user(self,page):
        df_list = []
        for i in range(1,page+1):
            response = self.weibo_response(i)
            if response.status_code == 200:
                df = self.extract_data(response.text)
                df_list.append(df)
                print(f'第{i}页解析成功！', flush=True)
        df = pd.concat(df_list)
        df = df.reset_index(drop=True)
        return df
