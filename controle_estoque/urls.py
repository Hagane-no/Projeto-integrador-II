from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('estoque.urls')), # <-- Isto é fundamental para que as rotas da app funcionem
]
