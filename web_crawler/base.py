import asyncio
import os

import aiohttp
from bs4 import BeautifulSoup

from .utils import URLHandler, get_all_document_names, make_document


class WebCrawler:
    """Basic web crawler."""

    def __init__(self, start_page, root_dir):
        self.start_page = start_page
        self.data_dir = os.path.join(root_dir, 'data/')
        self.queue = []

    async def start(self):
        self.queue.append(self.start_page)
        await self.crawl(self.start_page)

    def parse_links(self, doc_url, document):
        document_soup = BeautifulSoup(document, 'lxml')
        links = document_soup.select('a')
        urls = [link['href'] for link in links]
        for url in urls:
            handler = URLHandler(url)
            if handler.is_inline:
                continue
            abs_url = handler.to_absolute(doc_url)
            if abs_url not in get_all_document_names(self.data_dir):
                self.queue.append(abs_url)

    async def crawl(self, url):
        self.queue.remove(url)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            doc_content = await response.text()
        await make_document(url, doc_content, self.data_dir)
        self.parse_links(url, doc_content)
        await asyncio.gather(
            *[self.crawl(url) for url in self.queue]
        )
