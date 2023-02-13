import aiohttp
import asyncio
from dotenv import load_dotenv
import os
import aiofiles

# pip install aiofiles==0.7.0

load_dotenv()


async def img_downloader(session, img):
    img_name = img.split("/")[-1].split("?")[0]

    try:
        os.mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(img, ssl=False) as response:
        if response.status == 200:
            async with aiofiles.open(
                f"./images/{img_name}", mode="wb"
            ) as file:  # noqa: E501
                await file.write(await response.read())


async def fetch(session, url):
    headers = {
        "X-Naver-Client-id": os.environ.get("X-Naver-Client-id"),
        "X-Naver-Client-Secret": os.environ.get("X-Naver-Client-Secret"),
    }
    async with session.get(url, ssl=False, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]

        await asyncio.gather(*[img_downloader(session, img) for img in images])


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "지수"
    urls = [
        f"{BASE_URL}?query={keyword}&display=20&start={i * 20 + 1}"
        for i in range(10)  # noqa: E501
    ]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":
    asyncio.run(main())
    print("end")
