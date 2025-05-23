from scanner.utils import unverified_https_requests
from bs4 import BeautifulSoup
from scanner.base_module import ScannerModule

class FormFinder(ScannerModule):
    def __init__(self):
        self.forms = set()

    def extract_forms(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        forms = soup.find_all("form")
        for form in forms:
            action = form.get("action")
            if not action:
                continue

            method = form.get("method", "get").upper()
            if method == 'GET':
                continue
            
            inputs = [(i.get("type", "text"), i.get("name")) for i in form.find_all("input")]

            signature = (url, action, method, tuple(inputs))

            if signature not in self.forms:
                self.forms.append({
                    "url": url,
                    "action": action,
                    "method": method,
                    "inputs": inputs
                })

    def run(self, url):
        with unverified_https_requests() as session:
            try:
                response = session.get(url, timeout=5)
                self.extract_forms(response.text, url)
            except Exception:
                pass
        return self.forms