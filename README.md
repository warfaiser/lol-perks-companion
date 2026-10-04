# ⚔️ League of Legends: Perks & Champions Guide Companion

[![GitHub release](https://img.shields.io/badge/Release-v1.0.0-blue.svg)](https://github.com/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Web-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-gold.svg)]()
[![LoL Version](https://img.shields.io/badge/LoL%20Data-v16.19.1%20RU-red.svg)]()

> Интерактивная энциклопедия и настольное ПК-приложение (.EXE) для League of Legends: подробные гайды по всем 173 чемпионам, веткам рун (перкам), оптимальным сборкам предметов и рекомендациям для **новичков** и **опытных игроков (ветеранов)**.

---

## 🌟 Возможности проекта

- 🎮 **Все 173 чемпиона:** актуальная статистика, умения, распределение по линиям (Top, Mid, Jungle, Bot, Support) и рекомендуемые билды.
- 🔮 **Полная система перков и рун:** 5 великих ветвей (*Точность*, *Доминирование*, *Колдовство*, *Храбрость*, *Вдохновение*) с интерактивными тултипами, описаниями урона и перезарядок.
- 🌱 **Гайды новичок vs опытный:** подборка чемпионов с легким порогом входа и чемпионов с наивысшим потолком навыка (*High Skill-Cap*), советы по контролю карты и крипов.
- 💻 **ПК-приложение (.EXE):** автономный исполняемый файл размером ~650 КБ, не требующий установки зависимостей, с поддержкой нативного режима окна Windows.
- 🌐 **Web-версия (GitHub Pages):** возможность открыть руководство онлайн прямо из браузера или телефона.

---

## 🚀 Быстрый запуск

### 1. Скачать готовое приложение для Windows (.EXE)
Перейдите в раздел [**Releases**](../../releases) и скачайте `LoL_Perks_App.exe`. Запустите двойным кликом — приложение готово к работе!

### 2. Запуск Web-версии локально
Просто откройте файл `index.html` в любом современном веб-браузере (Chrome, Edge, Firefox, Opera, Safari) или поднимите локальный сервер:
```bash
python -m http.server 3000
```
Затем перейдите по адресу: [http://localhost:3000](http://localhost:3000)

---

## 🛠️ Сборка из исходников

### Требования
- Компилятор MinGW-w64 (`x86_64-w64-mingw32-gcc` или MSVC на Windows)
- Python 3.8+ (для обновления данных Data Dragon)

### Пошаговая сборка:

1. **Клонирование репозитория:**
```bash
git clone https://github.com/YOUR_USERNAME/lol-perks-companion.git
cd lol-perks-companion
```

2. **(Опционально) Обновление базы данных чемпионов и перков:**
```bash
python scripts/build_data.py
```

3. **Компиляция бинарного исполняемого файла (.exe):**
```bash
# На Linux (кросс-компиляция через MinGW) или Windows (MinGW/MSYS2):
make
# Либо прямой командой:
x86_64-w64-mingw32-windres assets/resource.rc -O coff -o bin/resource.res
x86_64-w64-mingw32-gcc -mwindows -O2 -s src/app.c assets/resource.res -o bin/LoL_Perks_App.exe
```

---

## 📁 Структура проекта

```text
├── .github/
│   └── workflows/
│       ├── build.yml          # Автоматическая сборка .EXE и Release на GitHub Actions
│       └── pages.yml          # Автоматический деплой веб-сайта на GitHub Pages
├── assets/                    # Иконки, стили и ресурсы приложения
│   ├── app_icon.ico           # Высококачественная иконка Windows (.ico)
│   └── resource.rc            # Файл ресурсов компилятора
├── bin/                       # Скомпилированный .EXE файл
│   └── LoL_Perks_App.exe
├── data/                      # Данные Data Dragon Riot Games
│   └── data.json              # База 173 чемпионов и всех рун на русском языке
├── scripts/
│   └── build_data.py          # Скрипт синхронизации с Riot Data Dragon API
├── src/                       # Исходный код на C для нативного Windows-клиента
│   ├── app.c
│   └── embedded_data.c
├── index.html                 # Автономная веб-версия (Single Page App)
├── Makefile                   # Файл сборки Make
├── LICENSE                    # Лицензия MIT
└── README.md                  # Документация проекта
```

---

## 🌐 Публикация сайта на GitHub Pages

1. Зайдите в ваш репозиторий на GitHub: **Settings** -> **Pages**.
2. В секции **Build and deployment**:
   - **Source:** Deploy from a branch
   - **Branch:** `main` (или `master`), папка `/ (root)`
3. Нажмите **Save**. Через минуту ваш сайт будет доступен по адресу:
   `https://YOUR_USERNAME.github.io/YOUR_REPO/`

---

## ⚖️ Правовая информация (Disclaimer)

Этот проект является фанатским и справочным ресурсом. League of Legends и Riot Games являются зарегистрированными товарными знаками компании Riot Games, Inc. Проект не поддерживается и не спонсируется компанией Riot Games. Все изображения чемпионов, рун и артов принадлежат Riot Games.

---

## 📄 Лицензия

Распространяется по лицензии [MIT](LICENSE).
