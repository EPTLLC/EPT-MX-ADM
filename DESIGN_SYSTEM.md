# 🎨 EPT-MX-ADM Design System

Единая система дизайна для обеспечения консистентности всех компонентов проекта.

## 📋 Содержание

- [🎯 Принципы](#-принципы)
- [🎨 Цветовая палитра](#-цветовая-палитра)
- [📐 Размеры и отступы](#-размеры-и-отступы)
- [🔤 Типографика](#-типографика)
- [🧱 Компоненты](#-компоненты)
- [📱 Адаптивность](#-адаптивность)
- [🌙 Темная тема](#-темная-тема)

## 🎯 Принципы

### Централизация
- Все стили управляются из одного файла `static/css/admin.css`
- CSS переменные (custom properties) для всех значений
- Никаких inline стилей в шаблонах

### Консистентность
- Единообразные компоненты на всех страницах
- Одинаковые размеры, отступы, цвета
- Унифицированная система именования классов

### Масштабируемость
- Модульная архитектура компонентов
- Переиспользуемые утилиты
- Легкое добавление новых компонентов

## 🎨 Цветовая палитра

### Основные цвета
```css
--primary-color: #4e73df;
--primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--primary-light: rgba(102, 126, 234, 0.1);
--primary-hover: rgba(102, 126, 234, 0.2);
```

### Статусные цвета
```css
--success-color: #28a745;
--warning-color: #ffc107;
--danger-color: #dc3545;
--info-color: #17a2b8;
--secondary-color: #6c757d;
```

### Нейтральные цвета
```css
--dark-color: #2c3e50;
--light-color: #f8f9fa;
--white-color: #ffffff;
--text-primary: #2c3e50;
--text-secondary: #6c757d;
--text-muted: #8a92a5;
```

### Фоны
```css
--bg-gradient: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
--bg-white: #ffffff;
--bg-glass: rgba(255, 255, 255, 0.95);
--bg-glass-dark: rgba(52, 58, 70, 0.95);
```

## 📐 Размеры и отступы

### Отступы
```css
--spacing-xs: 0.25rem;    /* 4px */
--spacing-sm: 0.5rem;     /* 8px */
--spacing: 1rem;          /* 16px */
--spacing-lg: 1.5rem;     /* 24px */
--spacing-xl: 2rem;       /* 32px */
--spacing-xxl: 3rem;      /* 48px */
```

### Скругления
```css
--border-radius-sm: 0.375rem;   /* 6px */
--border-radius: 0.75rem;       /* 12px */
--border-radius-lg: 1rem;       /* 16px */
--border-radius-xl: 1.5rem;     /* 24px */
--border-radius-pill: 50rem;    /* полное скругление */
```

### Тени
```css
--shadow-sm: 0 0.125rem 0.25rem rgba(102, 126, 234, 0.075);
--shadow: 0 0.15rem 1.75rem 0 rgba(102, 126, 234, 0.15);
--shadow-lg: 0 1rem 3rem rgba(102, 126, 234, 0.175);
--shadow-hover: 0 0.5rem 2rem rgba(102, 126, 234, 0.3);
```

## 🔤 Типографика

### Размеры шрифта
```css
--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size: 1rem;          /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.25rem;    /* 20px */
```

### Веса шрифта
```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

### Семейство шрифтов
```css
--font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
```

## 🧱 Компоненты

### Карточки
```html
<!-- Базовая карточка -->
<div class="card">
    <div class="card-header">
        <i class="bi bi-icon"></i>
        <span>Заголовок</span>
    </div>
    <div class="card-body">
        Содержимое
    </div>
    <div class="card-footer">
        Подвал
    </div>
</div>

<!-- Карточка со статусной полосой -->
<div class="card card-status">
    <!-- автоматически добавляется цветная полоса сверху -->
</div>

<!-- Элитная карточка -->
<div class="card elite-card">
    <!-- стеклянный эффект и анимации -->
</div>
```

### Кнопки
```html
<!-- Основные варианты -->
<button class="btn btn-primary">Основная</button>
<button class="btn btn-outline-primary">Контурная</button>
<button class="btn btn-success">Успех</button>
<button class="btn btn-warning">Предупреждение</button>
<button class="btn btn-danger">Опасность</button>

<!-- Размеры -->
<button class="btn btn-primary btn-sm">Маленькая</button>
<button class="btn btn-primary">Обычная</button>
<button class="btn btn-primary btn-lg">Большая</button>

<!-- Элитная кнопка -->
<button class="btn btn-elite">Элитная</button>
```

### Бейджи
```html
<span class="badge bg-success">Успех</span>
<span class="badge bg-warning">Предупреждение</span>
<span class="badge bg-danger">Опасность</span>
<span class="badge bg-info">Информация</span>
<span class="badge bg-primary">Основной</span>
<span class="badge bg-secondary">Вторичный</span>
```

### Аватары
```html
<!-- Аватар пользователя -->
<div class="user-avatar">
    <div class="avatar-circle">
        <i class="bi bi-person-fill"></i>
    </div>
</div>

<!-- Аватар с изображением -->
<div class="user-avatar">
    <img src="avatar.jpg" class="avatar-image" alt="Avatar">
</div>
```

### Формы
```html
<!-- Поле поиска -->
<div class="search-box">
    <i class="bi bi-search search-icon"></i>
    <input type="text" class="form-control" placeholder="Поиск...">
</div>

<!-- Переключатели -->
<div class="filter-switches">
    <div class="form-check form-switch">
        <input class="form-check-input" type="checkbox" id="switch1">
        <label class="form-check-label" for="switch1">Опция 1</label>
    </div>
</div>
```

### Сетки
```html
<!-- Сетка информационных карточек -->
<div class="info-cards-grid">
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
</div>

<!-- Сетка пользователей/комнат -->
<div class="users-grid">
    <!-- или .rooms-grid, .spaces-grid -->
    <div class="card">...</div>
    <div class="card">...</div>
</div>
```

### Статистика
```html
<div class="stats-grid">
    <div class="stat-item">
        <div class="stat-number">123</div>
        <div class="stat-label">Пользователи</div>
    </div>
    <div class="stat-item">
        <div class="stat-number success">45ms</div>
        <div class="stat-label">Ответ</div>
    </div>
</div>
```

### Индикаторы статуса
```html
<div class="status-indicators">
    <div class="status-item">
        <div class="status-dot bg-success"></div>
        <span>API работает</span>
    </div>
    <div class="status-item">
        <div class="status-dot bg-danger"></div>
        <span>Ошибка подключения</span>
    </div>
</div>
```

### Пустые состояния
```html
<div class="empty-state">
    <div class="empty-icon">
        <i class="bi bi-inbox"></i>
    </div>
    <h5>Нет данных</h5>
    <p>Попробуйте изменить фильтры</p>
    <button class="btn btn-outline-primary">Показать все</button>
</div>
```

## 📱 Адаптивность

### Брейкпоинты
- **Desktop**: > 1200px - полная сетка
- **Tablet**: 768px - 1200px - адаптированная сетка
- **Mobile**: < 768px - одна колонка

### Адаптивные сетки
```css
/* Desktop: 3-4 колонки */
.info-cards-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

/* Tablet: 2-3 колонки */
@media (max-width: 1200px) {
    .info-cards-grid {
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    }
}

/* Mobile: 1 колонка */
@media (max-width: 768px) {
    .info-cards-grid {
        grid-template-columns: 1fr;
    }
}
```

## 🌙 Темная тема

### Переключение переменных
```css
[data-bs-theme="dark"] {
    --text-primary: #e9ecef;
    --text-secondary: #adb5bd;
    --bg-white: #23263a;
    --bg-glass: rgba(52, 58, 70, 0.95);
    --border-color: rgba(102, 126, 234, 0.2);
}
```

### Автоматическая адаптация
Все компоненты автоматически адаптируются к темной теме через CSS переменные.

## 🔧 Утилиты

### Отступы
```html
<div class="p-lg">padding: var(--spacing-lg)</div>
<div class="m-xl">margin: var(--spacing-xl)</div>
```

### Типографика
```html
<span class="text-lg">Большой текст</span>
<span class="fw-semibold">Полужирный</span>
```

### Эффекты
```html
<div class="hover-lift">Поднимается при наведении</div>
<div class="fade-in-up">Анимация появления</div>
<div class="text-gradient">Градиентный текст</div>
```

## 📝 Правила использования

1. **Никогда не используйте inline стили** - только классы
2. **Всегда используйте CSS переменные** для цветов и размеров
3. **Следуйте BEM методологии** для новых компонентов
4. **Тестируйте в темной теме** - все должно работать автоматически
5. **Проверяйте адаптивность** на всех устройствах

## 🚀 Расширение системы

### Добавление нового компонента
1. Создайте секцию в `admin.css`
2. Используйте существующие переменные
3. Добавьте поддержку темной темы
4. Документируйте в этом файле

### Пример нового компонента
```css
/* ==========================================================================
   NEW COMPONENT
   ========================================================================== */

.new-component {
    background: var(--bg-glass);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    padding: var(--spacing);
    transition: var(--transition);
}

.new-component:hover {
    box-shadow: var(--shadow-hover);
}

[data-bs-theme="dark"] .new-component {
    background: var(--bg-glass-dark);
}
```

## 🔢 Z-Index система

### Слои наложения
```css
--z-dropdown: 1000;       /* Обычные выпадающие меню */
--z-sticky: 1020;         /* Закрепленные элементы */
--z-fixed: 1030;          /* Фиксированные элементы */
--z-modal-backdrop: 1040; /* Фон модальных окон */
--z-modal: 1050;          /* Модальные окна */
--z-popover: 1060;        /* Всплывающие подсказки */
--z-tooltip: 1070;        /* Тултипы */
--z-language: 9999;       /* Языковое меню (поверх всего) */
```

### Специальные случаи
- **Языковое меню** всегда поверх всех элементов (z-index: 9999)
- **Навигационные dropdown** используют высокий приоритет
- **Модальные окна** блокируют взаимодействие с фоном

---

**Создано для EPT-MX-ADM** - современная система дизайна для Matrix админ-панели. 