import os
from urllib.parse import urljoin, urlparse

import aiofiles


class URLHandler:
    """Custom URL handler.

    :param: href (``str``)      -> an absolute or relative link URL
    """

    def __init__(self, href):
        self.href = href

    @property
    def is_inline(self):
        """Checks if link is inline.

        :returns: (``bool``)    -> if link points to the current page
        """
        return self.href == '' or self.href == '/' or self.href.startswith('#')

    @property
    def domain_name(self):
        """Domain name of link.

        :returns: (``str``)     -> NetLoc of link
        """
        return urlparse(self.href).netloc

    def to_absolute(self, base):
        """Converts link to an absolute url.

        :param: base (``str``)  -> base URL of link
        :returns: (``str``)     -> absolute URL of link
        """
        return urljoin(base, self.href)

    def to_relative(self):
        """Converts link to a relative URL.

        :returns: (``str``)     -> relative URL of link
        """
        return urlparse(self.href).path


def secure_filename(name):
    """Converts a relative URL path to a secure filename. A secure
    filename means one that is not confused with a directory.

    :param: name (``str``)      -> relative URL
    :returns: (``str``)         -> secure filename
    """
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
