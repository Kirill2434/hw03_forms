from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    today = datetime.today()
    now = int(today.strftime('%Y'))
    return {
        'year': now
    }
