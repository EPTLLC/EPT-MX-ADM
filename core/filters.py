"""
Project: EPT-MX-ADM
Company: EasyProTech LLC (www.easypro.tech)
Dev: Brabus
Date: Thu 23 Oct 2025 22:56:11 UTC
Status: Jinja2 Filters
Telegram: https://t.me/EasyProTech

Jinja2 filters for EPT-MX-ADM
"""

from utils.i18n import t


def datetime_format(value):
    """Date and time formatting"""
    if value is None:
        return t("messages.not_specified")
    
    if isinstance(value, (int, float)):
        import datetime
        
        # Автоматическое определение формата timestamp
        # Если значение больше 1e10, то это миллисекунды, иначе секунды
        if value > 1e10:
            # Timestamp в миллисекундах
            dt = datetime.datetime.fromtimestamp(value / 1000)
        else:
            # Timestamp в секундах
            dt = datetime.datetime.fromtimestamp(value)
            
        return dt.strftime('%d.%m.%Y %H:%M')
    
    return str(value)


def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s:,} {size_names[i]}"


def register_filters(app):
    """Register all Jinja2 filters with the Flask app"""
    app.template_filter('datetime_format')(datetime_format)
    app.template_filter('format_file_size')(format_file_size) 