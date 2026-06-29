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
import re
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

def detect_input_type(target):
    """Определяет тип введённых данных"""
    # Проверка на номер телефона
    phone_patterns = [
        r'^\+7\d{10}$',
        r'^8\d{10}$',
        r'^7\d{10}$',
        r'^\d{11}$',
    ]
    for pattern in phone_patterns:
        if re.match(pattern, target):
            return "phone"
    
    if "@" in target:
        return "email"
    elif target.isdigit():
        return "id"
    elif "." in target and not "@" in target:
        return "domain"
    else:
        return "username"

def get_phone_info(phone):
    """Определяет оператора и регион по номеру телефона"""
    info = {"operator": "Неизвестно", "region": "Неизвестно"}
    
    clean_phone = re.sub(r'[^0-9]', '', phone)
    if clean_phone.startswith('7') or clean_phone.startswith('8'):
        clean_phone = clean_phone[-10:]
    
    if len(clean_phone) >= 3:
        code = clean_phone[:3]
        operators = {
            '901': 'МТС', '902': 'МТС', '903': 'МТС', '904': 'МТС', '905': 'МТС',
            '906': 'МТС', '907': 'МТС', '908': 'МТС', '909': 'МТС', '910': 'МТС',
            '911': 'МТС', '912': 'МТС', '913': 'МТС', '914': 'МТС', '915': 'МТС',
            '916': 'МТС', '917': 'МТС', '918': 'МТС', '919': 'МТС', '920': 'МТС',
            '921': 'МТС', '922': 'МТС', '923': 'МТС', '924': 'МТС', '925': 'МТС',
            '926': 'МТС', '927': 'МТС', '928': 'МТС', '929': 'МТС', '930': 'МТС',
            '931': 'МТС', '932': 'МТС', '933': 'МТС', '934': 'МТС', '935': 'МТС',
            '936': 'МТС', '937': 'МТС', '938': 'МТС', '939': 'МТС', '940': 'МТС',
            '941': 'МТС', '942': 'МТС', '943': 'МТС', '944': 'МТС', '945': 'МТС',
            '946': 'МТС', '947': 'МТС', '948': 'МТС', '949': 'МТС', '950': 'МТС',
            '951': 'МТС', '952': 'МТС', '953': 'МТС', '954': 'МТС', '955': 'МТС',
            '956': 'МТС', '957': 'МТС', '958': 'МТС', '959': 'МТС', '960': 'МТС',
            '961': 'МТС', '962': 'МТС', '963': 'МТС', '964': 'МТС', '965': 'МТС',
            '966': 'МТС', '967': 'МТС', '968': 'МТС', '969': 'МТС', '970': 'МТС',
            '971': 'МТС', '972': 'МТС', '973': 'МТС', '974': 'МТС', '975': 'МТС',
            '976': 'МТС', '977': 'МТС', '978': 'МТС', '979': 'МТС', '980': 'МТС',
            '981': 'МТС', '982': 'МТС', '983': 'МТС', '984': 'МТС', '985': 'МТС',
            '986': 'МТС', '987': 'МТС', '988': 'МТС', '989': 'МТС', '990': 'МТС',
            '991': 'МТС', '992': 'МТС', '993': 'МТС', '994': 'МТС', '995': 'МТС',
            '996': 'МТС', '997': 'МТС', '998': 'МТС', '999': 'МТС',
            '900': 'Билайн', '901': 'Билайн', '902': 'Билайн', '903': 'Билайн',
            '904': 'Билайн', '905': 'Билайн', '906': 'Билайн', '907': 'Билайн',
            '908': 'Билайн', '909': 'Билайн', '910': 'Билайн', '911': 'Билайн',
            '912': 'Билайн', '913': 'Билайн', '914': 'Билайн', '915': 'Билайн',
            '916': 'Билайн', '917': 'Билайн', '918': 'Билайн', '919': 'Билайн',
            '920': 'Билайн', '921': 'Билайн', '922': 'Билайн', '923': 'Билайн',
            '924': 'Билайн', '925': 'Билайн', '926': 'Билайн', '927': 'Билайн',
            '928': 'Билайн', '929': 'Билайн', '930': 'Билайн', '931': 'Билайн',
            '932': 'Билайн', '933': 'Билайн', '934': 'Билайн', '935': 'Билайн',
            '936': 'Билайн', '937': 'Билайн', '938': 'Билайн', '939': 'Билайн',
            '940': 'Билайн', '941': 'Билайн', '942': 'Билайн', '943': 'Билайн',
            '944': 'Билайн', '945': 'Билайн', '946': 'Билайн', '947': 'Билайн',
            '948': 'Билайн', '949': 'Билайн', '950': 'Билайн', '951': 'Билайн',
            '952': 'Билайн', '953': 'Билайн', '954': 'Билайн', '955': 'Билайн',
            '956': 'Билайн', '957': 'Билайн', '958': 'Билайн', '959': 'Билайн',
            '960': 'Билайн', '961': 'Билайн', '962': 'Билайн', '963': 'Билайн',
            '964': 'Билайн', '965': 'Билайн', '966': 'Билайн', '967': 'Билайн',
            '968': 'Билайн', '969': 'Билайн',
            '910': 'Мегафон', '911': 'Мегафон', '912': 'Мегафон', '913': 'Мегафон',
            '914': 'Мегафон', '915': 'Мегафон', '916': 'Мегафон', '917': 'Мегафон',
            '918': 'Мегафон', '919': 'Мегафон', '920': 'Мегафон', '921': 'Мегафон',
            '922': 'Мегафон', '923': 'Мегафон', '924': 'Мегафон', '925': 'Мегафон',
            '926': 'Мегафон', '927': 'Мегафон', '928': 'Мегафон', '929': 'Мегафон',
            '930': 'Мегафон', '931': 'Мегафон', '932': 'Мегафон', '933': 'Мегафон',
            '934': 'Мегафон', '935': 'Мегафон', '936': 'Мегафон', '937': 'Мегафон',
            '938': 'Мегафон', '939': 'Мегафон', '940': 'Мегафон', '941': 'Мегафон',
            '942': 'Мегафон', '943': 'Мегафон', '944': 'Мегафон', '945': 'Мегафон',
            '946': 'Мегафон', '947': 'Мегафон', '948': 'Мегафон', '949': 'Мегафон',
            '950': 'Мегафон', '951': 'Мегафон', '952': 'Мегафон', '953': 'Мегафон',
            '954': 'Мегафон', '955': 'Мегафон', '956': 'Мегафон', '957': 'Мегафон',
            '958': 'Мегафон', '959': 'Мегафон', '960': 'Мегафон', '961': 'Мегафон',
            '962': 'Мегафон', '963': 'Мегафон', '964': 'Мегафон', '965': 'Мегафон',
            '966': 'Мегафон', '967': 'Мегафон', '968': 'Мегафон', '969': 'Мегафон',
            '900': 'Tele2', '901': 'Tele2', '902': 'Tele2', '903': 'Tele2',
            '904': 'Tele2', '905': 'Tele2', '906': 'Tele2', '907': 'Tele2',
            '908': 'Tele2', '909': 'Tele2', '910': 'Tele2', '911': 'Tele2',
            '912': 'Tele2', '913': 'Tele2', '914': 'Tele2', '915': 'Tele2',
            '916': 'Tele2', '917': 'Tele2', '918': 'Tele2', '919': 'Tele2',
            '950': 'Tele2', '951': 'Tele2', '952': 'Tele2', '953': 'Tele2',
            '954': 'Tele2', '955': 'Tele2', '956': 'Tele2', '957': 'Tele2',
            '958': 'Tele2', '959': 'Tele2', '960': 'Tele2', '961': 'Tele2',
            '962': 'Tele2', '963': 'Tele2', '964': 'Tele2', '965': 'Tele2',
            '966': 'Tele2', '967': 'Tele2', '968': 'Tele2', '969': 'Tele2',
            '970': 'Tele2', '971': 'Tele2', '972': 'Tele2', '973': 'Tele2',
            '974': 'Tele2', '975': 'Tele2', '976': 'Tele2', '977': 'Tele2',
            '978': 'Tele2', '979': 'Tele2', '980': 'Tele2', '981': 'Tele2',
            '982': 'Tele2', '983': 'Tele2', '984': 'Tele2', '985': 'Tele2',
            '986': 'Tele2', '987': 'Tele2', '988': 'Tele2', '989': 'Tele2',
        }
        info["operator"] = operators.get(code, "Неизвестно")
        
        regions = {
            '495': 'Москва', '499': 'Москва', '496': 'Московская обл.',
            '812': 'Санкт-Петербург', '813': 'Ленинградская обл.',
            '343': 'Екатеринбург', '383': 'Новосибирск',
            '845': 'Саратов', '846': 'Самара', '347': 'Уфа',
            '843': 'Казань', '861': 'Краснодар', '863': 'Ростов-на-Дону',
        }
        info["region"] = regions.get(code, "Неизвестно")
    
    return info

def osint_scan(target, progress_callback=None):
    results = {
        "target": target,
        "timestamp": datetime.now().isoformat(),
        "type": detect_input_type(target),
        "social": {},
        "breaches": [],
        "whois": None,
        "telegram": None,
        "vk": None,
        "instagram": None,
        "phone_info": None,
        "getcontact": None,
        "status": "completed"
    }
    
    steps = []
    
    if results["type"] == "phone":
        steps = [
            ("📞 Определение оператора и региона...", "phone_info"),
            ("📱 Проверка в Telegram...", "telegram"),
            ("📘 Проверка в GetContact...", "getcontact"),
        ]
    elif results["type"] == "email":
        steps = [
            ("📧 Проверка email на утечки...", "breaches"),
            ("📱 Поиск в Telegram...", "telegram"),
            ("📘 Поиск в VK...", "vk"),
        ]
    elif results["type"] == "id":
        steps = [
            ("📱 Поиск ID в Telegram...", "telegram"),
            ("📘 Поиск ID в VK...", "vk"),
            ("📸 Поиск ID в Instagram...", "instagram"),
        ]
    elif results["type"] == "domain":
        steps = [
            ("🏷️ WHOIS для домена...", "whois"),
        ]
    else:
        steps = [
            ("🌐 Поиск в соцсетях...", "social"),
            ("📱 Поиск в Telegram...", "telegram"),
            ("📘 Поиск в VK...", "vk"),
        ]
    
    total_steps = len(steps)
    current_step = 0
    
    if results["type"] == "phone":
        try:
            phone_info = get_phone_info(target)
            results["phone_info"] = phone_info
        except:
            results["phone_info"] = {"operator": "Ошибка", "region": "Ошибка"}
        
        current_step += 1
        if progress_callback:
            progress_callback(current_step, total_steps, steps[0][0])
        
        try:
            clean_phone = re.sub(r'[^0-9]', '', target)
            tg_url = f"https://t.me/{clean_phone}"
            response = requests.get(tg_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200 and "tgme_page_extra" in response.text:
                results["telegram"] = {
                    "url": tg_url,
                    "exists": True,
                    "method": "по номеру"
                }
            else:
                search_url = f"https://t.me/s/{clean_phone}"
                response2 = requests.get(search_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if response2.status_code == 200:
                    results["telegram"] = {
                        "url": search_url,
                        "exists": True,
                        "method": "поиск"
                    }
                else:
                    results["telegram"] = {"exists": False, "message": "❌ Не найден"}
        except:
            results["telegram"] = {"exists": False, "error": "❌ Ошибка проверки"}
        
        current_step += 1
        if progress_callback:
            progress_callback(current_step, total_steps, steps[1][0])
        
        try:
            clean_phone = re.sub(r'[^0-9]', '', target)
            gc_url = f"https://api.getcontact.com/number/{clean_phone}"
            response = requests.get(gc_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                results["getcontact"] = {"exists": True, "data": response.text[:200]}
            else:
                results["getcontact"] = {"exists": False, "message": "❌ Не найден в базе"}
        except:
            results["getcontact"] = {"exists": False, "error": "❌ Ошибка проверки"}
        
        current_step += 1
        if progress_callback:
            progress_callback(current_step, total_steps, steps[2][0])
    
    if results["type"] == "email":
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
    
    if results["type"] in ["id", "username"]:
        try:
            if results["type"] == "id":
                tg_check = f"https://t.me/id{target}"
            else:
                tg_check = f"https://t.me/{target}"
            response = requests.get(tg_check, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200 and "tgme_page_extra" in response.text:
                results["telegram"] = {
                    "url": tg_check,
                    "exists": True
                }
            else:
                results["telegram"] = {"exists": False, "message": "❌ Не найден"}
        except:
            results["telegram"] = {"exists": False, "error": "❌ Ошибка проверки"}
        
        current_step += 1
        if progress_callback and current_step <= len(steps):
            progress_callback(current_step, total_steps, steps[current_step-1][0] if steps else ("", ""))
        
        try:
            if results["type"] == "id":
                vk_url = f"https://vk.com/id{target}"
            else:
                vk_url = f"https://vk.com/{target}"
            response = requests.get(vk_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200 and "page_name" in response.text.lower():
                results["vk"] = {
                    "url": vk_url,
                    "exists": True
                }
            else:
                results["vk"] = {"exists": False, "message": "❌ Не найден"}
        except:
            results["vk"] = {"exists": False, "error": "❌ Ошибка проверки"}
        
        current_step += 1
        if progress_callback and current_step <= len(steps):
            progress_callback(current_step, total_steps, steps[current_step-1][0] if steps else ("", ""))
        
        if results["type"] == "username":
            try:
                inst_url = f"https://instagram.com/{target}"
                response = requests.get(inst_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                if response.status_code == 200 and "instagram" in response.text.lower():
                    results["instagram"] = {
                        "url": inst_url,
                        "exists": True
                    }
                else:
                    results["instagram"] = {"exists": False, "message": "❌ Не найден"}
            except:
                results["instagram"] = {"exists": False, "error": "❌ Ошибка проверки"}
            
            current_step += 1
            if progress_callback and current_step <= len(steps):
                progress_callback(current_step, total_steps, steps[current_step-1][0] if steps else ("", ""))
    
    if results["type"] == "username":
        socials = {
            "GitHub": f"https://github.com/{target}",
            "Twitter": f"https://twitter.com/{target}",
            "Reddit": f"https://reddit.com/user/{target}",
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
        
        if len(steps) > 0 and current_step < len(steps):
            current_step += 1
            if progress_callback:
                progress_callback(current_step, total_steps, steps[current_step-1][0] if steps else ("", ""))
    
    if results["type"] == "domain":
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
            progress_callback(current_step, total_steps, steps[0][0])
    
    return results

def print_results(data):
    print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
    print(Fore.CYAN + "║        📊 РЕЗУЛЬТАТЫ OSINT          ║")
    print(Fore.CYAN + "╚════════════════════════════════════════╝\n")
    
    print(Fore.YELLOW + f"🎯 Цель: {Fore.WHITE}{data['target']}")
    print(Fore.YELLOW + f"📌 Тип: {Fore.WHITE}{data['type']}")
    print(Fore.YELLOW + f"🕐 Время: {Fore.WHITE}{data['timestamp'][:19]}\n")
    
    if data.get('phone_info'):
        print(Fore.CYAN + "📞 ИНФОРМАЦИЯ О НОМЕРЕ:")
        for key, value in data['phone_info'].items():
            if value:
                print(f"   {Fore.WHITE}{key.capitalize()}: {Fore.GREEN}{value}")
        print()
    
    if data.get('getcontact'):
        if data['getcontact'].get('exists'):
            print(Fore.BLUE + f"📘 GETCONTACT: {Fore.WHITE}Найден в базе")
        else:
            print(Fore.RED + f"📘 GETCONTACT: {data['getcontact'].get('message', '❌ Не найден')}")
        print()
    
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
            if data['telegram'].get('method'):
                print(f"   {Fore.WHITE}Метод: {Fore.CYAN}{data['telegram']['method']}")
        else:
            print(Fore.RED + f"📱 TELEGRAM: {data['telegram'].get('message', '❌ Не найден')}")
        print()
    
    if data.get('vk'):
        if data['vk'].get('exists'):
            print(Fore.BLUE + f"📘 VK: {Fore.WHITE}{data['vk']['url']}")
        else:
            print(Fore.RED + f"📘 VK: {data['vk'].get('message', '❌ Не найден')}")
        print()
    
    if data.get('instagram'):
        if data['instagram'].get('exists'):
            print(Fore.MAGENTA + f"📸 INSTAGRAM: {Fore.WHITE}{data['instagram']['url']}")
        else:
            print(Fore.RED + f"📸 INSTAGRAM: {data['instagram'].get('message', '❌ Не найден')}")
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
    print(Fore.CYAN + "📌 Функ
