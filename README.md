Как запустить osint-tool-RAZE в Termux

Установка необходимых компонентов

1. Обновление пакетов Termux

```bash
pkg update && pkg upgrade -y
```

2. Установка Python и Git

```bash
pkg install python git -y
```

3. Установка необходимых Python-библиотек

```bash
pkg install python-pip -y
pip install requests beautifulsoup4 selenium
```

Клонирование репозитория

```bash
git clone https://github.com/Razehtml/osint-tool-RAZE.git
cd osint-tool-RAZE
```

Запуск инструмента

```bash
python osint_tool_RAZE.py
```

Возможные проблемы и решения

Если Python не найден

```bash
pkg install python
```

Если ошибка с правами доступа

```bash
chmod +x osint_tool_RAZE.py
```

Если выдается ошибка с модулями

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Дополнительные советы

· Для получения справки по инструменту:

```bash
python osint_tool_RAZE.py --help
```

· Для ввода нужных параметров:

```bash
python osint_tool_RAZE.py -u [URL или никнейм]
```

Примечания

· Убедитесь, что у вас стабильное интернет-соединение
· Некоторые функции могут требовать дополнительных разрешений в Termux
· Для работы с графическими элементами может потребоваться установка Termux:API
