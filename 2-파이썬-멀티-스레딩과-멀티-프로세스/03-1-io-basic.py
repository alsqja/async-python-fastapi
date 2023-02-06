import requests
import time
import os
import threading


def fetcher(session, url):
    # 73044 process | 140704434419904 url : https://apple.com
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url}")
    with session.get(url) as response:
        return response.text


def main():
    urls = [
        "https://apple.com",
        "https://google.com",
        "https://github.com",
        "http://localhost:8080",
    ] * 50

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]
        print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)  # 32.92651915550232
