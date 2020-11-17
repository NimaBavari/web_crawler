import asyncio

from web_crawler import WebCrawler

if __name__ == '__main__':
    cr = WebCrawler('https://isitchristmas.com/', '.')
    asyncio.run(cr.start())
