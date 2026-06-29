#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
OSINT Scanner Pro v2.0
Разведка по открытым источникам
Автор: r62983218-dev
GitHub: https://github.com/r62983218-dev/Osint
"""

import os
import sys
import subprocess
import time
import requests
import json
from datetime import datetime

# ============================================
# ⚙️  НАСТРОЙКИ
# ============================================

GITHUB_NICKNAME = "r62983218-dev"
HUNTER_API_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# ============================================
# ИМПОРТ COLORAMA (с автоустановкой)
# ============================================

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("📦 Установка colorama...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama"], check=True)
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# ============================================
# ПРОВЕРКА ЗАВИСИМОСТЕЙ
# ============================================

def check_and_install_packages():
    """Автоматическая установка всех зависимостей"""
    
    print(Fore.CYAN + "╔════════════════════════════════════════╗")
    print(Fore.CYAN + "║    📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ          ║")
    print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
    
    required_packages = {
        "python": "python",
        "python-pip": "pip",
        "git": "git"
    }
    
    for package, name in required_packages.items():
        print(f"🔍 Проверка: {name}...", end=" ")
        try:
            result = subprocess.run(["pkg", "list-installed", package], 
                                   capture_output=True, text=True)
            if package in result.stdout:
                print(Fore.GREEN + "✅ Установлен")
            else:
                raise Exception("Not installed")
        except:
            print(Fore.YELLOW + "❌ Не найден")
            print(f"📥 Установка {name}...")
            subprocess.run(["pkg", "install", package, "-y"], check=True)
            print(Fore.GREEN + f"✅ {name} установлен!\n")
    
    python_libs = ["requests", "python-whois"]
    
    print("\n" + Fore.CYAN + "📚 ПРОВЕРКА PYTHON-БИБЛИОТЕК:")
    for lib in python_libs:
        print(f"🔍 Проверка: {lib}...", end=" ")
        try:
            __import__(lib.replace("-", "_"))
            print(Fore.GREEN + "✅ Установлена")
        except ImportError:
            print(Fore.YELLOW + "❌ Не найдена")
            print(f"📥 Установка {lib}...")
            subprocess.run([sys.executable, "-m", "pip", "install", lib], check=True)
            print(Fore.GREEN + f"✅ {lib} установлена!\n")
    
    print(Fore.GREEN + "\n✅ ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ!\n")
    time.sleep(1)

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def get_panda():
    panda = Fore.WHITE + """
        ╔══════════════════════════════════╗
        ║    🐼  ПАНДА-ХАКЕР ПРИВЕТСТВУЕТ  ║
        ╚══════════════════════════════════╝
        ████████████████████████████████████
        ██╔══════════════════════════════██║
        ██║   ▄▄▄▄▄   ▄▄▄▄▄   ▄▄▄▄▄   ║██║
        ██║  █▄▄▄▄█  █▄▄▄▄█  █▄▄▄▄█  ║██║
        ██║  █▄▄▄▄█  █▄▄▄▄█  █▄▄▄▄█  ║██║
        ██║   ▀▀▀▀▀   ▀▀▀▀▀   ▀▀▀▀▀   ║██║
        ██╚══════════════════════════════██║
        ████████████████████████████████████
    """
    return panda

def print_banner():
    clear_screen()
    print(Fore.CYAN + get_panda())
    print(Fore.CYAN + "╔═══════════════════════════════════════════╗")
    print(Fore.CYAN + "║     🕵️  OSINT SCANNER PRO v2.0          ║")
    print(Fore.CYAN + "║     Разведка по открытым источникам      ║")
    print(Fore.CYAN + f"║     Автор: @{GITHUB_NICKNAME}" + " " * (37 - len(GITHUB_NICKNAME)) + "║")
    print(Fore.CYAN + "╚═══════════════════════════════════════════╝")
    print(Fore.YELLOW + f"📱 Termux Edition | Разработано {GITHUB_NICKNAME}\n")

def progress_bar(current, total, message):
    percent = (current / total) * 100
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    sys.stdout.write(f"\r{Fore.GREEN}┃{bar}┃ {int(percent)}% {message}")
    sys.stdout.flush()

def print_menu():
    print(Fore.YELLOW + "╔════════════════════════════════════════╗")
    print(Fore.YELLOW + "║          📋  ГЛАВНОЕ МЕНЮ            ║")
    print(Fore.YELLOW + "╚════════════════════════════════════════╝")
    print()
    print(Fore.CYAN + "  [1]" + Fore.WHITE + " 🔍  Начать сканирование")
    print(Fore.CYAN + "  [2]" + Fore.WHITE + " 📂  Просмотреть отчёты")
    print(Fore.CYAN + "  [3]" + Fore.WHITE + " 🗑️   Очистить отчёты")
    print(Fore.CYAN + "  [4]" + Fore.WHITE + " ℹ️   Информация")
    print(Fore.CYAN + "  [5]" + Fore.WHITE + " 🚪  Выход")
    print()
    print(Fore.YELLOW + "╚════════════════════════════════════════╝")

def osint_scan(target, progress_callback=None):
    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "social": {},
        "breaches": [],
        "whois": None,
        "telegram": None,
        "vk": None,
        "status": "completed"
    }
    
    steps = [
        ("📧 Проверка email на утечки...", "breaches"),
        ("📱 Поиск в Telegram...", "telegram"),
        ("📘 Поиск в VK...", "vk"),
        ("🌐 Поиск в соцсетях...", "social"),
        ("🏷️ WHOIS для доменов...", "whois"),
    ]
    
    total_steps = len(steps)
    current_step = 0
    
    if "@" in target:
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{target}"
            response = requests.get(url, timeout=10, headers={"User-Agent": "OSINT-Scanner"})
            if response.status_code == 200:
                results["breaches"] = [b["Name"] for b in response.json()]
            elif response.status_code == 404:
                results["breaches"] = ["✅ Утечек не найдено"]
            else:
                results["breaches"] = [f"⚠️ Статус: {response.status_code}"]
        except requests.exceptions.Timeout:
            results["breaches"] = ["❌ Таймаут подключения"]
        except requests.exceptions.ConnectionError:
            results["breaches"] = ["❌ Ошибка соединения"]
        except Exception as e:
            results["breaches"] = [f"❌ Ошибка: {str(e)[:50]}"]
    
    current_step += 1
    if progress_callback:
        progress_callback(current_step, total_steps, steps[0][0])
    
    if "@" in target:
        try:
            possible_username = target.split("@")[0].replace(".", "").lower()
            tg_url = f"https://t.me/{possible_username}"
            response = requests.get(tg_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200 and "tgme_page_extra" in response.text:
                results["telegram"] = {
                    "username": possible_username,
                    "url": tg_url,
                    "exists": True
                }
            else:
                results["telegram"] = {"exists": False, "message": "❌ Не найден"}
        except:
            results["telegram"] = {"exists": False, "error": "❌ Ошибка проверки"}
    
    current_step += 1
    if progress_callback:
        progress_callback(current_step, total_steps, steps[1][0])
    
    try:
        search_query = target.split("@")[0] if "@" in target else target
        vk_urls = [
            f"https://vk.com/{search_query}",
            f"https://vk.com/id{search_query}" if search_query.isdigit() else None
        ]
        found = False
        for vk_url in vk_urls:
            if vk_url:
                try:
                    r = requests.get(vk_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                    if r.status_code == 200 and "page_name" in r.text.lower():
                        results["vk"] = {
                            "url": vk_url,
                            "exists": True,
                            "profile": "Найден в VK"
                        }
                        found = True
                        break
                except:
                    pass
        if not found:
            results["vk"] = {"exists": False, "message": "❌ Не найден"}
    except:
        results["vk"] = {"exists": False, "error": "❌ Ошибка проверки"}
    
    current_step += 1
    if progress_callback:
        progress_callback(current_step, total_steps, steps[2][0])
    
    if not "@" in target and "." not in target:
        socials = {
            "GitHub": f"https://github.com/{target}",
            "Twitter": f"https://twitter.com/{target}",
            "Reddit": f"https://reddit.com/user/{target}",
            "Instagram": f"https://instagram.com/{target}",
            "YouTube": f"https://youtube.com/@{target}",
            "TikTok": f"https://tiktok.com/@{target}"
        }
        for name, url in socials.items():
            try:
                r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                if r.status_code == 200:
                    results["social"][name] = url
            except:
                pass
    
    current_step += 1
    if progress_callback:
        progress_callback(current_step, total_steps, steps[3][0])
    
    if "." in target and not "@" in target:
        try:
            import whois
            domain_info = whois.whois(target)
            results["whois"] = {
                "registrar": domain_info.registrar or "Неизвестно",
                "creation": str(domain_info.creation_date) if domain_info.creation_date else "Неизвестно",
                "expiration": str(domain_info.expiration_date) if domain_info.expiration_date else "Неизвестно"
            }
        except Exception as e:
            results["whois"] = {"error": f"❌ Ошибка: {str(e)[:50]}"}
    
    current_step += 1
    if progress_callback:
        progress_callback(current_step, total_steps, steps[4][0])
    
    return results

def print_results(data):
    print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
    print(Fore.CYAN + "║        📊 РЕЗУЛЬТАТЫ OSINT          ║")
    print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
    
    print(Fore.YELLOW + f"🎯 Цель: {Fore.WHITE}{data['target']}")
    print(Fore.YELLOW + f"🕐 Время: {Fore.WHITE}{data['timestamp'][:19]}\n")
    
    if data['breaches']:
        print(Fore.RED + "💀 УТЕЧКИ:")
        for breach in data['breaches']:
            if breach.startswith("✅"):
                print(f"   {Fore.GREEN}{breach}")
            elif breach.startswith("❌") or breach.startswith("⚠️"):
                print(f"   {Fore.RED}{breach}")
            else:
                print(f"   {Fore.RED}• {breach}")
        print()
    
    if data.get('telegram'):
        if data['telegram'].get('exists'):
            print(Fore.BLUE + f"📱 TELEGRAM: {Fore.WHITE}{data['telegram']['url']}")
        else:
            print(Fore.RED + f"📱 TELEGRAM: {data['telegram'].get('message', '❌ Не найден')}")
        print()
    
    if data.get('vk'):
        if data['vk'].get('exists'):
            print(Fore.BLUE + f"📘 VK: {Fore.WHITE}{data['vk']['url']}")
        else:
            print(Fore.RED + f"📘 VK: {data['vk'].get('message', '❌ Не найден')}")
        print()
    
    if data['social']:
        print(Fore.MAGENTA + "🌐 СОЦИАЛЬНЫЕ СЕТИ:")
        for name, url in data['social'].items():
            print(f"   {Fore.CYAN}{name}: {Fore.WHITE}{url}")
        print()
    
    if data.get('whois'):
        print(Fore.GREEN + "🏷️ WHOIS-ДАННЫЕ:")
        for key, value in data['whois'].items():
            if value and not key == "error":
                print(f"   {Fore.CYAN}{key.capitalize()}: {Fore.WHITE}{value}")
        if data['whois'].get('error'):
            print(f"   {Fore.RED}{data['whois']['error']}")
        print()
    
    safe_target = data['target'].replace('@', '_').replace('.', '_').replace('/', '_')
    filename = f"osint_report_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(Fore.GREEN + f"✅ Отчёт сохранён: {Fore.WHITE}{filename}\n")
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка сохранения: {e}\n")

def show_info():
    print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
    print(Fore.CYAN + "║           ℹ️  ИНФОРМАЦИЯ              ║")
    print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
    print(Fore.WHITE + "🔹 Название: OSINT Scanner Pro v2.0")
    print(Fore.WHITE + f"🔹 Автор: @{GITHUB_NICKNAME}")
    print(Fore.WHITE + "🔹 Описание: Инструмент для поиска информации")
    print(Fore.WHITE + "           по открытым источникам")
    print()
    print(Fore.CYAN + "📌 Функции:")
    print(Fore.WHITE + "  • Проверка утечек (HaveIBeenPwned)")
    print(Fore.WHITE + "  • Поиск в Telegram")
    print(Fore.WHITE + "  • Поиск в VK")
    print(Fore.WHITE + "  • Поиск в соцсетях (GitHub, Twitter, Instagram...)")
    print(Fore.WHITE + "  • WHOIS для доменов")
    print(Fore.WHITE + "  • Сохранение отчётов в JSON")
    print()
    print(Fore.GREEN + "🔗 GitHub: https://github.com/" + GITHUB_NICKNAME + "/Osint\n")

def main():
    print_banner()
    
    try:
        requests.get("https://google.com", timeout=5)
        print(Fore.GREEN + "✅ Интернет доступен\n")
    except:
        print(Fore.RED + "⚠️ Нет подключения к интернету!\n")
        print(Fore.YELLOW + "Некоторые функции могут не работать\n")
    
    check_and_install_packages()
    
    while True:
        print_banner()
        print_menu()
        
        choice = input(f"\n{Fore.GREEN}└─ Выберите опцию (1-5): {Fore.WHITE}").strip()
        
        if choice == "1":
            print_banner()
            print(Fore.CYAN + "╔════════════════════════════════════════╗")
            print(Fore.CYAN + "║         🔍  НОВОЕ СКАНИРОВАНИЕ        ║")
            print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
            
            target = input(f"{Fore.YELLOW}📝 Введите email, username или домен: {Fore.WHITE}").strip()
            
            if not target:
                print(Fore.RED + "\n❌ Ошибка: цель не может быть пустой!")
                time.sleep(2)
                continue
            
            print(f"\n{Fore.CYAN}🔍 Начинаем сканирование: {Fore.WHITE}{target}\n")
            print(Fore.YELLOW + "⏳ Это может занять некоторое время...\n")
            
            try:
                results = osint_scan(target, progress_callback=progress_bar)
                print("\n\n")
                print_results(results)
            except Exception as e:
                print(Fore.RED + f"\n❌ Ошибка при сканировании: {str(e)}")
            
            input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...")
        
        elif choice == "2":
            print_banner()
            print(Fore.CYAN + "╔════════════════════════════════════════╗")
            print(Fore.CYAN + "║         📂  ПРОСМОТР ОТЧЁТОВ          ║")
            print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
            
            try:
                reports = [f for f in os.listdir(".") if f.startswith("osint_report_") and f.endswith(".json")]
            except:
                reports = []
            
            if not reports:
                print(Fore.YELLOW + "⚠️ Отчётов не найдено")
                input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...")
                continue
            
            reports.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            print(Fore.CYAN + "📋 Доступные отчёты:\n")
            for i, report in enumerate(reports[:10], 1):
                try:
                    size = os.path.getsize(report)
                    if size < 1024:
                        size_str = f"{size} байт"
                    elif size < 1048576:
                        size_str = f"{size/1024:.1f} КБ"
                    else:
                        size_str = f"{size/1048576:.1f} МБ"
                    print(f"  {Fore.GREEN}{i}.{Fore.WHITE} {report} {Fore.YELLOW}({size_str})")
                except:
                    print(f"  {Fore.GREEN}{i}.{Fore.WHITE} {report}")
            
            choice2 = input(f"\n{Fore.GREEN}Выберите номер отчёта (или Enter для отмены): {Fore.WHITE}")
            if choice2.isdigit() and 1 <= int(choice2) <= len(reports[:10]):
                filename = reports[int(choice2)-1]
                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        print(Fore.CYAN + "\n" + "═" * 50)
                        print(json.dumps(data, indent=2, ensure_ascii=False))
                        print(Fore.CYAN + "═" * 50 + "\n")
                except Exception as e:
                    print(Fore.RED + f"❌ Ошибка чтения файла: {e}")
            
            input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...")
        
        elif choice == "3":
            print_banner()
            print(Fore.CYAN + "╔════════════════════════════════════════╗")
            print(Fore.CYAN + "║         🗑️  ОЧИСТКА ОТЧЁТОВ           ║")
            print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
            
            try:
                reports = [f for f in os.listdir(".") if f.startswith("osint_report_") and f.endswith(".json")]
            except:
                reports = []
            
            if not reports:
                print(Fore.YELLOW + "⚠️ Отчётов не найдено")
                time.sleep(1)
                continue
            
            print(Fore.RED + "⚠️ ВНИМАНИЕ: Это действие необратимо!")
            print(Fore.YELLOW + f"Найдено {len(reports)} отчётов")
            confirm = input(f"\n{Fore.RED}Удалить все отчёты? (y/n): {Fore.WHITE}")
            
            if confirm.lower() == "y":
                count = 0
                for f in reports:
                    try:
                        os.remove(f)
                        count += 1
                    except:
                        pass
                print(Fore.GREEN + f"\n✅ Удалено {count} файлов")
            else:
                print(Fore.GREEN + "\n✅ Операция отменена")
            
            time.sleep(1)
        
        elif choice == "4":
            print_banner()
            show_info()
            input(f"\n{Fore.YELLOW}Нажмите Enter для продолжения...")
        
        elif choice == "5":
            print_banner()
            print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
            print(Fore.CYAN + "║    👋  ДО СВИДАНИЯ!                   ║")
            print(Fore.CYAN + "║    🐼  ПАНДА ГОВОРИТ: ДО ВСТРЕЧИ!     ║")
            print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
            print(Fore.GREEN + "Спасибо за использование OSINT Scanner Pro!\n")
            sys.exit(0)
        
        else:
            print(Fore.RED + "\n❌ Неверный ввод! Выберите 1-5")
            time.sleep(1)

# ============================================
# ЗАПУСК
# ============================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n⚠️ Программа прервана пользователем")
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Критическая ошибка: {str(e)}")
        print(Fore.YELLOW + "Пожалуйста, сообщите об ошибке автору")
        sys.exit(1)
