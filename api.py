from fastapi import FastAPI, HTTPException,Body
from weibo import weibo_query
import json
import uvicorn
import asyncio

# 创建 FastAPI 实例
app = FastAPI()

# 加载参数
with open('config.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

@app.post('/api/weibo')
async def get_weibo_info(input: str = Body()):
    try:
        # 使用配置中的 headers 和 cookies
        headers = data["weibo_header"]
        cookies = data["weibo_cookies"]
        input = json.loads(input)
        query = input['query']
        page = input['page']
        # 创建 weibo_query 实例并获取微博信息
        weibo_instance = weibo_query(query, page, headers, cookies)
        df = weibo_instance.get_weibo_info()
        # 将 DataFrame 转换为 JSON 字符串并返回
        # # return df.to_json(orient='records', force_ascii=False)
        return df.to_dict(orient='records')
    except Exception as e:
        # 如果遇到错误，抛出 HTTP 异常
        raise HTTPException(status_code=500, detail=str(e))

async def main():
    config = uvicorn.Config("api:app", host='localhost', reload=True, port=9394, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())