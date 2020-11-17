import asyncio
import os

import aiohttp
from bs4 import BeautifulSoup

from .utils import URLHandler, get_all_document_names, make_document


class WebCrawler:
    """Web crawler and indexer.

    :param: start_page (``str``)    -> starting URL of crawler, absolute
    :param: root_dir (``str``)      -> root directory
    """

    def __init__(self, start_page, root_dir):
        self.start_page = start_page
        self.data_dir = os.path.join(root_dir, 'data/')
        self.queue = []

    async def start(self):
        """Starts the crawler."""
        self.queue.append(self.start_page)
        await self.crawl(self.start_page)

    def parse_links(self, doc_url, document):
        """Parses links in a document and adds them to the queue if not
        already exist.

        :param: doc_url (``str``)   -> URL of the current document
        :param: document (``str``)  -> content of the current document
        """
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
        """Crawls recursively one by one off `self.queue`, indexing
        the already crawled document in a directory hierarchy.

        :param: url (``str``)       -> URL currently being crawled
        """
        self.queue.remove(url)
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            doc_content = await response.text()
        await make_document(url, doc_content, self.data_dir)
        self.parse_links(url, doc_content)
        await asyncio.gather(
            *[self.crawl(url) for url in self.queue]
        )
