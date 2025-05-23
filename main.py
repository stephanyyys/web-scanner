import argparse
from scanner.crawler import LinkCrawler
from scanner.formfinder import FormFinder
from scanner.headers import HeadersChecker
from scanner.portscanner import PortScanner
from scanner.utils import *
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser(description="Web Security Scanner")
    parser.add_argument("--url", required=True, help="Целевой URL (например, https://example.com)")
    mode = select_mode()

    args = parser.parse_args()

    match mode:
        case "crawler":
            depth = select_crawler_depth()
            show_full_result = select_crawler_show_full_result()
            print(f"[*] Запуск краулера для: {args.url}")
            crawler = LinkCrawler(max_depth=depth)
            links = crawler.run(args.url)
            print(f"\n[OK] Найдено {len(links)} ссылок:")

            if show_full_result == 'Yes':
                for link in links:
                    print(f" - {link}")

        case "forms":
            forms_mode = select_forms_mode()

            if forms_mode == 'Только целевом URL':
                print(f"[*] Поиск форм на: {args.url}")
                formfinder = FormFinder()
                forms = formfinder.run(args.url)
                forms_handler(forms)
            else:
                depth = select_crawler_depth()
                print(f"[*] Запуск поиска всех форм (с использованием Crawler): {args.url}")
                crawler = LinkCrawler(max_depth=depth)
                formfinder = FormFinder()
                links = crawler.run(args.url)
                for link in tqdm(links):
                    forms = formfinder.run(link)
                    forms_handler(forms)
            
        case "headers":
            print(f"[*] Получение заголовков с: {args.url}")
            checker = HeadersChecker()
            headers = checker.run(args.url)

            if not headers:
                print("[!] Не удалось получить заголовки.")
            else:
                print("\n[OK] Полученные заголовки ответа:\n")

                for key, value in headers.items():
                    print(f"- {key}: {value}")

                print("\n[INFO] Рекомендуемые заголовки безопасности (для справки):\n")
                for h in checker.recommended_headers():
                    print(f"- {h}")
        
        case "portscan":
            portscan_mode = select_portscan_mode()
            print(f"[*] Сканирование открытых портов в: {args.url}")
            portscanner = PortScanner(portscan_mode)
            portscanner.scan_ports(args.url)


        case _:
            print(f"[!] Неизвестный режим: {args.mode}")


if __name__ == "__main__":
    main()