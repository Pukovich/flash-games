def cart_items_count(request):
    """Контекст-процессор для совместимости с существующими шаблонами"""
    return {'cart_items_count': 0} 