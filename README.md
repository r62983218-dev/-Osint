 🔍 OSINT Tool for Termux

Инструмент для OSINT в Termux (Android)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![GitHub](https://img.shields.io/badge/Platform-GitHub-brightgreen)

 ✨ Возможности
- 🔎 Поиск информации по GitHub пользователям
- 📦 Поиск репозиториев по ключевым словам
- 🌐 WHOIS и базовая разведка
- 📱 Адаптировано специально под Termux
- 🚀 Простая установка одним скриптом

🚀 Установка

```bash
# Обновляем Termux
pkg update && pkg upgrade -y

# Клонируем репозиторий
git clone https://github.com/r62983218-dev/-Osint.git
cd -Osint

# Запускаем установщик
python installer.py
python osint.py


├── osint.py          # Главный скрипт
├── installer.py      # Установщик зависимостей
├── requirements.txt  # Python библиотеки
└── README.md
Автор: [r62983218-dev]
