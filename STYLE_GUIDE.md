# 📋 Style Guide - EPT-MX-ADM

Краткое руководство по единой системе стилей проекта.

## 🎯 Основные принципы

### ✅ Правильно
```html
<!-- Используйте классы из дизайн-системы -->
<div class="card">
    <div class="card-header">
        <i class="bi bi-users"></i>
        <span>Пользователи</span>
    </div>
    <div class="card-body">
        <div class="users-grid">
            <!-- контент -->
        </div>
    </div>
</div>
```

### ❌ Неправильно
```html
<!-- НЕ используйте inline стили -->
<div style="background: white; padding: 20px; border-radius: 10px;">
    <h3 style="color: #4e73df;">Заголовок</h3>
</div>
```

## 🎨 Быстрый справочник

### Карточки
```html
<div class="card">Базовая</div>
<div class="card card-status">Со статусной полосой</div>
<div class="card elite-card">Элитная</div>
```

### Кнопки
```html
<button class="btn btn-primary">Основная</button>
<button class="btn btn-outline-primary">Контурная</button>
<button class="btn btn-elite">Элитная</button>
```

### Сетки
```html
<div class="info-cards-grid">Информационные карточки</div>
<div class="users-grid">Пользователи</div>
<div class="rooms-grid">Комнаты</div>
```

### Формы
```html
<div class="search-box">
    <i class="bi bi-search search-icon"></i>
    <input class="form-control" placeholder="Поиск...">
</div>
```

### Бейджи
```html
<span class="badge bg-success">Успех</span>
<span class="badge bg-danger">Ошибка</span>
<span class="badge bg-warning">Предупреждение</span>
```

## 🔧 CSS переменные

### Цвета
- `var(--primary-color)` - основной цвет
- `var(--success-color)` - зеленый
- `var(--danger-color)` - красный
- `var(--text-primary)` - основной текст
- `var(--text-muted)` - приглушенный текст

### Размеры
- `var(--spacing-xs)` - 4px
- `var(--spacing-sm)` - 8px  
- `var(--spacing)` - 16px
- `var(--spacing-lg)` - 24px
- `var(--spacing-xl)` - 32px

### Скругления
- `var(--border-radius-sm)` - 6px
- `var(--border-radius)` - 12px
- `var(--border-radius-lg)` - 16px

## 📱 Адаптивность

Все компоненты автоматически адаптивны:
- Desktop: > 1200px
- Tablet: 768px - 1200px  
- Mobile: < 768px

## 🌙 Темная тема

Все компоненты автоматически поддерживают темную тему через CSS переменные.

## 📝 Чеклист для разработчика

- [ ] Используются только классы из дизайн-системы
- [ ] Нет inline стилей в HTML
- [ ] Компонент работает в темной теме
- [ ] Компонент адаптивен на всех устройствах
- [ ] Используются CSS переменные для цветов и размеров

## 🔗 Полная документация

Подробная документация: [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md) 