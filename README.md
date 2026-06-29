🐼 OSINT Scanner Pro

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/panda.png" alt="Panda">
</p>

<p align="center">
  <strong>Мощный OSINT-сканер для Termux с красивым интерфейсом и пандой 🐼</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python">
  <img src="https://img.shields.io/badge/Platform-Termux-green?style=flat&logo=android">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat">
  <img src="https://img.shields.io/github/stars/r62983218-dev/Osint?style=social">
</p>

## ✨ Возможности

- 📧 Проверка email на утечки (HaveIBeenPwned)
- 📱 Поиск профиля в Telegram
- 📘 Поиск профиля в VK
- 🌐 Поиск в соцсетях (GitHub, Twitter, Instagram, TikTok)
- 🏷️ WHOIS для доменов
- 📄 Сохранение отчётов в JSON
- 🐼 Крутой ASCII-арт с пандой
- 📊 Красивый прогресс-бар
- 🎨 Цветной интерфейс


## 📱 Установка и запуск (Termux)

**1️⃣ Обновление пакетов**
```bash
pkg update && pkg upgrade -y
```

2️⃣ Установка Python и Git

```bash
pkg install python git -y
```

3️⃣ Клонирование репозитория

```bash
git clone https://github.com/r62983218-dev/Osint
```

4️⃣ Переход в папку проекта

```bash
cd Osint
```

5️⃣ Запуск сканера (всё установится автоматически)

```bash
python osint.py
```

Примечание: При первом запуске автоматически установятся все необходимые библиотеки.


🎮 Пример работы

```bash
🔍 Начинаем сканирование: example@mail.com

┃██████████████████████████████┃ 100% Проверка email на утечки...
┃██████████████████████████████┃ 100% Поиск в Telegram...
┃██████████████████████████████┃ 100% Поиск в VK...
