import asyncio
import time
import os
import threading
import aiohttp


async def fetcher(session, url):
    # 73827 process | 140704434419904 url : https://apple.com
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def main():
    urls = [
        "https://apple.com",
        "https://google.com",
        "https://github.com",
        "http://localhost:8080",
    ] * 50

    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)  # 9.721978902816772
