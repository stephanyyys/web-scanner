from scanner.utils import unverified_https_requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from scanner.base_module import ScannerModule

class LinkCrawler(ScannerModule):
    def __init__(self, max_depth=1):
        self.visited = set()
        self.max_depth = max_depth
        self.links = []

    def crawl(self, url, depth):
        if depth > self.max_depth or url in self.visited:
            return

        self.visited.add(url)

        with unverified_https_requests() as session:
            try:
                response = session.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")
                for link_tag in soup.find_all("a", href=True):
                    link = urljoin(url, link_tag["href"])
                    parsed = urlparse(link)
                    if parsed.netloc == urlparse(url).netloc:
                        self.links.append(link)
                        self.crawl(link, depth + 1)
            except Exception:
                pass

    def run(self, url):
        self.crawl(url, 0)
        return self.links