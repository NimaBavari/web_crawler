import os
from urllib.parse import urljoin, urlparse

import aiofiles


class URLHandler:
    """Custom URL Handler."""

    def __init__(self, href):
        self.href = href

    @property
    def is_inline(self):
        return self.href == '' or self.href == '/' or self.href.startswith('#')

    @property
    def domain_name(self):
        return urlparse(self.href).netloc

    def to_absolute(self, base):
        return urljoin(base, self.href)

    def to_relative(self):
        return urlparse(self.href).path


def secure_filename(name):
    return name[:-1] if name.endswith('/') else name


def make_domain_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


async def make_document(url, content, data_dir):
    handler = URLHandler(url)
    domain_name = handler.domain_name
    domain_dir = os.path.join(data_dir, domain_name)
    make_domain_dir(domain_dir)
    filename = secure_filename(handler.to_relative())
    async with aiofiles.open(os.path.join(domain_dir, filename), 'w+') as f:
        await f.write(content)


def get_all_document_names(directory):
    return [f for dp, dn, filenames in os.walk(directory) for f in filenames]
