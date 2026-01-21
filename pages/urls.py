from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('rules/', views.RulesView.as_view(), name='rules'),    # ← .as_view()
    path('about/', views.AboutView.as_view(), name='about'),    # ← .as_view()
]