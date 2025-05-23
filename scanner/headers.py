from scanner.utils import unverified_https_requests
from scanner.base_module import ScannerModule

RECOMMENDED_SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
]


class HeadersChecker(ScannerModule):
    def __init__(self):
        self.headers = {}

    def run(self, url):
        with unverified_https_requests() as session:
            try:
                response = session.get(url, timeout=10)
                self.headers = dict(response.headers)
            except Exception as e:
                print(f"[!] Ошибка при запросе: {e}")
                self.headers = {}
        return self.headers

    @staticmethod
    def recommended_headers():
        return RECOMMENDED_SECURITY_HEADERS