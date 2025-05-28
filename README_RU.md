# 🚀 EPT-MX-ADM v0.0.1-beta

Современная панель администратора для сервера Matrix Synapse

![EPT-MX-ADM](https://img.shields.io/badge/Matrix-Admin-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-green?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-2.3+-red?style=flat-square)
![Multilingual](https://img.shields.io/badge/i18n-EN%20%7C%20RU%20%7C%20DE%20%7C%20FR%20%7C%20IT%20%7C%20ES%20%7C%20TR-orange?style=flat-square)
![Beta](https://img.shields.io/badge/Status-BETA-yellow?style=flat-square)

## ⚠️ ПРЕДУПРЕЖДЕНИЕ О БЕТА-ВЕРСИИ

**🚧 Это БЕТА-версия (v0.0.1-beta) — Работа в процессе!**

- 🔨 **Многие функции все еще в разработке**
- 🐛 **Ожидаются ошибки и проблемы**
- 📝 **Документация может быть неполной**
- 🔄 **Возможны критические изменения**
- ⚡ **Используйте на свой страх и риск в продакшене**

**Проект активно разрабатывается. Ожидайте частых обновлений и изменений.**

**EPT-MX-ADM v0.0.1-beta — бета-тест успешно завершён! 🎉 Всё работает: управление пользователями, комнатами, медиа, дашборд и 7 языков — уже в деле! 🔥 Но мы всё ещё шлифуем детали для совершенства. Это бета, не релиз, так что пробуйте, делитесь отзывами и помогайте сделать идеальную админ-панель для Matrix! 😎 #BetaVibes**

## 🧪 Демо / Попробовать онлайн

Вы можете попробовать EPT-MX-ADM онлайн без установки:

- **Демо-URL:** [https://admin.matrix.easypro.tech/](https://admin.matrix.easypro.tech/)
- **Пользователь:** `qwe`
- **Пароль:** `qwe`

> Это публичная демо-версия для ознакомления. Все изменения временные, окружение может быть сброшено в любой момент.

## 💡 Почему я создал EPT-MX-ADM

> *От автора — Brabus*

Я Brabus, и мне не всё равно. Matrix — отличная платформа, но её инструменты администрирования **ужасны**:

- **Synapse Admin** с устаревшим интерфейсом 😤
- Вечные **CORS ошибки** 🤬
- **Nginx-конфиги**, которые съедают часы ⏰
- **Документация**, где ответ — "просто погугли" 🔍

Админы тратят время на **борьбу с инструментом** вместо управления сервером.

**Я решил это исправить.**

EPT-MX-ADM — это админ-панель, которая **действительно работает**: модульная, многоязычная, с чистым интерфейсом и аналитикой. Сделано для вас, чтобы вы управляли Matrix **с удовольствием, а не с болью**.

*От EasyProTech — мы создаём технологии, которые помогают людям.* 😎

## ✨ Возможности

### 🎯 Текущий функционал (Бета)
- **👥 Управление пользователями** — создание, редактирование, деактивация пользователей *(реализовано)*
- **🏠 Управление комнатами** — просмотр, поиск, блокировка и удаление комнат *(в разработке)*
- **🌐 Управление пространствами** — просмотр иерархии Matrix Spaces *(запланировано)*
- **📁 Управление медиафайлами** — просмотр, фильтрация, карантин и удаление медиафайлов *(бета)*
- **📊 Дашборд** — обзор сервера и ключевые метрики *(базовая версия)*
- **🔐 Безопасная авторизация** — через Matrix API с проверкой прав администратора *(работает)*
- **🌍 Многоязычная поддержка** — поддержка 7 языков (EN, RU, DE, FR, IT, ES, TR) *(частично)*
- **📱 Адаптивный дизайн** — работает на всех устройствах *(в процессе)*
- **🔍 Мощный поиск** — по пользователям, комнатам, пространствам и медиафайлам *(ограниченно)*

### 🚧 Запланированные функции
- **📈 Расширенная аналитика** — графики активности, метрики
- **🌐 Управление федерацией** — управление серверами, блокировка
- **📋 Логи и аудит** — просмотр, фильтрация, экспорт
- **⚙️ Конфигурация** — редактор настроек через интерфейс
- **🚨 Мониторинг** — оповещения, уведомления, live-данные

## 📸 Скриншоты

### 🔐 Страница входа
![Login Page](screen/login-page.png)
*Чистый и современный интерфейс входа с тёмной темой*

### 📊 Дашборд
![Dashboard](screen/dashboard.png)
*Обзор сервера и ключевые метрики*

### 👥 Управление пользователями
![User Management](screen/user-management.png)
*Комплексный интерфейс администрирования пользователей*

### ✏️ Редактирование пользователя
![User Editing](screen/edit_user.png)
*Инструменты редактирования профиля и администрирования*

### 👤 Профиль пользователя
![User Profile](screen/user_profile.png)
*Детальный просмотр профиля и информации*

### 🏠 Управление комнатами
![Room Management](screen/room-management.png)
*Инструменты просмотра, поиска и управления комнатами*

### 🏠 Детали комнаты
![Room Details](screen/room_view.png)
*Детальная информация о комнате и настройки*

### 🌐 Управление пространствами
![Space Management](screen/space.png)
*Иерархия и управление Matrix Spaces*

### 📁 Управление медиафайлами
![Media Management](screen/media-management.png)
*Обзор и инструменты управления медиафайлами пользователей*

## 🌍 Многоязычная поддержка

### Доступные языки
- **🇬🇧 Английский**
- **🇷🇺 Русский**
- **🇩🇪 Немецкий**
- **🇫🇷 Французский**
- **🇮🇹 Итальянский**
- **🇪🇸 Испанский**
- **🇹🇷 Турецкий**
- **🇨🇳 Китайский**
- **🇯🇵 Японский**
- **🇦🇪 Арабский**
- **🇮🇱 Иврит**

> Все переводы завершены и полностью соответствуют английской версии на 28.05.2025.

### Переключение языка
- Переключатель языка на странице входа (правый нижний угол)
- Флаги стран для визуального распознавания
- Автоматическое сохранение выбранного языка

### Локализация включает
- ✅ Все элементы интерфейса
- ✅ Сообщения об ошибках
- ✅ Валидация форм
- ✅ Всплывающие подсказки
- ✅ JavaScript-уведомления

Всё вышеперечисленное полностью переведено на все поддерживаемые языки.

## 🔧 Архитектура

```
ept-mx-adm/
├── app.py                    # Основное приложение Flask
├── config/                   # Файлы конфигурации
│   └── settings.py          # Основные настройки
├── blueprints/              # Flask blueprints для модульной маршрутизации
│   ├── __init__.py         # Инициализация blueprints
│   ├── auth.py             # Маршруты аутентификации
│   ├── users.py            # Маршруты управления пользователями
│   ├── rooms.py            # Маршруты управления комнатами
│   ├── spaces.py           # Маршруты управления пространствами
│   ├── media.py            # Маршруты управления медиа
│   └── dashboard.py        # Маршруты панели управления
├── modules/                 # Основные функциональные модули
│   ├── __init__.py         # Инициализация модулей
│   ├── auth.py             # Авторизация и разрешения
│   ├── users.py            # Управление пользователями
│   ├── rooms.py            # Управление комнатами
│   ├── spaces.py           # Управление пространствами
│   ├── media.py            # Управление медиафайлами
│   └── analytics.py        # Аналитика и статистика
├── templates/              # Jinja2 HTML шаблоны
├── static/                # Статические файлы
│   ├── css/              # CSS стили
│   ├── js/               # JavaScript файлы
│   └── vendor/           # Внешние библиотеки
├── utils/                # Вспомогательные функции
│   ├── __init__.py      # Инициализация утилит
│   ├── api_client.py    # Matrix API клиент
│   ├── i18n.py          # Система локализации
│   └── logger.py        # Система логирования
├── locales/             # Переводы (7 языков)
│   ├── en.json         # Английский язык
│   ├── ru.json         # Русский язык
│   ├── de.json         # Немецкий язык
│   ├── fr.json         # Французский язык
│   ├── it.json         # Итальянский язык
│   ├── es.json         # Испанский язык
│   └── tr.json         # Турецкий язык
└── requirements.txt     # Python зависимости
```

## 🚀 Быстрый старт

### ⚠️ Уведомление о бета-установке
**Это бета-версия. Некоторые функции могут работать не так, как ожидается.**

### 📂 Рекомендации по развертыванию

**Для Linux серверов:**
```bash
# Рекомендуемое расположение
/opt/ept-mx-adm/          # Основной вариант (рекомендуется)
/var/www/matrix-admin/    # Альтернатива для веб-серверов  
/home/matrix/admin/       # Для пользовательской установки
```

**Права доступа:**
- **Владелец**: отдельный пользователь (например, `matrix` или `www-data`)
- **Права**: `755` для папок, `644` для файлов
- **Запуск**: НЕ от root (создайте отдельного пользователя)

**Пример создания структуры:**
```bash
# Создание пользователя для панели администрирования Matrix
sudo useradd -r -s /bin/bash -d /opt/ept-mx-adm matrix-admin

# Создание директории и установка прав
sudo mkdir -p /opt/ept-mx-adm
sudo chown matrix-admin:matrix-admin /opt/ept-mx-adm

# Переключение на пользователя для установки
sudo -u matrix-admin bash
cd /opt/ept-mx-adm

# Клонирование проекта
git clone https://github.com/EPTLLC/EPT-MX-ADM.git .
```

### Требования
- Python 3.10+
- Matrix Synapse сервер с включённым Admin API
- Учётная запись администратора Matrix

## 🔧 Быстрая установка одной командой

```bash
# Полная установка со всеми ресурсами (запустить в папке проекта)
pip3 install -r requirements.txt && \
mkdir -p static/vendor/{bootstrap/{css,js},bootstrap-icons/fonts,chartjs} && \
curl -o static/vendor/bootstrap/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css && \
curl -o static/vendor/bootstrap/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js && \
curl -o static/vendor/bootstrap-icons/bootstrap-icons.css https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css && \
curl -o static/vendor/bootstrap-icons/fonts/bootstrap-icons.woff https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff && \
curl -o static/vendor/bootstrap-icons/fonts/bootstrap-icons.woff2 https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/bootstrap-icons.woff2 && \
curl -o static/vendor/chartjs/chart.min.js https://cdn.jsdelivr.net/npm/chart.js && \
sed -i 's|https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/fonts/|../bootstrap-icons/fonts/|g' static/vendor/bootstrap-icons/bootstrap-icons.css && \
echo "✅ EPT-MX-ADM готов к запуску!"
```

### ⚙️ Конфигурация

1. **Отредактируйте** `config/settings.py`:
```python
SYNAPSE_URL = "https://your-domain.com"  # URL вашего сервера Synapse
DEFAULT_LOCALE = "en"                    # Язык по умолчанию (en/ru)
```

2. **Важно**: URL должен соответствовать тому, как вы обращаетесь к админ-панели!

### 🚀 Запуск

```bash
# Обычный запуск
python3 app.py

# Фоновый режим
nohup python3 app.py > logs/app.log 2>&1 &

# Продакшн (с Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 🌐 Доступ

- **URL**: `http://localhost:5000` или `https://admin.your-domain.com`
- **Логин**: ваш Matrix ID (например, `@admin:your-domain.com`)
- **Пароль**: пароль учётной записи Matrix
- **Требования**: права администратора на сервере Synapse

## 🔧 Технологии

- **Бэкенд**: Python 3.10+, Flask 2.3+
- **Фронтенд**: Bootstrap 5.3, Chart.js
- **Аутентификация**: Matrix API
- **База данных**: отсутствует (использует Matrix API)
- **Локализация**: собственная система i18n
- **Логирование**: собственная система логирования

## 📝 Лицензия

Этот проект распространяется под лицензией MIT — см. файл LICENSE.

## 🤝 Вклад

Вклад приветствуется! Не стесняйтесь отправлять Pull Request.

## 📞 Поддержка

Для поддержки, пожалуйста, создайте issue в репозитории GitHub.

## 🙏 Благодарности

- Команде Matrix.org за отличную платформу
- Команде Flask за прекрасный фреймворк
- Всем контрибьюторам и тестировщикам

#### 🇬🇧 Overview
Modern administration panel for Matrix Synapse.
*Translation is fully up-to-date as of 2025-05-28.*

#### 🇷🇺 Описание
Современная панель администратора для Matrix Synapse.
*Перевод полностью соответствует английской версии на 28.05.2025.*

#### 🇩🇪 Übersicht
Modernes Administrationspanel für Matrix Synapse.
*Die Übersetzung entspricht vollständig der englischen Version vom 28.05.2025.*

#### 🇫🇷 Présentation
Panneau d'administration moderne pour Matrix Synapse.
*La traduction est entièrement conforme à la version anglaise du 28.05.2025.*

#### 🇮🇹 Descrizione
Pannello di amministrazione moderno per Matrix Synapse.
*La traduzione è completamente aggiornata alla versione inglese del 28.05.2025.*

#### 🇪🇸 Descripción
Panel de administración moderno para Matrix Synapse.
*La traducción está completamente actualizada a la versión en inglés del 28.05.2025.*

#### 🇹🇷 Açıklama
Matrix Synapse için modern yönetim paneli.
*Çeviri, 28.05.2025 tarihli İngilizce sürümle tamamen uyumludur.*

#### 🇨🇳 简介
现代化的 Matrix Synapse 管理面板。
*本地化完全符合英语版本，截至2025年5月28日*

#### 🇯🇵 概要
モダンな Matrix Synapse 管理パネル。
*ローカライズは2025年5月28日時点の英語版と一致しています*

#### 🇦🇪 نظرة عامة
لوحة إدارة حديثة لـ Matrix Synapse.
*الترجمة مطابقة للنسخة الإنجليزية بتاريخ 28.05.2025*

#### 🇮🇱 תקציר
פאנל ניהול מודרני ל-Matrix Synapse.
*התרגום תואם לגרסה האנגלית נכון ל־28.05.2025* 