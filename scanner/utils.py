from contextlib import contextmanager
import requests as req
import inquirer

@contextmanager
def unverified_https_requests():
    session = req.Session()
    session.verify = False
    req.packages.urllib3.disable_warnings()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/"
    })
    try:
        yield session
    finally:
        session.close()


def select_mode():
    questions = [
        inquirer.List(
            'mode',
            message="Выберите режим работы сканера",
            choices=['crawler', 'forms', 'headers', 'portscan'],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['mode']

def select_crawler_depth():
    questions = [
        inquirer.List(
            'depth',
            message="Выберите глубину сканирования Crawler",
            choices=[1,2,3],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['depth']

def select_crawler_show_full_result():
    questions = [
        inquirer.List(
            'show_full_result',
            message="Показать полный вывод (список найденных ссылок)",
            choices=['Yes', 'No'],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['show_full_result']

def select_forms_mode():
    questions = [
        inquirer.List(
            'forms_mode',
            message="Выберите режим сканирования форм",
            choices=['Только целевом URL', 'Сканирование всех форм (Crawler)'],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['forms_mode']
    
def forms_handler(forms):
    if forms:
        for form in forms:
            print(f"\n[OK] Форма на {form['url']}")
            print(f"    Метод: {form['method']}")
            print(f"    Action: {form['action']}")
            print(f"    Поля: {form['inputs']}")
    else:
        print(f"[!] Формы не найдены")

def select_portscan_mode():
    questions = [
        inquirer.List(
            'portscan_mode',
            message="Выберите режим сканирования портов",
            choices=['stelth', 'aggressive', 'firewall_check'],
        ),
    ]
    answers = inquirer.prompt(questions)
    return answers['portscan_mode']

def get_popular_ports():
    try:
        print(f"[*] Получаем список самых популярных портов")
        with open('data/ports_test.txt', 'r') as f:
            line = f.readline().strip()
            return [int(n) for n in line.split(',')]
    except FileNotFoundError:
        print(f"[!] Не удалось получить список портов")
        return