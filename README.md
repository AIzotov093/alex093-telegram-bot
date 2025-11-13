# alex093-telegram-bot
Telegram bot that generates funny posts using GigaChat API with aiogram 3.x


## 킠ок запуска

### Шаг 1: Открыте Codespaces

1. Перейдите на этот репозиторий
2. Нажмите кнопку **"Code"** (зелёная кнопка)
3. Выберите вкладку **"Codespaces"**
4. Нажмите **"Create codespace on main"**

### Шаг 2: Подготовьте файл конфигурации

В терминале Codespaces выполните:

```bash
# 1. Скопируйте шаблон .env.example в .env
cp .env.example .env

# 2. Отредактируйте .env файл
nano .env
```

Заполните значения:

```
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН_ОТ_BOTFATHER

# GigaChat API Configuration
GIGACHAT_CLIENT_ID=ВАШ_CLIENT_ID
GIGACHAT_CLIENT_SECRET=ВАШ_CLIENT_SECRET
GIGACHAT_SCOPE=GIGACHAT_API_PERS
```


**Как получить эти значения:**
- **TELEGRAM_BOT_TOKEN**: Напишите @BotFather в Telegram, создайте бота и скопируйте токен
- **GIGACHAT_CLIENT_ID** и **GIGACHAT_CLIENT_SECRET**: Получите в консоли GigaChat API

### Шаг 3: Установите зависимости

```bash
pip install -r requirements.txt
```

Это установит:
- **aiogram 3.x** — фреймворк для Telegram ботов
- **aiohttp** — асинхронный HTTP клиент
- **python-dotenv** — для работы с .env файлами

### Шаг 4: Запустите бота

```bash
python3 main.py
```

Вы должны увидеть в консоли:
```
✅ Bot started polling...
INFO:root:Bot is running and ready to receive messages
```

### Шаг 5: Протестируйте бота

1. Откройте Telegram
2. Найдите вашего бота (используя @имя_бота)
3. Отправьте команду **/start**
4. Бот ответит: **"Привет! Я бот Alex093. О чем поболтаем?"**

## Функциональность бота

- ✅ **Команда /start** — приветствие и инструкция
- ✅ **Команда /help** — справка по командам  
- ✅ **Команда /cancel** — отмена операции
- ✅ **Отправка текста** → Бот генерирует смешной пост через GigaChat API
- ✅ **Форматирование** — автоматически добавляет emoji, заголовок и хештеги

## Как остановить бота

В терминале нажмите **Ctrl+C**

## Структура проекта

```
alex093-telegram-bot/
├── main.py              ← Основной файл бота
├── requirements.txt     ← Зависимости проекта
├── .env.example        ← Шаблон конфигурации
├── .env                ← Ваша конфигурация (НЕ коммитьте!)
├── .gitignore          ← Исключает .env из Git
└── README.md           ← Этот файл
```

## Возможные проблемы

| Проблема | Решение |
|----------|----------|
| `ModuleNotFoundError: No module named 'aiogram'` | Выполните `pip install -r requirements.txt` |
| `KeyError: 'TELEGRAM_BOT_TOKEN'` | Проверьте, что .env файл заполнен |
| Бот не отвечает | Проверьте интернет-соединение и токены |
