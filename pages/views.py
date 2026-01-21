from django.views.generic import TemplateView
from django.views.defaults import page_not_found, server_error
from django.shortcuts import render

class AboutView(TemplateView):
    """Статичная страница 'О проекте'."""
    template_name = 'pages/about.html'

class RulesView(TemplateView):
    """Статичная страница 'Правила'."""
    template_name = 'pages/rules.html'

# Обработчики ошибок
def page_not_found_handler(request, exception):
    """Обработка ошибки 404."""
    return page_not_found(request, exception, template_name='pages/404.html')

def server_error_handler(request):
    """Обработка ошибки 500."""
    return server_error(request, template_name='pages/500.html')

def csrf_failure_handler(request, reason=""):
    """Обработка ошибки 403 CSRF."""
    return render(request, 'pages/403csrf.html', status=403)

def csrf_failure(request, reason=""):
    return render(request, '403.html', status=403)