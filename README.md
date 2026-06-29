📱 Установка и запуск (Termux)

```bash
# 1. Обновление пакетов
pkg update && pkg upgrade -y

# 2. Установка Python и Git
pkg install python git -y

# 3. Клонирование репозитория
git clone https://github.com/r62983218-dev/Osint
cd Osint

# 4. Запуск сканера (всё установится автоматически)
python osint.py
