#!/data/data/com.termux/files/usr/bin/python

import subprocess
import sys
import time
from colorama import Fore, init

init(autoreset=True)

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result
    except:
        return None

print(Fore.CYAN + "╔════════════════════════════════════════════════════╗")
print(Fore.CYAN + "║         🚀 УСТАНОВКА ЗАВИСИМОСТЕЙ ДЛЯ TERMUX       ║")
print(Fore.CYAN + "╚════════════════════════════════════════════════════╝\n")

# Обновляем Termux
print(Fore.CYAN + "🔄 Обновление репозиториев...")
subprocess.run(["pkg", "update", "-y"], check=False)

# Системные пакеты
system_packages = {
    "python": "Python",
    "python-pip": "pip",
    "git": "Git",
    "clang": "Clang",
    "libxml2": "libxml2",
    "libxslt": "libxslt"
}

print(Fore.CYAN + "\n🔧 Установка системных пакетов:\n")

for pkg, name in system_packages.items():
    print(f"🔍 Проверка {name}...", end=" ")
    result = run_command(["pkg", "list-installed", pkg])
    if result and result.returncode == 0 and pkg in result.stdout:
        print(Fore.GREEN + "✅ Уже установлен")
    else:
        print(Fore.YELLOW + "❌ Устанавливаю...")
        if run_command(["pkg", "install", pkg, "-y"]):
            print(Fore.GREEN + f"✅ {name} установлен")
        else:
            print(Fore.RED + f"❌ Ошибка при установке {name}")

# Python библиотеки
python_libs = [
    "colorama", "requests", "python-whois", "pandas", 
    "numpy", "matplotlib", "openpyxl", "beautifulsoup4", "lxml"
]

print(Fore.CYAN + "\n\n📚 Установка Python-библиотек:\n")

for lib in python_libs:
    print(f"🔍 Проверка {lib}...", end=" ")
    try:
        import_name = "whois" if lib == "python-whois" else lib.replace("-", "_").replace("4", "")
        __import__(import_name)
        print(Fore.GREEN + "✅ Уже установлена")
    except ImportError:
        print(Fore.YELLOW + "❌ Устанавливаю...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", lib, "--quiet", "--upgrade"], 
                         check=True)
            print(Fore.GREEN + f"✅ {lib} установлен")
        except:
            print(Fore.RED + f"❌ Не удалось установить {lib}")

print(Fore.GREEN + "\n" + "═" * 55)
print(Fore.GREEN + "🎉 ВСЕ ЗАВИСИМОСТИ УСТАНОВЛЕНЫ УСПЕШНО!")
print(Fore.GREEN + "═" * 55)
print(Fore.CYAN + "\nГотов к использованию! 🚀\n")

time.sleep(2)
