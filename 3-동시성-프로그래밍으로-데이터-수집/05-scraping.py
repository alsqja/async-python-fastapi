# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# pip install beautifulsoup4

"""
  웹 크롤링 : 검색 엔진의 구축 등을 위하여 특정한 벙법으로 웹 페이지를 수집하는 프로그램
  웹 스크래핑 : 웹에서 데이터를 수집하는 프로그램
"""

import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()


async def fetch(session, url):
    headers = {
        "X-Naver-Client-id": os.environ.get("X-Naver-Client-id"),
        "X-Naver-Client-Secret": os.environ.get("X-Naver-Client-Secret"),
    }
    async with session.get(url, ssl=False, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "지수"
    urls = [
        f"{BASE_URL}?query={keyword}&display=20&start={i}"
        for i in range(1, 10)  # noqa: E501
    ]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    asyncio.run(main())
